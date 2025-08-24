"""End-to-end tests for the doctor command."""

from pathlib import Path

import pexpect
import pytest

from tests.e2e.conftest import ConfigCreator


@pytest.mark.e2e
def test_doctor_command_with_init_subcommand_success(
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
        "uv run adr-ai-tools doctor init", cwd=isolated_e2e_env, encoding="utf-8"
    )

    child.expect_exact("✓ init: Configuration is valid")
    child.expect(pexpect.EOF)
    child.close()

    assert child.exitstatus == 0
