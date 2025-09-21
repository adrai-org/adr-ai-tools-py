"""End-to-end tests for the doctor command."""

from pathlib import Path

import pexpect
import pytest

from tests.e2e.conftest import ConfigCreator


@pytest.mark.e2e
def test_doctor_command_success(
    isolated_e2e_env: Path, config_creator: ConfigCreator
) -> None:
    """Test that the doctor command successfully diagnoses init configuration."""
    # Create valid configuration for init subcommand
    config_creator(
        {
            "adr_directory": "docs/adr",
            "template_file": "docs/adr/0000-adr-template.md",
            "author_name": "Test Author",
        }
    )

    # Run doctor init command in isolated environment
    child = pexpect.spawn(
        "uv run adr-ai-tools doctor", cwd=isolated_e2e_env, encoding="utf-8"
    )

    child.expect_exact("✅ Configuration Validation: PASS")
    child.expect(pexpect.EOF)
    child.close()

    assert child.exitstatus == 0


@pytest.mark.e2e
def test_doctor_command_invalid_config(
    isolated_e2e_env: Path, config_creator: ConfigCreator
) -> None:
    """Test that the doctor command fails with invalid configuration."""
    # Create invalid configuration (missing required fields)
    config_creator(
        {
            "invalid_field": "invalid_value",
        }
    )

    # Run doctor command in isolated environment
    child = pexpect.spawn(
        "uv run adr-ai-tools doctor", cwd=isolated_e2e_env, encoding="utf-8"
    )

    child.expect("❌ Configuration Validation: FAIL")
    child.expect(pexpect.EOF)
    child.close()

    # Should exit with non-zero status for invalid config
    assert child.exitstatus == 1


@pytest.mark.e2e
def test_doctor_command_corrupted_config(isolated_e2e_env: Path) -> None:
    """Test that the doctor command handles corrupted configuration file."""
    # Create corrupted config file
    config_file = isolated_e2e_env / ".adr-ai-tools" / "config.toml"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text("invalid toml content [[[")

    # Run doctor command in isolated environment
    child = pexpect.spawn(
        "uv run adr-ai-tools doctor", cwd=isolated_e2e_env, encoding="utf-8"
    )

    child.expect(
        r"❌ Configuration Validation: FAIL \(Configuration file is corrupted:"
    )
    child.expect(pexpect.EOF)
    child.close()

    # Should exit with non-zero status for corrupted config
    assert child.exitstatus == 1
