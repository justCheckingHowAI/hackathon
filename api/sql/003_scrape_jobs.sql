CREATE TABLE scrape_jobs (
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
);

CREATE INDEX idx_scrape_jobs_status_created_at ON scrape_jobs (status, created_at DESC);
CREATE INDEX idx_scrape_jobs_provider_repo ON scrape_jobs (provider, repo, created_at DESC);
