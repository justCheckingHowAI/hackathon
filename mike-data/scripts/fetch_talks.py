#!/usr/bin/env python3
"""Search and download Mike Grabowski's conference talks from YouTube."""
import subprocess, os, json, re, glob

YTDLP = "/opt/homebrew/bin/yt-dlp"
OUTPUT_DIR = "teamtwin/raw/talks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SEARCH_QUERIES = [
    "Mike Grabowski React Summit",
    "Mike Grabowski React Native EU",
    "Mike Grabowski Chain React conference",
    "Mike Grabowski App.js conf",
    "Mike Grabowski callstack talk",
    "grabbou conference react native",
    "Mike Grabowski module federation react native repack",
    "Mike Grabowski react native CLI",
    "React Native Show podcast callstack Mike",
]

# 5.1 Search
all_results = []
seen_urls = set()

for query in SEARCH_QUERIES:
    print(f"Searching: {query}")
    result = subprocess.run(
        [YTDLP, "--flat-playlist", f"ytsearch5:{query}",
         "--print", "%(title)s|||%(url)s|||%(duration_string)s|||%(upload_date)s"],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("|||")
        if len(parts) >= 2 and parts[1] not in seen_urls:
            seen_urls.add(parts[1])
            entry = {
                "title": parts[0],
                "url": parts[1],
                "duration": parts[2] if len(parts) > 2 else "",
                "date": parts[3] if len(parts) > 3 else "",
                "search_query": query,
            }
            all_results.append(entry)
            print(f"  Found: {parts[0][:80]}")

with open(f"{OUTPUT_DIR}/talks-index.json", "w") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f"\nTotal unique results: {len(all_results)}")

# 5.2 Download transcripts for relevant talks
relevant_talks = [t for t in all_results if any(kw in t["title"].lower()
    for kw in ["grabowski", "callstack", "repack", "grabbou", "react native show"])]

if len(relevant_talks) < 3:
    relevant_talks = all_results[:8]
else:
    relevant_talks = relevant_talks[:8]

print(f"\nDownloading transcripts for {len(relevant_talks)} talks...")

for i, talk in enumerate(relevant_talks):
    print(f"\n[{i+1}/{len(relevant_talks)}] {talk['title'][:70]}")
    safe_title = re.sub(r'[^\w\s-]', '', talk["title"])[:60].strip()
    safe_title = re.sub(r'\s+', '-', safe_title)

    subprocess.run([
        YTDLP, "--write-auto-subs", "--sub-langs", "en",
        "--convert-subs", "srt", "--skip-download",
        "-o", f"{OUTPUT_DIR}/{safe_title}", talk["url"]
    ], timeout=60, capture_output=True)

# 5.3 Clean SRT to plain text
print("\nCleaning SRT files...")
for srt_file in glob.glob(f"{OUTPUT_DIR}/*.srt"):
    with open(srt_file) as f:
        content = f.read()
    lines = content.split("\n")
    text_lines = []
    prev = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d+$', line):
            continue
        if re.match(r'\d{2}:\d{2}:\d{2}', line):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        if line and line != prev:
            text_lines.append(line)
        prev = line
    output_file = srt_file.replace(".srt", ".txt")
    with open(output_file, "w") as f:
        f.write("\n".join(text_lines))
    print(f"Cleaned: {os.path.basename(srt_file)} -> {len(text_lines)} lines")

print("\nDone!")
