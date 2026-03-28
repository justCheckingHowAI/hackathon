#!/usr/bin/env python3
"""Generate data collection report."""
import os, json, glob

report = []
report.append("# TeamTwin Data Collection Report")
report.append(f"## Target: Mike Grabowski (@grabbou)\n")

checks = []

def check(category, name, path_pattern, min_count=1):
    if path_pattern.endswith('.json'):
        if os.path.exists(path_pattern):
            with open(path_pattern) as f:
                try:
                    data = json.load(f)
                    count = len(data) if isinstance(data, list) else 1
                except:
                    count = 0
            status = "PASS" if count >= min_count else "LOW"
            checks.append((status, category, name, count))
        else:
            checks.append(("MISSING", category, name, 0))
    else:
        files = glob.glob(path_pattern)
        count = len(files)
        status = "PASS" if count >= min_count else ("LOW" if count > 0 else "MISSING")
        checks.append((status, category, name, count))

check("GitHub", "PRs authored", "teamtwin/raw/github/prs-authored.json", 15)
check("GitHub", "Code reviews", "teamtwin/raw/github/reviews.json", 5)
check("GitHub", "Issues", "teamtwin/raw/github/issues.json", 5)
check("GitHub", "Commits", "teamtwin/raw/github/commits.json", 10)
check("GitHub", "Profile", "teamtwin/raw/github/profile.json", 1)

check("Written", "Reactiflux Q&A", "teamtwin/raw/written/reactiflux-qa.md", 1)
check("Written", "Other articles", "teamtwin/raw/written/*.md", 1)

check("Talks", "Talk transcripts", "teamtwin/raw/talks/*.txt", 2)
check("Talks", "Talk index", "teamtwin/raw/talks/talks-index.json", 1)

check("Podcast", "Podcast transcripts", "teamtwin/raw/podcast/*.txt", 1)

check("Docs", "Technical docs", "teamtwin/raw/docs/*.md", 4)

check("Synthetic", "Jira tickets", "teamtwin/raw/synthetic/jira-tickets.json", 5)
check("Synthetic", "1:1 Notes", "teamtwin/raw/synthetic/1on1-notes.md", 1)
check("Synthetic", "Slack threads", "teamtwin/raw/synthetic/slack-threads.json", 5)

check("Output", "Full context", "teamtwin/processed/full-context.md", 1)

report.append("## Data Collection Status\n")
report.append("| Status | Category | Source | Count |")
report.append("|--------|----------|--------|-------|")

for status, category, name, count in checks:
    report.append(f"| {status} | {category} | {name} | {count} |")

passed = sum(1 for s, _, _, _ in checks if s == "PASS")
total = len(checks)
report.append(f"\n**{passed}/{total} checks passed**\n")

missing = [(c, n) for s, c, n, _ in checks if s == "MISSING"]
if missing:
    report.append("### Missing Data (action required):\n")
    for cat, name in missing:
        report.append(f"- {cat}: {name}")

ctx_path = "teamtwin/processed/full-context.md"
if os.path.exists(ctx_path):
    size = os.path.getsize(ctx_path)
    estimated_tokens = size // 4
    report.append(f"\n### Context Size")
    report.append(f"- File size: {size:,} bytes")
    report.append(f"- Estimated tokens: {estimated_tokens:,}")
    report.append(f"- Gemini 2M context usage: {estimated_tokens/2_000_000*100:.1f}%")

report_text = "\n".join(report)
with open("teamtwin/processed/data-report.md", "w") as f:
    f.write(report_text)

print(report_text)
