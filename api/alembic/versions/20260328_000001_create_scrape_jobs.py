from __future__ import annotations

from alembic import op


revision = "20260328_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS scrape_jobs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            provider TEXT NOT NULL,
            repo TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'queued',
            step TEXT,
            progress_current INTEGER NOT NULL DEFAULT 0,
            progress_total INTEGER NOT NULL DEFAULT 0,
            message TEXT,
            output_dir TEXT,
            error TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            started_at TIMESTAMPTZ,
            finished_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_scrape_jobs_status_created_at ON scrape_jobs (status, created_at DESC)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_scrape_jobs_provider_repo ON scrape_jobs (provider, repo, created_at DESC)"
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS scrape_jobs")
