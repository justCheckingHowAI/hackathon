from __future__ import annotations

from fastapi import HTTPException

from db import get_database


def get_organizations_data() -> list[dict[str, str]]:
    db = get_database()
    return db.fetch_all(
        'SELECT id::text, name, slug, created_at::text FROM organizations ORDER BY created_at'
    )


def get_people_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        '''
        SELECT
            p.id::text,
            p.organization_id::text,
            p.external_key,
            p.full_name,
            p.display_name,
            p.role_title,
            p.seniority,
            p.department,
            p.bio,
            p.github_login,
            p.clone_status,
            p.status,
            p.rag_corpus_name,
            o.name AS organization_name
        FROM people p
        JOIN organizations o ON o.id = p.organization_id
        ORDER BY p.full_name
        '''
    )


def get_skills_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        '''
        SELECT
            s.id::text,
            s.organization_id::text,
            s.canonical_name,
            s.category,
            s.description,
            o.name AS organization_name
        FROM skills s
        JOIN organizations o ON o.id = s.organization_id
        ORDER BY s.category, s.canonical_name
        '''
    )


def get_projects_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        '''
        SELECT
            p.id::text,
            p.organization_id::text,
            p.name,
            p.slug,
            p.description,
            p.status,
            o.name AS organization_name
        FROM projects p
        JOIN organizations o ON o.id = p.organization_id
        ORDER BY p.name
        '''
    )


def get_relationships_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        '''
        SELECT
            r.id::text,
            r.organization_id::text,
            r.from_person_id::text,
            r.to_person_id::text,
            fp.full_name AS from_person,
            tp.full_name AS to_person,
            r.relationship_type,
            r.source,
            r.notes,
            r.strength::text,
            r.confidence::text
        FROM people_relationships r
        JOIN people fp ON fp.id = r.from_person_id
        JOIN people tp ON tp.id = r.to_person_id
        ORDER BY fp.full_name, tp.full_name, r.relationship_type
        '''
    )


def get_default_organization_id() -> str | None:
    organizations = get_organizations_data()
    if not organizations:
        return None
    return organizations[0]['id']


def require_default_organization_id() -> str:
    organization_id = get_default_organization_id()
    if organization_id is None:
        raise HTTPException(status_code=500, detail='No organization found. Seed the database first.')
    return organization_id


def get_dashboard_counts() -> dict[str, int]:
    db = get_database()
    return {
        'organizations': int(db.fetch_one('SELECT COUNT(*)::int AS count FROM organizations')['count']),
        'people': int(db.fetch_one('SELECT COUNT(*)::int AS count FROM people')['count']),
        'skills': int(db.fetch_one('SELECT COUNT(*)::int AS count FROM skills')['count']),
        'projects': int(db.fetch_one('SELECT COUNT(*)::int AS count FROM projects')['count']),
        'relationships': int(
            db.fetch_one('SELECT COUNT(*)::int AS count FROM people_relationships')['count']
        ),
    }
