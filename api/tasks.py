from __future__ import annotations

from github_graph_exporter import GitHubGraphExportError, export_repo_graph
from scrape_jobs import ScrapeProgressUpdate, update_scrape_job
from taskiq_broker import broker


@broker.task
async def scrape_github_repo_task(job_id: str, repo: str) -> None:
    update_scrape_job(
        job_id,
        ScrapeProgressUpdate(
            status="running",
            step="starting",
            progress_current=0,
            progress_total=4,
            message=f"Starting scrape for {repo}",
            started=True,
        ),
    )

    def report_progress(step: str, current: int, total: int, message: str) -> None:
        update_scrape_job(
            job_id,
            ScrapeProgressUpdate(
                status="running",
                step=step,
                progress_current=current,
                progress_total=total,
                message=message,
                started=True,
            ),
        )

    try:
        result = export_repo_graph(repo, progress_callback=report_progress)
    except GitHubGraphExportError as exc:
        update_scrape_job(
            job_id,
            ScrapeProgressUpdate(
                status="failed",
                step="failed",
                progress_current=4,
                progress_total=4,
                message="GitHub export failed",
                error=str(exc),
                started=True,
                finished=True,
            ),
        )
        raise
    except Exception as exc:
        update_scrape_job(
            job_id,
            ScrapeProgressUpdate(
                status="failed",
                step="failed",
                progress_current=4,
                progress_total=4,
                message="Unexpected scraper failure",
                error=str(exc),
                started=True,
                finished=True,
            ),
        )
        raise

    update_scrape_job(
        job_id,
        ScrapeProgressUpdate(
            status="completed",
            step="completed",
            progress_current=4,
            progress_total=4,
            message=(
                f"Done: {result['prs']} PRs, {result['commits']} commits, "
                f"{result['authors']} authors"
            ),
            output_dir=result["output_dir"],
            started=True,
            finished=True,
        ),
    )
