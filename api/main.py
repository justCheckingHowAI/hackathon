from __future__ import annotations

import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from db import DatabaseConfigError, get_database
from scrape_jobs import create_scrape_job, get_scrape_job, list_scrape_jobs
from taskiq_broker import broker
from tasks import scrape_github_repo_task


REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(_: FastAPI):
    await broker.startup()
    try:
        yield
    finally:
        await broker.shutdown()


app = FastAPI(title="API", lifespan=lifespan)


class GitHubRepoScrapeRequest(BaseModel):
    repo: str


def validate_repo(repo: str) -> str:
    normalized = repo.strip()
    if not REPO_PATTERN.match(normalized):
        raise HTTPException(status_code=422, detail="Repo must use owner/repo format.")
    return normalized


async def enqueue_scrape_job(repo: str) -> dict[str, str]:
    normalized_repo = validate_repo(repo)
    job = create_scrape_job(normalized_repo)
    job_id = job.get("id")
    if not job_id:
        raise HTTPException(status_code=500, detail="Unable to create scrape job.")

    await scrape_github_repo_task.kiq(job_id, normalized_repo)
    return {
        "job_id": job_id,
        "repo": normalized_repo,
        "status": "queued",
        "status_url": f"/scrapers/jobs/{job_id}",
    }


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


@app.get("/scrapers", response_class=HTMLResponse)
def scrapers_dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="scrapers.html",
        context={"jobs": list_scrape_jobs(limit=100)},
    )


@app.post("/scrapers/github/repo")
async def start_github_repo_scrape(payload: GitHubRepoScrapeRequest) -> dict[str, str]:
    return await enqueue_scrape_job(payload.repo)


@app.post("/scrapers/github/repo/form")
async def start_github_repo_scrape_form(repo: str = Form(...)) -> RedirectResponse:
    await enqueue_scrape_job(repo)
    return RedirectResponse(url="/scrapers", status_code=303)


@app.get("/scrapers/jobs")
def get_scraper_jobs() -> list[dict[str, str | int | None]]:
    return list_scrape_jobs(limit=100)


@app.get("/scrapers/jobs/{job_id}")
def get_scraper_job(job_id: str) -> dict[str, str | int | None]:
    job = get_scrape_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Scrape job not found.")
    return job


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
