#!/usr/bin/env python3
"""Fetch technical documentation."""
import subprocess, os

OUTPUT_DIR = "teamtwin/raw/docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOCS = {
    "rn-getting-started": "https://raw.githubusercontent.com/facebook/react-native-website/main/docs/getting-started.md",
    "rn-native-modules-intro": "https://raw.githubusercontent.com/facebook/react-native-website/main/docs/native-modules-intro.md",
    "rn-new-architecture-intro": "https://raw.githubusercontent.com/facebook/react-native-website/main/docs/the-new-architecture/landing-page.md",
    "rn-turbo-modules": "https://raw.githubusercontent.com/facebook/react-native-website/main/docs/the-new-architecture/pillars-turbomodules.md",
    "cli-readme": "https://raw.githubusercontent.com/react-native-community/cli/main/README.md",
    "cli-autolinking": "https://raw.githubusercontent.com/react-native-community/cli/main/docs/autolinking.md",
    "cli-configuration": "https://raw.githubusercontent.com/react-native-community/cli/main/docs/configuration.md",
    "cli-init": "https://raw.githubusercontent.com/react-native-community/cli/main/docs/init.md",
    "repack-readme": "https://raw.githubusercontent.com/callstack/repack/main/README.md",
    "paper-readme": "https://raw.githubusercontent.com/callstack/react-native-paper/main/README.md",
    "rnpm-readme": "https://raw.githubusercontent.com/rnpm/rnpm/master/README.md",
    "super-app-readme": "https://raw.githubusercontent.com/callstack/super-app-example/main/README.md",
    "ai-readme": "https://raw.githubusercontent.com/callstackincubator/ai/main/README.md",
    "callstack-os": "https://www.callstack.com/open-source",
}

for name, url in DOCS.items():
    print(f"Fetching {name}...")
    subprocess.run(["curl", "-sL", url, "-o", f"{OUTPUT_DIR}/{name}.md"],
                   capture_output=True, text=True)
    filepath = f"{OUTPUT_DIR}/{name}.md"
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size < 100:
            print(f"  WARNING: {name} is only {size} bytes")
        else:
            print(f"  OK: {size} bytes")
    else:
        print(f"  FAILED: file not created")
