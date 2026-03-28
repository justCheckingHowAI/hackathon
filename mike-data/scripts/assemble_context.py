#!/usr/bin/env python3
"""Assemble all collected data into a single context file."""
import json, os, glob

OUTPUT_FILE = "teamtwin/processed/full-context.md"
sections = []

sections.append("# TeamTwin Knowledge Base - Mike Grabowski (@grabbou)")
sections.append("## CTO & Co-Founder, Callstack | React Native Core Team\n")
sections.append("---\n")

# 1. GITHUB PROFILE
profile_path = "teamtwin/raw/github/profile.json"
if os.path.exists(profile_path):
    with open(profile_path) as f:
        profile = json.load(f)
    sections.append("## GITHUB PROFILE\n")
    sections.append(json.dumps(profile, indent=2))
    sections.append("\n---\n")

# 2. PULL REQUESTS
prs_path = "teamtwin/raw/github/prs-authored.json"
if os.path.exists(prs_path):
    with open(prs_path) as f:
        prs = json.load(f)
    sections.append(f"## PULL REQUESTS AUTHORED ({len(prs)} total)\n")
    for pr in prs[:30]:
        sections.append(f"### PR: {pr.get('title', 'Unknown')}")
        sections.append(f"Repo: {pr.get('repo', '?')} | State: {pr.get('state', '?')} | URL: {pr.get('url', '')}")
        body = pr.get('body', '') or ''
        if body:
            sections.append(f"Description: {body[:600]}")
        for c in pr.get('comments', [])[:3]:
            sections.append(f"  Comment by @{c.get('author', '?')}: {c.get('body', '')[:250]}")
        for rc in pr.get('review_comments', [])[:2]:
            sections.append(f"  Review on {rc.get('path', '?')}: {rc.get('body', '')[:250]}")
        sections.append("")
    sections.append("---\n")

# 3. CODE REVIEWS
reviews_path = "teamtwin/raw/github/reviews.json"
if os.path.exists(reviews_path):
    with open(reviews_path) as f:
        reviews = json.load(f)
    sections.append(f"## CODE REVIEWS ({len(reviews)} PRs reviewed)\n")
    for review in reviews[:20]:
        sections.append(f"### Reviewed: {review.get('pr_title', '?')} by @{review.get('pr_author', '?')}")
        for c in review.get('review_comments', [])[:3]:
            sections.append(f"  Mike's comment: {c.get('body', '')[:300]}")
        sections.append("")
    sections.append("---\n")

# 4. ISSUES
issues_path = "teamtwin/raw/github/issues.json"
if os.path.exists(issues_path):
    with open(issues_path) as f:
        issues = json.load(f)
    sections.append(f"## ISSUES ({len(issues)} total)\n")
    for issue in issues[:20]:
        sections.append(f"### {issue.get('title', '?')}")
        body = issue.get('body', '') or ''
        if body:
            sections.append(f"Description: {body[:400]}")
        for c in issue.get('comments', issue.get('comments_by_target', []))[:2]:
            sections.append(f"  Comment: {c.get('body', '')[:250]}")
        sections.append("")
    sections.append("---\n")

# 5. REACTIFLUX Q&A
qa_path = "teamtwin/raw/written/reactiflux-qa.md"
if os.path.exists(qa_path):
    with open(qa_path) as f:
        content = f.read()
    sections.append("## REACTIFLUX Q&A - DEEP INTERVIEW ABOUT REACT NATIVE CORE\n")
    sections.append(content[:10000])
    sections.append("\n---\n")

# 6. CONFERENCE TALKS
talk_files = sorted(glob.glob("teamtwin/raw/talks/*.txt"))
if talk_files:
    sections.append(f"## CONFERENCE TALKS ({len(talk_files)} transcripts)\n")
    for txt_file in talk_files[:5]:
        with open(txt_file) as f:
            content = f.read()
        sections.append(f"### Talk: {os.path.basename(txt_file)}\n")
        sections.append(content[:5000])
        sections.append("\n---\n")

# 7. PODCAST EPISODES
podcast_files = sorted(glob.glob("teamtwin/raw/podcast/*.txt"))
if podcast_files:
    sections.append(f"## PODCAST EPISODES ({len(podcast_files)} transcripts)\n")
    for txt_file in podcast_files[:3]:
        with open(txt_file) as f:
            content = f.read()
        sections.append(f"### Episode: {os.path.basename(txt_file)}\n")
        sections.append(content[:4000])
        sections.append("\n---\n")

# 8. DOCUMENTATION
doc_files = sorted(glob.glob("teamtwin/raw/docs/*.md"))
if doc_files:
    sections.append(f"## TECHNICAL DOCUMENTATION ({len(doc_files)} docs)\n")
    for doc_file in doc_files:
        with open(doc_file) as f:
            content = f.read()
        if len(content) > 200:
            sections.append(f"### {os.path.basename(doc_file)}\n")
            sections.append(content[:3000])
            sections.append("\n---\n")

# 9. WRITTEN CONTENT
for written_file in sorted(glob.glob("teamtwin/raw/written/*.md")):
    if "reactiflux" not in written_file:
        with open(written_file) as f:
            content = f.read()
        if len(content) > 200:
            sections.append(f"### Written: {os.path.basename(written_file)}\n")
            sections.append(content[:3000])
            sections.append("\n---\n")

# 10. SYNTHETIC DATA
sections.append("## INTERNAL DATA (Synthetic - Jira, Slack, 1:1 Notes)\n")

jira_path = "teamtwin/raw/synthetic/jira-tickets.json"
if os.path.exists(jira_path):
    with open(jira_path) as f:
        tickets = json.load(f)
    sections.append("### Jira Tickets\n")
    sections.append(json.dumps(tickets, indent=2, ensure_ascii=False)[:15000])
    sections.append("\n")

notes_path = "teamtwin/raw/synthetic/1on1-notes.md"
if os.path.exists(notes_path):
    with open(notes_path) as f:
        sections.append("### 1:1 Notes\n")
        sections.append(f.read())
        sections.append("\n")

slack_path = "teamtwin/raw/synthetic/slack-threads.json"
if os.path.exists(slack_path):
    with open(slack_path) as f:
        threads = json.load(f)
    sections.append("### Slack Threads\n")
    sections.append(json.dumps(threads, indent=2, ensure_ascii=False)[:15000])

# ASSEMBLE
full_context = "\n".join(sections)
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    f.write(full_context)

char_count = len(full_context)
word_count = len(full_context.split())
estimated_tokens = char_count // 4

print(f"\n{'='*50}")
print(f"CONTEXT ASSEMBLY COMPLETE")
print(f"{'='*50}")
print(f"Characters:      {char_count:,}")
print(f"Words:           {word_count:,}")
print(f"Estimated tokens: {estimated_tokens:,}")
print(f"Gemini 2M usage: {estimated_tokens/2_000_000*100:.1f}%")
print(f"Output:          {OUTPUT_FILE}")
print(f"{'='*50}")

if estimated_tokens > 1_500_000:
    print("WARNING: Approaching context limit. Consider trimming transcripts.")
elif estimated_tokens < 50_000:
    print("INFO: Context is small. Consider adding more data sources.")
