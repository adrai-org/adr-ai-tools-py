"""E2E tests for init command using pexpect."""

import tempfile
from pathlib import Path

import pexpect
import pytest


@pytest.mark.e2e
def test_init_command_creates_directory_and_template() -> None:
    """Test that init command creates docs/adr directory and template file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Run init command in temp directory
        child = pexpect.spawn("uv run adr-ai-tools init", cwd=tmpdir)
        child.expect_exact("Created docs/adr/ directory")
        child.expect_exact("Generated template: docs/adr/0000-adr-template.md")
        child.expect_exact(
            "Ready to create your first ADR with: "
            'adr-ai-tools new "Your decision title"'
        )
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code
        assert child.exitstatus == 0

        # Verify directory was created
        adr_dir = Path(tmpdir) / "docs/adr"
        assert adr_dir.exists()
        assert adr_dir.is_dir()

        # Verify template file was created
        template_file = adr_dir / "0000-adr-template.md"
        assert template_file.exists()
        assert template_file.is_file()

        # Verify template content
        content = template_file.read_text()
        assert "# Architecture Decision Record (ADR)" in content
        assert "## Title" in content
        assert "## Status" in content
        assert "## Date" in content


@pytest.mark.e2e
def test_init_command_with_existing_directory_continue() -> None:
    """Test that init command handles existing directory with user confirmation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create existing directory
        adr_dir = Path(tmpdir) / "docs/adr"
        adr_dir.mkdir(parents=True, exist_ok=True)

        # Run init command and confirm continuation
        child = pexpect.spawn("uv run adr-ai-tools init", cwd=tmpdir)
        child.expect_exact("Directory 'docs/adr' already exists. Continue? (y/N):")
        child.sendline("y")
        child.expect_exact("Created docs/adr/ directory")
        child.expect_exact("Generated template: docs/adr/0000-adr-template.md")
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code
        assert child.exitstatus == 0

        # Verify template was created
        template_file = adr_dir / "0000-adr-template.md"
        assert template_file.exists()


@pytest.mark.e2e
def test_init_command_with_existing_directory_cancel() -> None:
    """Test that init command handles existing directory with user cancellation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create existing directory
        adr_dir = Path(tmpdir) / "docs/adr"
        adr_dir.mkdir(parents=True, exist_ok=True)

        # Run init command and cancel
        child = pexpect.spawn("uv run adr-ai-tools init", cwd=tmpdir)
        child.expect_exact("Directory 'docs/adr' already exists. Continue? (y/N):")
        child.sendline("n")
        child.expect_exact("Initialization cancelled")
        child.expect(pexpect.EOF)
        child.close()

        # Verify exit code
        assert child.exitstatus == 0

        # Verify template was not created
        template_file = adr_dir / "0000-adr-template.md"
        assert not template_file.exists()
