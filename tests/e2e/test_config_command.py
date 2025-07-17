"""E2E tests for config command using pexpect."""

import tempfile
from pathlib import Path

import pexpect
import pytest
from pytest_mock import MockerFixture


@pytest.mark.e2e
def test_config_list_command_shows_default_values(mocker: MockerFixture) -> None:
    """Test that config list command shows default configuration values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        mocker.patch.dict("os.environ", {"HOME": tmpdir})
        # Run config list command in temp directory
        child = pexpect.spawn("uv run adr-ai-tools config list", cwd=tmpdir)
        child.expect_exact("adr_directory: docs/adr")
        child.expect_exact("template_file: docs/adr/0000-adr-template.md")
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code
        assert child.exitstatus == 0


@pytest.mark.e2e
def test_config_get_command_returns_specific_value(mocker: MockerFixture) -> None:
    """Test that config get command returns a specific configuration value."""
    with tempfile.TemporaryDirectory() as tmpdir:
        mocker.patch.dict("os.environ", {"HOME": tmpdir})
        # Run config get command for adr_directory
        child = pexpect.spawn(
            "uv run adr-ai-tools config get adr_directory", cwd=tmpdir
        )
        child.expect_exact("docs/adr")
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code
        assert child.exitstatus == 0


@pytest.mark.e2e
def test_config_set_command_updates_value() -> None:
    """Test that config set command updates a configuration value."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Run config set command to update adr_directory
        child = pexpect.spawn(
            "uv run adr-ai-tools config set adr_directory architecture/decisions",
            cwd=tmpdir,
        )
        child.expect_exact(
            "Configuration updated (project-local): "
            "adr_directory = architecture/decisions"
        )
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code
        assert child.exitstatus == 0

        # Verify the change persists by getting the value
        child = pexpect.spawn(
            "uv run adr-ai-tools config get adr_directory", cwd=tmpdir
        )
        child.expect_exact("architecture/decisions")
        child.expect(pexpect.EOF)
        child.close()

        assert child.exitstatus == 0


@pytest.mark.e2e
def test_config_with_invalid_key_shows_error() -> None:
    """Test that config commands with invalid keys show appropriate errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Run config get with invalid key
        child = pexpect.spawn("uv run adr-ai-tools config get invalid_key", cwd=tmpdir)
        child.expect_exact("Error: \"Unknown configuration key 'invalid_key'\"")
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code indicates error
        assert child.exitstatus == 1


@pytest.mark.e2e
def test_config_uses_project_local_configuration() -> None:
    """Test that config commands use project-local configuration when available."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a project-local configuration file
        config_dir = Path(tmpdir) / ".adr-ai-tools"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("""
adr_directory = "project/adr"
template_file = "project/adr/custom-template.md"
""")

        # Run config get command - should use project-local config
        child = pexpect.spawn(
            "uv run adr-ai-tools config get adr_directory", cwd=tmpdir
        )
        child.expect_exact("project/adr")
        child.expect(pexpect.EOF)
        child.close()

        assert child.exitstatus == 0


@pytest.mark.e2e
def test_config_set_global_command_updates_global_config(mocker: MockerFixture) -> None:
    """Test that config set --global command updates global configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock home directory to create global config there
        mocker.patch.dict("os.environ", {"HOME": tmpdir})

        # Run config set --global command
        child = pexpect.spawn(
            "uv run adr-ai-tools config set --global adr_directory global/decisions",
            cwd=tmpdir,
        )
        child.expect_exact(
            "Configuration updated (global): adr_directory = global/decisions"
        )
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code
        assert child.exitstatus == 0

        # Verify global config file was created
        global_config_file = Path(tmpdir) / ".config" / "adr-ai-tools" / "config.toml"
        assert global_config_file.exists()

        # Verify the change persists by getting the value
        child = pexpect.spawn(
            "uv run adr-ai-tools config get adr_directory", cwd=tmpdir
        )
        child.expect_exact("global/decisions")
        child.expect(pexpect.EOF)
        child.close()

        assert child.exitstatus == 0


@pytest.mark.e2e
def test_config_set_global_vs_local_precedence(mocker: MockerFixture) -> None:
    """Test that project-local config takes precedence over global config."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock home directory
        mocker.patch.dict("os.environ", {"HOME": tmpdir})

        # Set global config
        child = pexpect.spawn(
            "uv run adr-ai-tools config set --global adr_directory global/adr",
            cwd=tmpdir,
        )
        child.expect_exact("Configuration updated (global): adr_directory = global/adr")
        child.expect(pexpect.EOF)
        child.close()
        assert child.exitstatus == 0

        # Set project-local config (should override global)
        child = pexpect.spawn(
            "uv run adr-ai-tools config set adr_directory project/adr",
            cwd=tmpdir,
        )
        child.expect_exact(
            "Configuration updated (project-local): adr_directory = project/adr"
        )
        child.expect(pexpect.EOF)
        child.close()
        assert child.exitstatus == 0

        # Verify project-local takes precedence
        child = pexpect.spawn(
            "uv run adr-ai-tools config get adr_directory", cwd=tmpdir
        )
        child.expect_exact("project/adr")
        child.expect(pexpect.EOF)
        child.close()
        assert child.exitstatus == 0
