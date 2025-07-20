"""End-to-end tests for logging functionality."""

from pathlib import Path

import pexpect
import pytest


@pytest.mark.e2e
def test_cli_verbose_flag_shows_debug_logs(isolated_e2e_env: Path) -> None:
    """Test that the CLI shows debug logs with --verbose flag."""
    # Use init command with --verbose flag to trigger logging setup
    child = pexpect.spawn(
        "uv run adr-ai-tools --verbose init", cwd=isolated_e2e_env, encoding="utf-8"
    )

    # Should show debug information when --verbose is used
    child.expect("DEBUG")
    child.expect_exact("Created docs/adr/ directory")
    child.expect(pexpect.EOF)
    child.close()

    # Verify exit code
    assert child.exitstatus == 0


@pytest.mark.e2e
def test_cli_quiet_flag_suppresses_logs(isolated_e2e_env: Path) -> None:
    """Test that the CLI suppresses logs with --quiet flag."""
    # Use init command with --quiet flag to trigger logging setup
    child = pexpect.spawn(
        "uv run adr-ai-tools --quiet init", cwd=isolated_e2e_env, encoding="utf-8"
    )

    # Should not show debug or info logs when --quiet is used
    child.expect_exact("Created docs/adr/ directory")
    child.expect(pexpect.EOF)
    child.close()

    # Verify exit code
    assert child.exitstatus == 0

    # Verify that no DEBUG or INFO logs were shown
    output = child.before or ""
    assert "DEBUG" not in output
    assert "INFO" not in output


@pytest.mark.e2e
def test_cli_log_file_option_creates_log_file(isolated_e2e_env: Path) -> None:
    """Test that the CLI creates a log file when --log-file option is used."""
    log_file = isolated_e2e_env / "debug.log"

    # Use init command with --log-file option
    child = pexpect.spawn(
        f"uv run adr-ai-tools --verbose --log-file {log_file} init",
        cwd=isolated_e2e_env,
        encoding="utf-8",
    )

    # Should show normal output
    child.expect_exact("Created docs/adr/ directory")
    child.expect(pexpect.EOF)
    child.close()

    # Verify exit code
    assert child.exitstatus == 0

    # Verify log file was created and contains debug information
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "DEBUG" in log_content
    assert "Debug logging enabled" in log_content
