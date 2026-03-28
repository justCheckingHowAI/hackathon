from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

import psycopg
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db import DatabaseConfigError, get_database


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="API")


def redirect_with_message(
    path: str,
    *,
    success: str | None = None,
    error: str | None = None,
) -> RedirectResponse:
    params: dict[str, str] = {}
    if success:
        params["success"] = success
    if error:
        params["error"] = error

    url = path
    if params:
        url = f"{path}?{urlencode(params)}"

    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


def render_template(
    request: Request,
    template_name: str,
    context: dict[str, object],
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={
            "request": request,
            "success": request.query_params.get("success"),
            "error": request.query_params.get("error"),
            **context,
        },
    )


def get_organizations_data() -> list[dict[str, str]]:
    db = get_database()
    return db.fetch_all(
        "SELECT id::text, name, slug, created_at::text FROM organizations ORDER BY created_at"
    )


def get_people_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        """
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
        """
    )


def get_skills_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        """
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
        """
    )


def get_projects_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        """
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
        """
    )


def get_relationships_data() -> list[dict[str, str | None]]:
    db = get_database()
    return db.fetch_all(
        """
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
        """
    )


def get_default_organization_id() -> str | None:
    organizations = get_organizations_data()
    if not organizations:
        return None
    return organizations[0]["id"]


def require_default_organization_id() -> str:
    organization_id = get_default_organization_id()
    if organization_id is None:
        raise HTTPException(status_code=500, detail="No organization found. Seed the database first.")
    return organization_id


def get_dashboard_counts() -> dict[str, int]:
    db = get_database()
    return {
        "organizations": int(db.fetch_one("SELECT COUNT(*)::int AS count FROM organizations")["count"]),
        "people": int(db.fetch_one("SELECT COUNT(*)::int AS count FROM people")["count"]),
        "skills": int(db.fetch_one("SELECT COUNT(*)::int AS count FROM skills")["count"]),
        "projects": int(db.fetch_one("SELECT COUNT(*)::int AS count FROM projects")["count"]),
        "relationships": int(
            db.fetch_one("SELECT COUNT(*)::int AS count FROM people_relationships")["count"]
        ),
    }


def handle_db_error(path: str, action: str, exc: Exception) -> RedirectResponse:
    message = f"Could not {action}. {str(exc).strip() or exc.__class__.__name__}"
    return redirect_with_message(path, error=message)


@app.get("/")
def read_root() -> RedirectResponse:
    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)


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
    return get_organizations_data()


@app.get("/people")
def list_people() -> list[dict[str, str | None]]:
    return get_people_data()


@app.get("/skills")
def list_skills() -> list[dict[str, str | None]]:
    return get_skills_data()


@app.get("/projects")
def list_projects() -> list[dict[str, str | None]]:
    return get_projects_data()


@app.get("/relationships")
def list_relationships() -> list[dict[str, str | None]]:
    return get_relationships_data()


@app.get("/ui", response_class=HTMLResponse)
def ui_home(request: Request) -> HTMLResponse:
    return render_template(
        request,
        "dashboard.html",
        {"counts": get_dashboard_counts()},
    )


@app.get("/ui/people", response_class=HTMLResponse)
def people_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    people = get_people_data()
    edit_person = next((person for person in people if person["id"] == edit_id), None)
    return render_template(
        request,
        "people.html",
        {
            "organizations": get_organizations_data(),
            "people": people,
            "edit_person": edit_person,
            "default_organization_id": get_default_organization_id(),
        },
    )


