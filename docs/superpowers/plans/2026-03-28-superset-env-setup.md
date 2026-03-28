# Superset Env Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatycznie kopiowac `.env` z glownego worktree do nowo tworzonego workspace Superset.

**Architecture:** Repo dostaje `.superset/config.json`, ktory uruchamia `.superset/setup.sh` przy tworzeniu workspace. Skrypt korzysta z `SUPERSET_ROOT_PATH` i `SUPERSET_WORKSPACE_PATH`, waliduje obecność zrodlowego `.env`, a test pytest sprawdza scenariusz nadpisania i scenariusz bledu.

**Tech Stack:** Superset setup scripts, POSIX shell, pytest

---

### Task 1: Add a failing integration test for setup script behavior

**Files:**
- Create: `api/tests/test_superset_setup.py`
- Test: `api/tests/test_superset_setup.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import os
import subprocess
import sys


SCRIPT_PATH = Path(__file__).resolve().parents[2] / ".superset" / "setup.sh"


def test_setup_script_overwrites_workspace_env(tmp_path: Path) -> None:
    root_path = tmp_path / "root"
    workspace_path = tmp_path / "workspace"
    root_path.mkdir()
    workspace_path.mkdir()
    (root_path / ".env").write_text("API_KEY=from-root\n")
    (workspace_path / ".env").write_text("API_KEY=stale\n")

    result = subprocess.run(
        ["/bin/sh", str(SCRIPT_PATH)],
        cwd=workspace_path,
        env={
            **os.environ,
            "SUPERSET_ROOT_PATH": str(root_path),
            "SUPERSET_WORKSPACE_PATH": str(workspace_path),
        },
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (workspace_path / ".env").read_text() == "API_KEY=from-root\n"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=api python3 -m pytest api/tests/test_superset_setup.py -q`
Expected: FAIL because `.superset/setup.sh` does not exist yet.

### Task 2: Implement Superset setup config and script

**Files:**
- Create: `.superset/config.json`
- Create: `.superset/setup.sh`
- Modify: `README.md`
- Test: `api/tests/test_superset_setup.py`

- [ ] **Step 1: Write minimal implementation**

```json
{
  "setup": ["./.superset/setup.sh"]
}
```

```sh
#!/bin/sh
set -eu

source_env_path="${SUPERSET_ROOT_PATH}/.env"
target_env_path="${SUPERSET_WORKSPACE_PATH}/.env"

if [ ! -f "$source_env_path" ]; then
  printf 'Missing source env: %s\n' "$source_env_path" >&2
  exit 1
fi

cp -f "$source_env_path" "$target_env_path"
printf 'Copied %s -> %s\n' "$source_env_path" "$target_env_path"
```

- [ ] **Step 2: Run test to verify it passes**

Run: `PYTHONPATH=api python3 -m pytest api/tests/test_superset_setup.py -q`
Expected: PASS

- [ ] **Step 3: Document the behavior**

Add a short README note explaining that Superset workspace creation automatically copies `.env` from the main worktree and overwrites the workspace-local file.

### Task 3: Add missing-source error coverage

**Files:**
- Modify: `api/tests/test_superset_setup.py`
- Test: `api/tests/test_superset_setup.py`

- [ ] **Step 1: Write the failing test**

```python
def test_setup_script_fails_when_root_env_is_missing(tmp_path: Path) -> None:
    root_path = tmp_path / "root"
    workspace_path = tmp_path / "workspace"
    root_path.mkdir()
    workspace_path.mkdir()

    result = subprocess.run(
        ["/bin/sh", str(SCRIPT_PATH)],
        cwd=workspace_path,
        env={
            **os.environ,
            "SUPERSET_ROOT_PATH": str(root_path),
            "SUPERSET_WORKSPACE_PATH": str(workspace_path),
        },
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Missing source env" in result.stderr
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=api python3 -m pytest api/tests/test_superset_setup.py -q`
Expected: FAIL until the script validates missing source `.env`.

- [ ] **Step 3: Update implementation if needed**

```sh
if [ ! -f "$source_env_path" ]; then
  printf 'Missing source env: %s\n' "$source_env_path" >&2
  exit 1
fi
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=api python3 -m pytest api/tests/test_superset_setup.py -q`
Expected: PASS
