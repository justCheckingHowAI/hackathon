import os
import shlex
import subprocess
import time
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[2] / ".superset" / "setup.sh"
RUN_SCRIPT_PATH = Path(__file__).resolve().parents[2] / ".superset" / "run.sh"


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


def test_run_script_starts_overridden_processes_and_stops_cleanly(tmp_path: Path) -> None:
    workspace_path = tmp_path / "workspace"
    workspace_path.mkdir()
    (workspace_path / "app").mkdir()
    (workspace_path / ".env").write_text("BACKEND_URL=http://127.0.0.1:9001\n")

    marker_dir = workspace_path / "markers"
    marker_dir.mkdir()

    backend_marker = marker_dir / "backend.txt"
    frontend_marker = marker_dir / "frontend.txt"

    backend_cmd = (
        f"printf backend > {shlex.quote(str(backend_marker))}; "
        "trap 'exit 0' TERM INT; "
        "while :; do sleep 1; done"
    )
    frontend_cmd = (
        f"printf frontend > {shlex.quote(str(frontend_marker))}; "
        "trap 'exit 0' TERM INT; "
        "while :; do sleep 1; done"
    )

    proc = subprocess.Popen(
        ["/bin/sh", str(RUN_SCRIPT_PATH)],
        cwd=workspace_path,
        env={
            **os.environ,
            "SUPERSET_WORKSPACE_PATH": str(workspace_path),
            "SUPERSET_RUN_BOOTSTRAP": "0",
            "SUPERSET_RUN_BACKEND_CMD": backend_cmd,
            "SUPERSET_RUN_FRONTEND_CMD": frontend_cmd,
        },
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    deadline = time.time() + 5
    while time.time() < deadline:
        if backend_marker.exists() and frontend_marker.exists():
            break
        time.sleep(0.1)

    proc.terminate()
    proc.wait(timeout=10)

    assert proc.returncode == 0
    assert backend_marker.read_text() == "backend"
    assert frontend_marker.read_text() == "frontend"
