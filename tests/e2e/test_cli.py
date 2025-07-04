"""End-to-end tests for the CLI."""

import shutil
from pathlib import Path
from subprocess import run

import adraitools


def test_cli_print_version(project_dir: Path) -> None:
    """Test that the CLI prints the version."""
    cmd_path_str = shutil.which("adr-ai-tools")
    assert cmd_path_str is not None, "adr-ai-tools not found in PATH"
    cmd_path = Path(cmd_path_str)
    assert cmd_path.is_absolute(), "Command path must be absolute"
    assert str(project_dir) in cmd_path.parent.as_posix(), (
        "Project directory not found in command path"
    )
    result = run(  # noqa: S603
        [cmd_path, "--version"],
        capture_output=True,
        shell=False,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "adr-ai-tools" in result.stdout
    assert adraitools.__version__ in result.stdout
