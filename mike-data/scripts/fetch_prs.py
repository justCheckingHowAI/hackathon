#!/usr/bin/env python3
"""Fetch PRs authored by grabbou from key repos."""
import subprocess, json, time, sys

REPOS = [
    "facebook/react-native", "react-native-community/cli", "callstack/repack",
    "callstack/react-native-paper", "callstack/haul", "callstack/super-app-example",
    "rnpm/rnpm", "rnpm/rnpm-plugin-link", "react-native-community/releases",
    "callstackincubator/ai",
]

all_prs = []

for repo in REPOS:
    print(f"Fetching PRs from {repo}...")
    result = subprocess.run(
        ["gh", "search", "prs", "--author=grabbou", f"--repo={repo}", "--limit=30",
         "--json", "number,title,url,body,createdAt,state"],
        capture_output=True, text=True
    )
    try:
        prs = json.loads(result.stdout) if result.stdout.strip() else []
    except json.JSONDecodeError:
        prs = []

    owner, name = repo.split("/")
    for pr in prs:
        pr["repo"] = repo
        num = pr["number"]

        # Fetch PR comments
        time.sleep(1)
        cr = subprocess.run(
            ["gh", "api", f"repos/{owner}/{name}/pulls/{num}/comments", "--paginate"],
            capture_output=True, text=True
        )
        try:
            comments = json.loads(cr.stdout) if cr.stdout.strip() else []
            pr["review_comments"] = [{"author": c["user"]["login"], "body": c["body"][:500], "path": c.get("path","")} for c in comments[:5]]
        except:
            pr["review_comments"] = []

        # Fetch issue comments
        time.sleep(1)
        ic = subprocess.run(
            ["gh", "api", f"repos/{owner}/{name}/issues/{num}/comments", "--paginate"],
            capture_output=True, text=True
        )
        try:
            icomments = json.loads(ic.stdout) if ic.stdout.strip() else []
            pr["comments"] = [{"author": c["user"]["login"], "body": c["body"][:500]} for c in icomments[:5]]
        except:
            pr["comments"] = []

    all_prs.extend(prs)
    print(f"  {repo}: {len(prs)} PRs")
    time.sleep(1)

with open("teamtwin/raw/github/prs-authored.json", "w") as f:
    json.dump(all_prs, f, indent=2, ensure_ascii=False)

print(f"\nTotal: {len(all_prs)} PRs saved")
