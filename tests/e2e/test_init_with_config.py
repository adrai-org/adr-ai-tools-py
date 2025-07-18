"""E2E tests for init command with configuration integration."""

from pathlib import Path

import pexpect
import pytest

from tests.e2e.conftest import ConfigCreator


@pytest.mark.e2e
def test_init_command_uses_configured_adr_directory(
    isolated_e2e_env: Path, config_creator: ConfigCreator
) -> None:
    """Test that init command uses configured adr_directory instead of default."""
    # Create a custom adr_directory configuration
    config_creator(
        {
            "adr_directory": "custom/adr",
            "template_file": "custom/adr/0000-adr-template.md",
        }
    )

    # Run init command
    child = pexpect.spawn("uv run adr-ai-tools init", cwd=isolated_e2e_env)
    child.expect("Created custom/adr/ directory")
    child.expect("Generated template: custom/adr/0000-adr-template.md")
    child.expect(pexpect.EOF)
    child.close()

    # Verify exit code
    assert child.exitstatus == 0

    # Verify the custom directory was created
    assert (isolated_e2e_env / "custom" / "adr").exists()
    assert (isolated_e2e_env / "custom" / "adr" / "0000-adr-template.md").exists()

    # Verify default directory was NOT created
    assert not (isolated_e2e_env / "docs" / "adr").exists()


@pytest.mark.e2e
def test_init_command_uses_configured_template_file(
    isolated_e2e_env: Path, config_creator: ConfigCreator
) -> None:
    """Test that init command uses configured template_file instead of default."""
    # Create a custom template_file configuration (within adr_directory)
    config_creator(
        {"adr_directory": "docs/adr", "template_file": "docs/adr/custom-template.md"}
    )

    # Run init command
    child = pexpect.spawn("uv run adr-ai-tools init", cwd=isolated_e2e_env)
    child.expect("Created docs/adr/ directory")
    child.expect("Generated template: docs/adr/custom-template.md")
    child.expect(pexpect.EOF)
    child.close()

    # Verify exit code
    assert child.exitstatus == 0

    # Verify the custom template was created
    assert (isolated_e2e_env / "docs" / "adr" / "custom-template.md").exists()

    # Verify default template was NOT created
    assert not (isolated_e2e_env / "docs" / "adr" / "0000-adr-template.md").exists()
