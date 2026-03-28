import os
import subprocess
from pathlib import Path


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
