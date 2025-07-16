"""Unit tests for configuration file loading functionality."""

import tempfile
from pathlib import Path
from tomllib import TOMLDecodeError

import pytest
from pytest_mock import MockerFixture

from adraitools.models.configuration import AdrConfiguration


def test_configuration_loads_from_project_local_toml_file(
    mocker: MockerFixture,
) -> None:
    """Test that configuration loads from project-local TOML file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create project-local config file
        config_dir = Path(tmpdir) / ".adr-ai-tools"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("""
adr_directory = "project/adr"
template_file = "project/adr/custom-template.md"
author_name = "Project Author"
""")

        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))
        config = AdrConfiguration()

        assert config.adr_directory == Path("project/adr")
        assert config.template_file == Path("project/adr/custom-template.md")
        assert config.author_name == "Project Author"


def test_configuration_loads_from_global_toml_file(mocker: MockerFixture) -> None:
    """Test that configuration loads from global TOML file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create global config file
        global_config_dir = Path(tmpdir) / ".config/adr-ai-tools"
        global_config_dir.mkdir(parents=True)
        config_file = global_config_dir / "config.toml"
        config_file.write_text("""
adr_directory = "global/adr"
author_name = "Global Author"
""")

        # Mock user home directory
        mocker.patch("pathlib.Path.home", return_value=Path(tmpdir))
        config = AdrConfiguration()

        assert config.adr_directory == Path("global/adr")
        assert config.author_name == "Global Author"
        # Should use default for unspecified values
        assert config.template_file == Path("docs/adr/0000-adr-template.md")


def test_configuration_precedence_project_over_global(
    mocker: MockerFixture,
) -> None:
    """Test that project-local configuration takes precedence over global."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create global config file
        global_config_dir = Path(tmpdir) / ".config/adr-ai-tools"
        global_config_dir.mkdir(parents=True)
        global_config_file = global_config_dir / "config.toml"
        global_config_file.write_text("""
adr_directory = "global/adr"
author_name = "Global Author"
""")

        # Create project-local config file
        project_dir = Path(tmpdir) / "project"
        project_dir.mkdir()
        project_config_dir = project_dir / ".adr-ai-tools"
        project_config_dir.mkdir()
        project_config_file = project_config_dir / "config.toml"
        project_config_file.write_text("""
adr_directory = "project/adr"
""")

        # Mock both home and current working directory
        mocker.patch("pathlib.Path.home", return_value=Path(tmpdir))
        mocker.patch("pathlib.Path.cwd", return_value=project_dir)
        config = AdrConfiguration()

        # Project-local should override global
        assert config.adr_directory == Path("project/adr")
        # Global should be used for unspecified values
        assert config.author_name == "Global Author"


def test_configuration_falls_back_to_defaults(mocker: MockerFixture) -> None:
    """Test that configuration falls back to defaults when no files exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock directories that don't contain config files
        mocker.patch("pathlib.Path.home", return_value=Path(tmpdir))
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))
        config = AdrConfiguration()

        # Should use defaults
        assert config.adr_directory == Path("docs/adr")
        assert config.template_file == Path("docs/adr/0000-adr-template.md")
        assert config.author_name == ""


def test_configuration_raises_error_for_invalid_toml_file(
    mocker: MockerFixture,
) -> None:
    """Test that configuration raises error for invalid TOML files (ADR-0019)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create invalid TOML file
        config_dir = Path(tmpdir) / ".adr-ai-tools"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("invalid toml content [[[")

        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))
        # Should raise error for invalid TOML file (strict validation per ADR-0019)
        with pytest.raises(TOMLDecodeError):
            AdrConfiguration()
