from __future__ import annotations

from fastapi import FastAPI, HTTPException

from db import DatabaseConfigError, get_database


app = FastAPI(title="API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from FastAPI"}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def db_healthcheck() -> dict[str, str]:
    try:
        db = get_database()
        db.ping()
    except DatabaseConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}") from exc

    return {"status": "ok"}


@app.get("/organizations")
def list_organizations() -> list[dict[str, str]]:
    db = get_database()
    return db.fetch_all(
        "SELECT id::text, name, slug, created_at::text FROM organizations ORDER BY created_at"
    )


@app.get("/people")
def list_people() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        """
        SELECT
            p.id::text,
            p.external_key,
            p.full_name,
            p.display_name,
            p.role_title,
            p.seniority,
            p.department,
            p.github_login,
            p.clone_status,
            p.status,
            p.rag_corpus_name,
            o.name AS organization_name
        FROM people p
        JOIN organizations o ON o.id = p.organization_id
        ORDER BY p.full_name
        """
    )


@app.get("/skills")
def list_skills() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        """
        SELECT
            s.id::text,
            s.canonical_name,
            s.category,
            s.description,
            o.name AS organization_name
        FROM skills s
        JOIN organizations o ON o.id = s.organization_id
        ORDER BY s.category, s.canonical_name
        """
    )


@app.get("/relationships")
def list_relationships() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        """
        SELECT
            r.id::text,
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
        """
    )
