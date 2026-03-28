#!/usr/bin/env python3
"""Fetch commits by grabbou."""
import subprocess, json, time

REPOS = [
    "facebook/react-native", "react-native-community/cli", "callstack/repack",
    "callstack/react-native-paper", "callstack/haul", "callstack/super-app-example",
    "rnpm/rnpm", "rnpm/rnpm-plugin-link", "react-native-community/releases",
    "callstackincubator/ai",
]

all_commits = []

for repo in REPOS:
    print(f"Fetching commits from {repo}...")
    result = subprocess.run(
        ["gh", "search", "commits", "--author=grabbou", f"--repo={repo}", "--limit=30",
         "--json", "sha,commit", "--sort=committer-date", "--order=desc"],
        capture_output=True, text=True
    )
    try:
        commits = json.loads(result.stdout) if result.stdout.strip() else []
    except:
        commits = []

    for c in commits:
        c["repo"] = repo

    all_commits.extend(commits)
    print(f"  {repo}: {len(commits)} commits")
    time.sleep(1)

with open("teamtwin/raw/github/commits.json", "w") as f:
    json.dump(all_commits, f, indent=2, ensure_ascii=False)

print(f"\nTotal: {len(all_commits)} commits saved")
