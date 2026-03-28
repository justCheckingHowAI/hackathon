#!/usr/bin/env python3
"""Export a GitHub repository's commits and pull requests to graph-friendly CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PR_GRAPHQL_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 100, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        number
        title
        state
        createdAt
        closedAt
        mergedAt
        url
        author {
          login
        }
        baseRefName
        headRefName
        headRefOid
        mergeCommit {
          oid
        }
        comments {
          totalCount
        }
        reviews {
          totalCount
        }
        commits {
          totalCount
        }
      }
    }
  }
}
"""


def run_gh_api(endpoint: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    page_number = 1
    separator = "&" if "?" in endpoint else "?"

    while True:
        paged_endpoint = f"{endpoint}{separator}page={page_number}"
        command = [
            "gh",
            "api",
            "-H",
            "Accept: application/vnd.github+json",
            paged_endpoint,
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip() or "unknown gh error"
            raise RuntimeError(f"gh api failed for {paged_endpoint}: {message}")

        page = json.loads(result.stdout or "[]")
        if isinstance(page, list):
            page_records = [item for item in page if isinstance(item, dict)]
            records.extend(page_records)
            if len(page_records) < 100:
                break
        elif isinstance(page, dict):
            records.append(page)
            break
        else:
            break

        page_number += 1

    return records


def run_gh_graphql(query: str, variables: dict[str, str]) -> dict[str, Any]:
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        command.extend(["-F", f"{key}={value}"])

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown gh error"
        raise RuntimeError(f"gh graphql failed: {message}")
    return json.loads(result.stdout or "{}")


def safe_login(user: dict[str, Any] | None) -> str:
    if not isinstance(user, dict):
        return ""
    return str(user.get("login") or "").strip()


def safe_name(value: Any) -> str:
    return str(value or "").strip()


def email_hash(email: str) -> str:
    normalized = email.strip().lower()
    if not normalized:
        return ""
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def author_key(login: str, name: str, email: str) -> str:
    if login:
        return f"github:{login.lower()}"
    if email:
        return f"email:{email_hash(email)}"
    if name:
        return f"name:{name.lower()}"
    return "unknown:unknown"


def ensure_author(
    authors: dict[str, dict[str, str]],
    *,
    login: str,
    name: str,
    email: str,
    source: str,
) -> str:
    key = author_key(login, name, email)
    current = authors.get(key)
    hashed_email = email_hash(email)
    if current is None:
        authors[key] = {
            "author_id": key,
            "login": login,
            "display_name": name,
            "email_hash": hashed_email,
            "source": source,
        }
        return key

    if login and not current["login"]:
        current["login"] = login
    if name and not current["display_name"]:
        current["display_name"] = name
    if hashed_email and not current["email_hash"]:
        current["email_hash"] = hashed_email
    if source and current["source"] != source:
        current["source"] = f"{current['source']},{source}"
    return key


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fetch_prs(repo: str) -> list[dict[str, Any]]:
    owner, name = repo.split("/", 1)
    prs: list[dict[str, Any]] = []
    cursor: str | None = None

    while True:
        variables = {"owner": owner, "name": name}
        if cursor:
            variables["cursor"] = cursor

        response = run_gh_graphql(PR_GRAPHQL_QUERY, variables)
        repository = response.get("data", {}).get("repository", {})
        pull_requests = repository.get("pullRequests", {}) if isinstance(repository, dict) else {}
        nodes = pull_requests.get("nodes", []) if isinstance(pull_requests, dict) else []

        for node in nodes:
            if not isinstance(node, dict):
                continue
            prs.append(
                {
                    "number": node.get("number"),
                    "title": node.get("title"),
                    "state": str(node.get("state") or "").lower(),
                    "created_at": node.get("createdAt"),
                    "closed_at": node.get("closedAt"),
                    "merged_at": node.get("mergedAt"),
                    "html_url": node.get("url"),
                    "user": {"login": safe_login(node.get("author"))},
                    "base": {"ref": safe_name(node.get("baseRefName"))},
                    "head": {
                        "ref": safe_name(node.get("headRefName")),
                        "sha": safe_name(node.get("headRefOid")),
                    },
                    "merge_commit_sha": safe_name(node.get("mergeCommit", {}).get("oid")) if isinstance(node.get("mergeCommit"), dict) else "",
                    "comments": node.get("comments", {}).get("totalCount", 0) if isinstance(node.get("comments"), dict) else 0,
                    "review_comments": node.get("reviews", {}).get("totalCount", 0) if isinstance(node.get("reviews"), dict) else 0,
                    "commits": node.get("commits", {}).get("totalCount", 0) if isinstance(node.get("commits"), dict) else 0,
                }
            )

        page_info = pull_requests.get("pageInfo", {}) if isinstance(pull_requests, dict) else {}
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        if not cursor:
            break

    return prs


def fetch_commits(repo: str) -> list[dict[str, Any]]:
    endpoint = f"repos/{repo}/commits?per_page=100"
    return run_gh_api(endpoint)


def normalize_data(repo: str, prs: list[dict[str, Any]], commits: list[dict[str, Any]]) -> dict[str, Any]:
    authors: dict[str, dict[str, str]] = {}
    commit_rows: list[dict[str, Any]] = []
    pr_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str]] = set()

    commit_shas: set[str] = set()
    for commit in commits:
        sha = safe_name(commit.get("sha"))
        if not sha:
            continue

        commit_author = commit.get("commit", {}).get("author", {}) if isinstance(commit.get("commit"), dict) else {}
        committer = commit.get("commit", {}).get("committer", {}) if isinstance(commit.get("commit"), dict) else {}
        login = safe_login(commit.get("author"))
        display_name = safe_name(commit_author.get("name"))
        email = safe_name(commit_author.get("email"))
        author_id = ensure_author(
            authors,
            login=login,
            name=display_name,
            email=email,
            source="commit",
        )

        commit_rows.append(
            {
                "commit_sha": sha,
                "repo": repo,
                "author_id": author_id,
                "author_login": login,
                "author_name": display_name,
                "author_email_hash": email_hash(email),
                "committer_login": safe_login(commit.get("committer")),
                "committer_name": safe_name(committer.get("name")),
                "committed_at": safe_name(commit_author.get("date")),
                "message": safe_name(commit.get("commit", {}).get("message")),
                "parent_count": len(commit.get("parents", []) or []),
                "is_merge_commit": len(commit.get("parents", []) or []) > 1,
                "html_url": safe_name(commit.get("html_url")),
            }
        )
        commit_shas.add(sha)

        edge = (author_id, "authored_commit", sha)
        if edge not in seen_edges:
            seen_edges.add(edge)
            edge_rows.append(
                {
                    "source_id": author_id,
                    "source_type": "AUTHOR",
                    "relation": "authored_commit",
                    "target_id": sha,
                    "target_type": "COMMIT",
                    "repo": repo,
                    "metadata": "",
                }
            )

    for pr in prs:
        number = pr.get("number")
        if number is None:
            continue

        pr_user = pr.get("user") if isinstance(pr.get("user"), dict) else {}
        login = safe_login(pr_user)
        display_name = safe_name(pr_user.get("login"))
        author_id = ensure_author(
            authors,
            login=login,
            name=display_name,
            email="",
            source="pr",
        )

        pr_id = f"{repo}#PR-{number}"
        merge_commit_sha = safe_name(pr.get("merge_commit_sha"))
        is_merged = bool(pr.get("merged_at"))
        pr_rows.append(
            {
                "pr_id": pr_id,
                "repo": repo,
                "number": number,
                "author_id": author_id,
                "author_login": login,
                "title": safe_name(pr.get("title")),
                "state": safe_name(pr.get("state")),
                "created_at": safe_name(pr.get("created_at")),
                "closed_at": safe_name(pr.get("closed_at")),
                "merged_at": safe_name(pr.get("merged_at")),
                "is_merged": is_merged,
                "merge_commit_sha": merge_commit_sha,
                "head_sha": safe_name(pr.get("head", {}).get("sha")) if isinstance(pr.get("head"), dict) else "",
                "head_ref": safe_name(pr.get("head", {}).get("ref")) if isinstance(pr.get("head"), dict) else "",
                "base_ref": safe_name(pr.get("base", {}).get("ref")) if isinstance(pr.get("base"), dict) else "",
                "comments": pr.get("comments") or 0,
                "review_comments": pr.get("review_comments") or 0,
                "commits": pr.get("commits") or 0,
                "html_url": safe_name(pr.get("html_url")),
            }
        )

        open_edge = (author_id, "opened_pr", pr_id)
        if open_edge not in seen_edges:
            seen_edges.add(open_edge)
            edge_rows.append(
                {
                    "source_id": author_id,
                    "source_type": "AUTHOR",
                    "relation": "opened_pr",
                    "target_id": pr_id,
                    "target_type": "PR",
                    "repo": repo,
                    "metadata": "",
                }
            )

        if merge_commit_sha and merge_commit_sha in commit_shas:
            merge_edge = (pr_id, "merged_as", merge_commit_sha)
            if merge_edge not in seen_edges:
                seen_edges.add(merge_edge)
                edge_rows.append(
                    {
                        "source_id": pr_id,
                        "source_type": "PR",
                        "relation": "merged_as",
                        "target_id": merge_commit_sha,
                        "target_type": "COMMIT",
                        "repo": repo,
                        "metadata": "",
                    }
                )

        head_sha = safe_name(pr.get("head", {}).get("sha")) if isinstance(pr.get("head"), dict) else ""
        if head_sha and head_sha in commit_shas:
            head_edge = (pr_id, "head_commit", head_sha)
            if head_edge not in seen_edges:
                seen_edges.add(head_edge)
                edge_rows.append(
                    {
                        "source_id": pr_id,
                        "source_type": "PR",
                        "relation": "head_commit",
                        "target_id": head_sha,
                        "target_type": "COMMIT",
                        "repo": repo,
                        "metadata": "",
                    }
                )

    author_rows = sorted(authors.values(), key=lambda row: row["author_id"])
    commit_rows.sort(key=lambda row: row["committed_at"], reverse=True)
    pr_rows.sort(key=lambda row: row["created_at"], reverse=True)

    return {
        "authors": author_rows,
        "commits": commit_rows,
        "prs": pr_rows,
        "edges": edge_rows,
    }


