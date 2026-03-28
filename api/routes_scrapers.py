from __future__ import annotations

import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from scrape_jobs import create_scrape_job, get_scrape_job, list_scrape_jobs
from tasks import scrape_github_repo_task


REPO_PATTERN = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')

router = APIRouter(prefix='/scrapers', tags=['scrapers'])


class GitHubRepoScrapeRequest(BaseModel):
    repo: str


def validate_repo(repo: str) -> str:
    normalized = repo.strip()
    if not REPO_PATTERN.match(normalized):
        raise HTTPException(status_code=422, detail='Repo must use owner/repo format.')
    return normalized


@router.post('/github/repo')
async def start_github_repo_scrape(payload: GitHubRepoScrapeRequest) -> dict[str, str]:
    normalized_repo = validate_repo(payload.repo)
    job = create_scrape_job(normalized_repo)
    job_id = job.get('id')
    if not job_id:
        raise HTTPException(status_code=500, detail='Unable to create scrape job.')

    await scrape_github_repo_task.kiq(job_id, normalized_repo)
    return {
        'job_id': job_id,
        'repo': normalized_repo,
        'status': 'queued',
        'status_url': f'/scrapers/jobs/{job_id}',
    }


@router.get('/jobs')
def get_scraper_jobs() -> list[dict[str, str | int | None]]:
    return list_scrape_jobs(limit=100)


@router.get('/jobs/{job_id}')
def get_scraper_job(job_id: str) -> dict[str, str | int | None]:
    job = get_scrape_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail='Scrape job not found.')
    return job
