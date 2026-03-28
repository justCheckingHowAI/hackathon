# GitHub Graph Export

This folder contains a small exporter that scrapes one public GitHub repository and writes graph-friendly CSV files.

## What it exports

- `raw/prs.json` - full pull request payloads from GitHub
- `raw/commits.json` - full commit payloads from GitHub
- `csv/authors.csv` - unique authors normalized across PRs and commits
- `csv/commits.csv` - commit nodes
- `csv/prs.csv` - pull request nodes
- `csv/edges.csv` - graph edges linking authors, PRs, and commits
- `summary.json` - quick counts for sanity checks

## Usage

```bash
python data/github-graph/scripts/export_repo_graph.py owner/repo
```

Optional custom output path:

```bash
python data/github-graph/scripts/export_repo_graph.py owner/repo --output-dir data/github-graph/outputs/custom
```

The script uses `gh api`, so make sure GitHub CLI is installed and authenticated.