def write_outputs(output_dir: Path, repo: str, prs: list[dict[str, Any]], commits: list[dict[str, Any]], graph: dict[str, Any]) -> None:
    raw_dir = output_dir / "raw"
    csv_dir = output_dir / "csv"
    raw_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    (raw_dir / "prs.json").write_text(json.dumps(prs, indent=2), encoding="utf-8")
    (raw_dir / "commits.json").write_text(json.dumps(commits, indent=2), encoding="utf-8")
    (output_dir / "summary.json").write_text(
        json.dumps(
            {
                "repo": repo,
                "authors": len(graph["authors"]),
                "commits": len(graph["commits"]),
                "prs": len(graph["prs"]),
                "edges": len(graph["edges"]),
                "merged_prs": sum(1 for pr in graph["prs"] if pr["is_merged"]),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    write_csv(
        csv_dir / "authors.csv",
        ["author_id", "login", "display_name", "email_hash", "source"],
        graph["authors"],
    )
    write_csv(
        csv_dir / "commits.csv",
        [
            "commit_sha",
            "repo",
            "author_id",
            "author_login",
            "author_name",
            "author_email_hash",
            "committer_login",
            "committer_name",
            "committed_at",
            "message",
            "parent_count",
            "is_merge_commit",
            "html_url",
        ],
        graph["commits"],
    )
    write_csv(
        csv_dir / "prs.csv",
        [
            "pr_id",
            "repo",
            "number",
            "author_id",
            "author_login",
            "title",
            "state",
            "created_at",
            "closed_at",
            "merged_at",
            "is_merged",
            "merge_commit_sha",
            "head_sha",
            "head_ref",
            "base_ref",
            "comments",
            "review_comments",
            "commits",
            "html_url",
        ],
        graph["prs"],
    )
    write_csv(
        csv_dir / "edges.csv",
        ["source_id", "source_type", "relation", "target_id", "target_type", "repo", "metadata"],
        graph["edges"],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="Public GitHub repo in owner/name format")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory. Defaults to data/github-graph/outputs/<owner>__<repo>",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.strip()
    if repo.count("/") != 1:
        print("Repo must use owner/name format.", file=sys.stderr)
        return 1

    default_output = Path("data/github-graph/outputs") / repo.replace("/", "__")
    output_dir = Path(args.output_dir) if args.output_dir else default_output

    print(f"Fetching pull requests for {repo}...")
    prs = fetch_prs(repo)
    print(f"Fetched {len(prs)} pull requests")

    print(f"Fetching commits for {repo}...")
    commits = fetch_commits(repo)
    print(f"Fetched {len(commits)} commits")

    print("Normalizing graph data...")
    graph = normalize_data(repo, prs, commits)
    write_outputs(output_dir, repo, prs, commits, graph)

    print(f"Done. Output written to {output_dir}")
    print(
        json.dumps(
            {
                "repo": repo,
                "authors": len(graph["authors"]),
                "commits": len(graph["commits"]),
                "prs": len(graph["prs"]),
                "edges": len(graph["edges"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
