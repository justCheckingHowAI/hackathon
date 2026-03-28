#!/usr/bin/env python3
"""Fetch issues authored/commented by grabbou."""
import subprocess, json, time

AUTHOR_REPOS = ["facebook/react-native", "react-native-community/cli", "callstack/repack"]
all_issues = []
seen = set()

# Issues authored by grabbou
for repo in AUTHOR_REPOS:
    print(f"Fetching authored issues from {repo}...")
    result = subprocess.run(
        ["gh", "search", "issues", "--author=grabbou", f"--repo={repo}", "--limit=20",
         "--json", "number,title,url,body,createdAt,state,labels"],
        capture_output=True, text=True
    )
    try:
        issues = json.loads(result.stdout) if result.stdout.strip() else []
    except:
        issues = []

    for issue in issues:
        key = f"{repo}#{issue['number']}"
        if key not in seen:
            seen.add(key)
            issue["repo"] = repo
            issue["role"] = "author"
            all_issues.append(issue)

    print(f"  {repo}: {len(issues)} authored issues")
    time.sleep(1)

# Issues commented by grabbou (facebook/react-native only)
print("Fetching commented issues from facebook/react-native...")
result = subprocess.run(
    ["gh", "search", "issues", "--commenter=grabbou", "--repo=facebook/react-native", "--limit=15",
     "--json", "number,title,url,body,createdAt,state,labels"],
    capture_output=True, text=True
)
try:
    issues = json.loads(result.stdout) if result.stdout.strip() else []
except:
    issues = []

for issue in issues:
    key = f"facebook/react-native#{issue['number']}"
    if key not in seen:
        seen.add(key)
        issue["repo"] = "facebook/react-native"
        issue["role"] = "commenter"

        # Fetch grabbou's comments
        time.sleep(1)
        cr = subprocess.run(
            ["gh", "api", f"repos/facebook/react-native/issues/{issue['number']}/comments", "--paginate"],
            capture_output=True, text=True
        )
        try:
            comments = json.loads(cr.stdout) if cr.stdout.strip() else []
            issue["comments_by_target"] = [{"body": c["body"][:500]}
                                           for c in comments if c["user"]["login"] == "grabbou"]
        except:
            issue["comments_by_target"] = []

        all_issues.append(issue)

print(f"  commented: {len(issues)} issues")

with open("teamtwin/raw/github/issues.json", "w") as f:
    json.dump(all_issues, f, indent=2, ensure_ascii=False)

print(f"\nTotal: {len(all_issues)} issues saved")
