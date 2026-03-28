#!/usr/bin/env python3
"""Find and download React Native Show podcast episodes."""
import subprocess, os, json, re, glob

YTDLP = "/opt/homebrew/bin/yt-dlp"
OUTPUT_DIR = "teamtwin/raw/podcast"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 6.1 Find episodes
result = subprocess.run(
    [YTDLP, "--flat-playlist", "ytsearch20:React Native Show podcast callstack",
     "--print", "%(title)s|||%(url)s|||%(duration_string)s|||%(upload_date)s"],
    capture_output=True, text=True, timeout=60
)

episodes = []
for line in result.stdout.strip().split("\n"):
    if not line.strip():
        continue
    parts = line.split("|||")
    if len(parts) >= 2:
        episodes.append({
            "title": parts[0],
            "url": parts[1],
            "duration": parts[2] if len(parts) > 2 else "",
            "date": parts[3] if len(parts) > 3 else "",
        })

with open(f"{OUTPUT_DIR}/podcast-index.json", "w") as f:
    json.dump(episodes, f, indent=2, ensure_ascii=False)

print(f"Found {len(episodes)} podcast episodes")
for ep in episodes[:10]:
    print(f"  {ep['title'][:70]}")

# 6.2 Download transcripts for top 5
selected = episodes[:5]
print(f"\nDownloading transcripts for {len(selected)} episodes...")

for i, ep in enumerate(selected):
    print(f"[{i+1}/{len(selected)}] {ep['title'][:70]}")
    safe_title = re.sub(r'[^\w\s-]', '', ep["title"])[:60].strip()
    safe_title = re.sub(r'\s+', '-', safe_title)

    subprocess.run([
        YTDLP, "--write-auto-subs", "--sub-langs", "en",
        "--convert-subs", "srt", "--skip-download",
        "-o", f"{OUTPUT_DIR}/{safe_title}", ep["url"]
    ], timeout=60, capture_output=True)

# Clean SRT to text
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
