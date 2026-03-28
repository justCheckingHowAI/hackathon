from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from db import Database, get_database


@dataclass(slots=True)
class ScrapeProgressUpdate:
    status: str
    step: str | None = None
    progress_current: int | None = None
    progress_total: int | None = None
    message: str | None = None
    output_dir: str | None = None
    error: str | None = None
    started: bool = False
    finished: bool = False


def create_scrape_job(repo: str, provider: str = "github", db: Database | None = None) -> dict[str, Any]:
    database = db or get_database()
    return database.fetch_one(
        """
        INSERT INTO scrape_jobs (provider, repo, status, step, message)
        VALUES (%s, %s, 'queued', 'queued', 'Job queued')
        RETURNING
            id::text,
            provider,
            repo,
            status,
            step,
            progress_current,
            progress_total,
            message,
            output_dir,
            error,
            created_at::text,
            started_at::text,
            finished_at::text
        """,
        (provider, repo),
    ) or {}


def get_scrape_job(job_id: str, db: Database | None = None) -> dict[str, Any] | None:
    database = db or get_database()
    return database.fetch_one(
        """
        SELECT
            id::text,
            provider,
            repo,
            status,
            step,
            progress_current,
            progress_total,
            message,
            output_dir,
            error,
            created_at::text,
            started_at::text,
            finished_at::text
        FROM scrape_jobs
        WHERE id = %s::uuid
        """,
        (job_id,),
    )


def list_scrape_jobs(limit: int = 50, db: Database | None = None) -> list[dict[str, Any]]:
    database = db or get_database()
    return database.fetch_all(
        """
        SELECT
            id::text,
            provider,
            repo,
            status,
            step,
            progress_current,
            progress_total,
            message,
            output_dir,
            error,
            created_at::text,
            started_at::text,
            finished_at::text
        FROM scrape_jobs
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (limit,),
    )


def update_scrape_job(job_id: str, update: ScrapeProgressUpdate, db: Database | None = None) -> None:
    database = db or get_database()
    database.execute(
        """
        UPDATE scrape_jobs
        SET
            status = %s,
            step = COALESCE(%s, step),
            progress_current = COALESCE(%s, progress_current),
            progress_total = COALESCE(%s, progress_total),
            message = COALESCE(%s, message),
            output_dir = COALESCE(%s, output_dir),
            error = %s,
            started_at = CASE
                WHEN %s THEN COALESCE(started_at, NOW())
                ELSE started_at
            END,
            finished_at = CASE
                WHEN %s THEN NOW()
                ELSE finished_at
            END
        WHERE id = %s::uuid
        """,
        (
            update.status,
            update.step,
            update.progress_current,
            update.progress_total,
            update.message,
            update.output_dir,
            update.error,
            update.started,
            update.finished,
            job_id,
        ),
    )