@app.post("/ui/people")
def create_person(
    organization_id: str = Form(...),
    external_key: str = Form(...),
    full_name: str = Form(...),
    display_name: str = Form(default=""),
    role_title: str = Form(default=""),
    seniority: str = Form(default=""),
    department: str = Form(default=""),
    bio: str = Form(default=""),
    github_login: str = Form(default=""),
    clone_status: str = Form(default="pending"),
    status_value: str = Form(default="active", alias="status"),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            """
            INSERT INTO people (
                organization_id,
                external_key,
                full_name,
                display_name,
                role_title,
                seniority,
                department,
                bio,
                github_login,
                clone_status,
                status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                organization_id,
                external_key.strip(),
                full_name.strip(),
                display_name.strip() or None,
                role_title.strip() or None,
                seniority.strip() or None,
                department.strip() or None,
                bio.strip() or None,
                github_login.strip() or None,
                clone_status.strip() or "pending",
                status_value.strip() or "active",
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error("/ui/people", "create person", exc)

    return redirect_with_message("/ui/people", success="Person created.")


@app.post("/ui/people/{person_id}/update")
def update_person(
    person_id: str,
    organization_id: str = Form(...),
    external_key: str = Form(...),
    full_name: str = Form(...),
    display_name: str = Form(default=""),
    role_title: str = Form(default=""),
    seniority: str = Form(default=""),
    department: str = Form(default=""),
    bio: str = Form(default=""),
    github_login: str = Form(default=""),
    clone_status: str = Form(default="pending"),
    status_value: str = Form(default="active", alias="status"),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            """
            UPDATE people
            SET organization_id = %s,
                external_key = %s,
                full_name = %s,
                display_name = %s,
                role_title = %s,
                seniority = %s,
                department = %s,
                bio = %s,
                github_login = %s,
                clone_status = %s,
                status = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (
                organization_id,
                external_key.strip(),
                full_name.strip(),
                display_name.strip() or None,
                role_title.strip() or None,
                seniority.strip() or None,
                department.strip() or None,
                bio.strip() or None,
                github_login.strip() or None,
                clone_status.strip() or "pending",
                status_value.strip() or "active",
                person_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(f"/ui/people?edit_id={person_id}", "update person", exc)

    return redirect_with_message("/ui/people", success="Person updated.")


@app.post("/ui/people/{person_id}/delete")
def delete_person(person_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute("DELETE FROM people WHERE id = %s", (person_id,))
    except psycopg.Error as exc:
        return handle_db_error("/ui/people", "delete person", exc)

    return redirect_with_message("/ui/people", success="Person deleted.")


@app.get("/ui/skills", response_class=HTMLResponse)
def skills_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    skills = get_skills_data()
    edit_skill = next((skill for skill in skills if skill["id"] == edit_id), None)
    return render_template(
        request,
        "skills.html",
        {
            "organizations": get_organizations_data(),
            "skills": skills,
            "edit_skill": edit_skill,
            "default_organization_id": get_default_organization_id(),
        },
    )


@app.post("/ui/skills")
def create_skill(
    organization_id: str = Form(...),
    canonical_name: str = Form(...),
    category: str = Form(...),
    description: str = Form(default=""),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            "INSERT INTO skills (organization_id, canonical_name, category, description) VALUES (%s, %s, %s, %s)",
            (
                organization_id,
                canonical_name.strip(),
                category.strip(),
                description.strip() or None,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error("/ui/skills", "create skill", exc)

    return redirect_with_message("/ui/skills", success="Skill created.")


@app.post("/ui/skills/{skill_id}/update")
def update_skill(
    skill_id: str,
    organization_id: str = Form(...),
    canonical_name: str = Form(...),
    category: str = Form(...),
    description: str = Form(default=""),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            """
            UPDATE skills
            SET organization_id = %s,
                canonical_name = %s,
                category = %s,
                description = %s
            WHERE id = %s
            """,
            (
                organization_id,
                canonical_name.strip(),
                category.strip(),
                description.strip() or None,
                skill_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(f"/ui/skills?edit_id={skill_id}", "update skill", exc)

    return redirect_with_message("/ui/skills", success="Skill updated.")


@app.post("/ui/skills/{skill_id}/delete")
def delete_skill(skill_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute("DELETE FROM skills WHERE id = %s", (skill_id,))
    except psycopg.Error as exc:
        return handle_db_error("/ui/skills", "delete skill", exc)

    return redirect_with_message("/ui/skills", success="Skill deleted.")


@app.get("/ui/projects", response_class=HTMLResponse)
def projects_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    projects = get_projects_data()
    edit_project = next((project for project in projects if project["id"] == edit_id), None)
    return render_template(
        request,
        "projects.html",
        {
            "organizations": get_organizations_data(),
            "projects": projects,
            "edit_project": edit_project,
            "default_organization_id": get_default_organization_id(),
        },
    )


@app.post("/ui/projects")
def create_project(
    organization_id: str = Form(...),
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(default=""),
    status_value: str = Form(default="active", alias="status"),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            "INSERT INTO projects (organization_id, name, slug, description, status) VALUES (%s, %s, %s, %s, %s)",
            (
                organization_id,
                name.strip(),
                slug.strip(),
                description.strip() or None,
                status_value.strip() or "active",
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error("/ui/projects", "create project", exc)

    return redirect_with_message("/ui/projects", success="Project created.")


@app.post("/ui/projects/{project_id}/update")
def update_project(
    project_id: str,
    organization_id: str = Form(...),
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(default=""),
    status_value: str = Form(default="active", alias="status"),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            """
            UPDATE projects
            SET organization_id = %s,
                name = %s,
                slug = %s,
                description = %s,
                status = %s
            WHERE id = %s
            """,
            (
                organization_id,
                name.strip(),
                slug.strip(),
                description.strip() or None,
                status_value.strip() or "active",
                project_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(f"/ui/projects?edit_id={project_id}", "update project", exc)

    return redirect_with_message("/ui/projects", success="Project updated.")


@app.post("/ui/projects/{project_id}/delete")
def delete_project(project_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    except psycopg.Error as exc:
        return handle_db_error("/ui/projects", "delete project", exc)

    return redirect_with_message("/ui/projects", success="Project deleted.")


@app.get("/ui/relationships", response_class=HTMLResponse)
def relationships_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    relationships = get_relationships_data()
    edit_relationship = next(
        (relationship for relationship in relationships if relationship["id"] == edit_id),
        None,
    )
    return render_template(
        request,
        "relationships.html",
        {
            "organizations": get_organizations_data(),
            "people": get_people_data(),
            "relationships": relationships,
            "edit_relationship": edit_relationship,
            "default_organization_id": get_default_organization_id(),
            "relationship_types": [
                "manager_of",
                "mentor_of",
                "reviewer_of",
                "collaborates_with",
                "depends_on",
                "backup_for",
                "knowledge_source_for",
            ],
        },
    )


@app.post("/ui/relationships")
def create_relationship(
    organization_id: str = Form(...),
    from_person_id: str = Form(...),
    to_person_id: str = Form(...),
    relationship_type: str = Form(...),
    strength: str = Form(default=""),
    confidence: str = Form(default="1"),
    source: str = Form(default=""),
    notes: str = Form(default=""),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            """
            INSERT INTO people_relationships (
                organization_id,
                from_person_id,
                to_person_id,
                relationship_type,
                strength,
                confidence,
                source,
                notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                organization_id,
                from_person_id,
                to_person_id,
                relationship_type.strip(),
                strength.strip() or None,
                confidence.strip() or "1",
                source.strip() or None,
                notes.strip() or None,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error("/ui/relationships", "create relationship", exc)

    return redirect_with_message("/ui/relationships", success="Relationship created.")


@app.post("/ui/relationships/{relationship_id}/update")
def update_relationship(
    relationship_id: str,
    organization_id: str = Form(...),
    from_person_id: str = Form(...),
    to_person_id: str = Form(...),
    relationship_type: str = Form(...),
    strength: str = Form(default=""),
    confidence: str = Form(default="1"),
    source: str = Form(default=""),
    notes: str = Form(default=""),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            """
            UPDATE people_relationships
            SET organization_id = %s,
                from_person_id = %s,
                to_person_id = %s,
                relationship_type = %s,
                strength = %s,
                confidence = %s,
                source = %s,
                notes = %s
            WHERE id = %s
            """,
            (
                organization_id,
                from_person_id,
                to_person_id,
                relationship_type.strip(),
                strength.strip() or None,
                confidence.strip() or "1",
                source.strip() or None,
                notes.strip() or None,
                relationship_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(
            f"/ui/relationships?edit_id={relationship_id}",
            "update relationship",
            exc,
        )

    return redirect_with_message("/ui/relationships", success="Relationship updated.")


@app.post("/ui/relationships/{relationship_id}/delete")
def delete_relationship(relationship_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute("DELETE FROM people_relationships WHERE id = %s", (relationship_id,))
    except psycopg.Error as exc:
        return handle_db_error("/ui/relationships", "delete relationship", exc)

    return redirect_with_message("/ui/relationships", success="Relationship deleted.")
