#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from neo4j import GraphDatabase
    from neo4j.exceptions import ServiceUnavailable
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        'Missing dependency: install the `neo4j` package with `pip install neo4j`.'
    ) from exc


RELATIONSHIP_TYPES = {
    'authored_commit': 'AUTHORED_COMMIT',
    'opened_pr': 'OPENED_PR',
    'merged_as': 'MERGED_AS',
    'head_commit': 'HEAD_COMMIT',
}

NODE_LABELS = {
    'AUTHOR': 'Author',
    'COMMIT': 'Commit',
    'PR': 'PullRequest',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Push exported GitHub graph CSVs to Neo4j.')
    parser.add_argument(
        '--outputs-dir',
        default=str(Path(__file__).resolve().parent / 'github-graph' / 'outputs'),
        help='Directory containing exported repo folders.',
    )
    parser.add_argument(
        '--repo-dir',
        default=None,
        help='Single exported repo directory to import instead of all directories in outputs-dir.',
    )
    parser.add_argument(
        '--env-file',
        default=str(Path(__file__).resolve().parent / '.env'),
        help='Optional env file with NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD.',
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=500,
        help='Rows per Neo4j batch.',
    )
    return parser.parse_args()


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def get_setting(name: str, env_values: dict[str, str]) -> str:
    return os.environ.get(name, env_values.get(name, '')).strip()


def maybe_fix_neo4j_uri(uri: str) -> tuple[str, str | None]:
    parsed = urlparse(uri)
    if parsed.scheme not in {'bolt', 'neo4j'}:
        return uri, None

    if parsed.port != 7474:
        return uri, None

    fixed_uri = parsed._replace(netloc=f'{parsed.hostname}:7687').geturl()
    message = f'Neo4j Bolt usually runs on 7687, switching from {uri} to {fixed_uri}.'
    return fixed_uri, message


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open('r', encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def chunked(rows: list[dict[str, Any]], size: int):
    for start in range(0, len(rows), size):
        yield rows[start:start + size]


def to_bool(value: Any) -> bool:
    return str(value).strip().lower() in {'1', 'true', 'yes'}


def clean_value(value: Any) -> Any:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def normalize_author_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized.append(
            {
                'author_id': row['author_id'],
                'login': clean_value(row.get('login')),
                'display_name': clean_value(row.get('display_name')),
                'email_hash': clean_value(row.get('email_hash')),
                'source': clean_value(row.get('source')),
            }
        )
    return normalized


def normalize_commit_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized.append(
            {
                'commit_sha': row['commit_sha'],
                'repo': clean_value(row.get('repo')),
                'author_id': clean_value(row.get('author_id')),
                'author_login': clean_value(row.get('author_login')),
                'author_name': clean_value(row.get('author_name')),
                'author_email_hash': clean_value(row.get('author_email_hash')),
                'committer_login': clean_value(row.get('committer_login')),
                'committer_name': clean_value(row.get('committer_name')),
                'committed_at': clean_value(row.get('committed_at')),
                'message': clean_value(row.get('message')),
                'parent_count': int(row.get('parent_count') or 0),
                'is_merge_commit': to_bool(row.get('is_merge_commit')),
                'html_url': clean_value(row.get('html_url')),
            }
        )
    return normalized


def normalize_pr_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized.append(
            {
                'pr_id': row['pr_id'],
                'repo': clean_value(row.get('repo')),
                'number': int(row.get('number') or 0),
                'author_id': clean_value(row.get('author_id')),
                'author_login': clean_value(row.get('author_login')),
                'title': clean_value(row.get('title')),
                'state': clean_value(row.get('state')),
                'created_at': clean_value(row.get('created_at')),
                'closed_at': clean_value(row.get('closed_at')),
                'merged_at': clean_value(row.get('merged_at')),
                'is_merged': to_bool(row.get('is_merged')),
                'merge_commit_sha': clean_value(row.get('merge_commit_sha')),
                'head_sha': clean_value(row.get('head_sha')),
                'head_ref': clean_value(row.get('head_ref')),
                'base_ref': clean_value(row.get('base_ref')),
                'comments': int(row.get('comments') or 0),
                'review_comments': int(row.get('review_comments') or 0),
                'commits': int(row.get('commits') or 0),
                'html_url': clean_value(row.get('html_url')),
            }
        )
    return normalized


def normalize_edge_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        relation = RELATIONSHIP_TYPES.get(str(row.get('relation') or '').strip())
        source_label = NODE_LABELS.get(str(row.get('source_type') or '').strip())
        target_label = NODE_LABELS.get(str(row.get('target_type') or '').strip())
        if not relation or not source_label or not target_label:
            continue

        normalized.append(
            {
                'source_id': row['source_id'],
                'target_id': row['target_id'],
                'repo': clean_value(row.get('repo')),
                'metadata': clean_value(row.get('metadata')),
                'relation': relation,
                'source_label': source_label,
                'target_label': target_label,
            }
        )
    return normalized


def create_constraints(driver: Any) -> None:
    statements = [
        'CREATE CONSTRAINT author_id IF NOT EXISTS FOR (n:Author) REQUIRE n.author_id IS UNIQUE',
        'CREATE CONSTRAINT commit_sha IF NOT EXISTS FOR (n:Commit) REQUIRE n.commit_sha IS UNIQUE',
        'CREATE CONSTRAINT pr_id IF NOT EXISTS FOR (n:PullRequest) REQUIRE n.pr_id IS UNIQUE',
    ]
    with driver.session() as session:
        for statement in statements:
            session.run(statement).consume()


def import_authors(driver: Any, rows: list[dict[str, Any]], batch_size: int) -> None:
    query = '''
    UNWIND $rows AS row
    MERGE (a:Author {author_id: row.author_id})
    SET a.login = row.login,
        a.display_name = row.display_name,
        a.email_hash = row.email_hash,
        a.source = row.source
    '''
    with driver.session() as session:
        for batch in chunked(rows, batch_size):
            session.run(query, rows=batch).consume()


def import_commits(driver: Any, rows: list[dict[str, Any]], batch_size: int) -> None:
    query = '''
    UNWIND $rows AS row
    MERGE (c:Commit {commit_sha: row.commit_sha})
    SET c.repo = row.repo,
        c.author_id = row.author_id,
        c.author_login = row.author_login,
        c.author_name = row.author_name,
        c.author_email_hash = row.author_email_hash,
        c.committer_login = row.committer_login,
        c.committer_name = row.committer_name,
        c.committed_at = row.committed_at,
        c.message = row.message,
        c.parent_count = row.parent_count,
        c.is_merge_commit = row.is_merge_commit,
        c.html_url = row.html_url
    '''
    with driver.session() as session:
        for batch in chunked(rows, batch_size):
            session.run(query, rows=batch).consume()


def import_prs(driver: Any, rows: list[dict[str, Any]], batch_size: int) -> None:
    query = '''
    UNWIND $rows AS row
    MERGE (p:PullRequest {pr_id: row.pr_id})
    SET p.repo = row.repo,
        p.number = row.number,
        p.author_id = row.author_id,
        p.author_login = row.author_login,
        p.title = row.title,
        p.state = row.state,
        p.created_at = row.created_at,
        p.closed_at = row.closed_at,
        p.merged_at = row.merged_at,
        p.is_merged = row.is_merged,
        p.merge_commit_sha = row.merge_commit_sha,
        p.head_sha = row.head_sha,
        p.head_ref = row.head_ref,
        p.base_ref = row.base_ref,
        p.comments = row.comments,
        p.review_comments = row.review_comments,
        p.commits = row.commits,
        p.html_url = row.html_url
    '''
    with driver.session() as session:
        for batch in chunked(rows, batch_size):
            session.run(query, rows=batch).consume()


def import_edges(driver: Any, rows: list[dict[str, Any]], batch_size: int) -> None:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for row in rows:
        key = (row['source_label'], row['target_label'], row['relation'])
        grouped.setdefault(key, []).append(row)

    with driver.session() as session:
        for (source_label, target_label, relation), relation_rows in grouped.items():
            query = f'''
            UNWIND $rows AS row
            MATCH (source:{source_label})
            MATCH (target:{target_label})
            WHERE (
                ({'source.author_id' if source_label == 'Author' else 'source.commit_sha' if source_label == 'Commit' else 'source.pr_id'}) = row.source_id
            ) AND (
                ({'target.author_id' if target_label == 'Author' else 'target.commit_sha' if target_label == 'Commit' else 'target.pr_id'}) = row.target_id
            )
            MERGE (source)-[r:{relation}]->(target)
            SET r.repo = row.repo,
                r.metadata = row.metadata
            '''
            for batch in chunked(relation_rows, batch_size):
                session.run(query, rows=batch).consume()


def discover_repo_dirs(outputs_dir: Path, repo_dir: str | None) -> list[Path]:
    if repo_dir:
        target = Path(repo_dir).resolve()
        if not target.exists():
            raise FileNotFoundError(f'Repo directory not found: {target}')
        return [target]

    if not outputs_dir.exists():
        raise FileNotFoundError(f'Outputs directory not found: {outputs_dir}')

    return sorted(path for path in outputs_dir.iterdir() if path.is_dir())


def import_repo_dir(driver: Any, repo_dir: Path, batch_size: int) -> dict[str, int]:
    csv_dir = repo_dir / 'csv'
    authors = normalize_author_rows(read_csv_rows(csv_dir / 'authors.csv'))
    commits = normalize_commit_rows(read_csv_rows(csv_dir / 'commits.csv'))
    prs = normalize_pr_rows(read_csv_rows(csv_dir / 'prs.csv'))
    edges = normalize_edge_rows(read_csv_rows(csv_dir / 'edges.csv'))

    import_authors(driver, authors, batch_size)
    import_commits(driver, commits, batch_size)
    import_prs(driver, prs, batch_size)
    import_edges(driver, edges, batch_size)

    return {
        'authors': len(authors),
        'commits': len(commits),
        'prs': len(prs),
        'edges': len(edges),
    }


def main() -> int:
    args = parse_args()
    env_values = load_env_file(Path(args.env_file))
    uri = get_setting('NEO4J_URI', env_values)
    user = get_setting('NEO4J_USER', env_values)
    password = get_setting('NEO4J_PASSWORD', env_values)

    if not uri or not user or not password:
        print(
            'Missing Neo4j config. Set NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD in env vars or --env-file.',
            file=sys.stderr,
        )
        return 1

    outputs_dir = Path(args.outputs_dir).resolve()
    repo_dirs = discover_repo_dirs(outputs_dir, args.repo_dir)
    if not repo_dirs:
        print('No exported repo directories found.', file=sys.stderr)
        return 1

    totals = {'authors': 0, 'commits': 0, 'prs': 0, 'edges': 0}

    uri, uri_message = maybe_fix_neo4j_uri(uri)
    if uri_message:
        print(uri_message)

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        try:
            driver.verify_connectivity()
        except ServiceUnavailable as exc:
            print(f'Neo4j connection failed for {uri}: {exc}', file=sys.stderr)
            return 1
        create_constraints(driver)

        for repo_dir in repo_dirs:
            counts = import_repo_dir(driver, repo_dir, args.batch_size)
            for key, value in counts.items():
                totals[key] += value
            print(
                f'Imported {repo_dir.name}: '
                f"authors={counts['authors']} commits={counts['commits']} prs={counts['prs']} edges={counts['edges']}"
            )
    finally:
        driver.close()

    print(
        'Done: '
        f"authors={totals['authors']} commits={totals['commits']} prs={totals['prs']} edges={totals['edges']}"
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
