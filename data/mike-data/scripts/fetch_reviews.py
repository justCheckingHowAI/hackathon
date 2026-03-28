#!/usr/bin/env python3
"""Fetch code reviews by grabbou on other people's PRs."""
import subprocess, json, time

REPOS = ["facebook/react-native", "react-native-community/cli", "callstack/repack"]
all_reviews = []

for repo in REPOS:
    print(f"Fetching reviews from {repo}...")
    result = subprocess.run(
        ["gh", "search", "prs", "--commenter=grabbou", f"--repo={repo}", "--limit=20",
         "--json", "number,title,url,author,createdAt"],
        capture_output=True, text=True
    )
    try:
        prs = json.loads(result.stdout) if result.stdout.strip() else []
    except:
        prs = []

    owner, name = repo.split("/")
    for pr in prs:
        num = pr["number"]
        time.sleep(1)
        cr = subprocess.run(
            ["gh", "api", f"repos/{owner}/{name}/pulls/{num}/comments", "--paginate"],
            capture_output=True, text=True
        )
        try:
            comments = json.loads(cr.stdout) if cr.stdout.strip() else []
            grabbou_comments = [{"body": c["body"][:500], "path": c.get("path","")}
                               for c in comments if c["user"]["login"] == "grabbou"]
        except:
            grabbou_comments = []

        if grabbou_comments:
            all_reviews.append({
                "repo": repo,
                "pr_number": num,
                "pr_title": pr["title"],
                "pr_author": pr.get("author", {}).get("login", "?") if isinstance(pr.get("author"), dict) else str(pr.get("author", "?")),
                "review_comments": grabbou_comments[:5]
            })

    print(f"  {repo}: {len([r for r in all_reviews if r['repo']==repo])} reviews with grabbou comments")
    time.sleep(1)

with open("teamtwin/raw/github/reviews.json", "w") as f:
    json.dump(all_reviews, f, indent=2, ensure_ascii=False)

print(f"\nTotal: {len(all_reviews)} reviews saved")
