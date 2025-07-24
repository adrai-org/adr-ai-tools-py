"""Unit tests for configuration service."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
import tomli
from pytest_mock import MockerFixture

from adraitools.infrastructure.configuration_service import ConfigurationService
from adraitools.services.models.configuration import AdrConfiguration


@pytest.fixture
def _mock_home_directory(mocker: MockerFixture) -> Generator[Path, None, None]:
    """Mock the home directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        mocker.patch("pathlib.Path.home", return_value=Path(tmpdir))
        yield Path(tmpdir)


@pytest.fixture
def _mock_current_working_directory(
    mocker: MockerFixture,
) -> Generator[Path, None, None]:
    """Mock the current working directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))
        yield Path(tmpdir)


@pytest.mark.usefixtures("_mock_home_directory", "_mock_current_working_directory")
def test_get_configuration_returns_adr_configuration() -> None:
    """Test that get_configuration returns an AdrConfiguration instance."""
    service = ConfigurationService()
    config = service.get_configuration()

    assert isinstance(config, AdrConfiguration)
    assert config.adr_directory.name == "adr"
    assert config.template_file.name == "0000-adr-template.md"


@pytest.mark.usefixtures("_mock_home_directory", "_mock_current_working_directory")
def test_get_value_returns_configuration_attribute() -> None:
    """Test that get_value returns the correct configuration attribute."""
    service = ConfigurationService()

    adr_directory = service.get_value("adr_directory")
    assert str(adr_directory) == "docs/adr"

    template_file = service.get_value("template_file")
    assert str(template_file) == "docs/adr/0000-adr-template.md"


def test_get_value_raises_keyerror_for_unknown_key() -> None:
    """Test that get_value raises KeyError for unknown configuration key."""
    service = ConfigurationService()

    with pytest.raises(KeyError) as exc_info:
        service.get_value("unknown_key")

    assert "Unknown configuration key 'unknown_key'" in str(exc_info.value)


def test_set_value_raises_keyerror_for_unknown_key() -> None:
    """Test that set_value raises KeyError for unknown configuration key."""
    service = ConfigurationService()

    with pytest.raises(KeyError) as exc_info:
        service.set_value("unknown_key", "value")

    assert "Unknown configuration key 'unknown_key'" in str(exc_info.value)


def test_set_value_validates_known_key(mocker: MockerFixture) -> None:
    """Test that set_value validates that known keys exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))

        service = ConfigurationService()

        # Should not raise for valid keys
        service.set_value("adr_directory", "new/path")
        service.set_value("template_file", "new-template.md")
        service.set_value("author_name", "New Author")


def test_configuration_service_set_value_creates_project_local_config(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value creates project-local config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))

        service = ConfigurationService()
        service.set_value("adr_directory", "custom/adr")

        # Check that config file was created
        config_file = Path(tmpdir) / ".adr-ai-tools" / "config.toml"
        assert config_file.exists()

        # Check that config file contains the correct value
        with config_file.open("rb") as f:
            config_data = tomli.load(f)

        assert config_data["adr_directory"] == "custom/adr"


def test_configuration_service_set_value_updates_existing_config(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value updates existing config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create existing config file
        config_dir = Path(tmpdir) / ".adr-ai-tools"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("""
adr_directory = "old/adr"
author_name = "Test Author"
""")

        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))

        service = ConfigurationService()
        service.set_value("adr_directory", "new/adr")

        # Check that config file was updated
        with config_file.open("rb") as f:
            config_data = tomli.load(f)

        assert config_data["adr_directory"] == "new/adr"
        assert (
            config_data["author_name"] == "Test Author"
        )  # Should preserve existing values


def test_configuration_service_set_value_handles_path_fields(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value handles Path fields correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))

        service = ConfigurationService()
        service.set_value("template_file", "custom/template.md")

        # Check that config file contains the correct value
        config_file = Path(tmpdir) / ".adr-ai-tools" / "config.toml"
        with config_file.open("rb") as f:
            config_data = tomli.load(f)

        assert config_data["template_file"] == "custom/template.md"


def test_configuration_service_set_value_raises_error_for_invalid_key(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value raises KeyError for invalid keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))

        service = ConfigurationService()

        with pytest.raises(KeyError, match="Unknown configuration key 'invalid_key'"):
            service.set_value("invalid_key", "some_value")


def test_configuration_service_set_value_handles_string_fields(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value handles string fields correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))

        service = ConfigurationService()
        service.set_value("author_name", "Test Author")

        # Check that config file contains the correct value
        config_file = Path(tmpdir) / ".adr-ai-tools" / "config.toml"
        with config_file.open("rb") as f:
            config_data = tomli.load(f)

        assert config_data["author_name"] == "Test Author"


def test_configuration_service_set_value_creates_global_config(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value creates global config file with global_config=True."""  # noqa: E501
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock home directory
        mocker.patch("pathlib.Path.home", return_value=Path(tmpdir))

        service = ConfigurationService()
        service.set_value("adr_directory", "global/adr", global_config=True)

        # Check that global config file was created
        global_config_file = Path(tmpdir) / ".config" / "adr-ai-tools" / "config.toml"
        assert global_config_file.exists()

        # Check that config file contains the correct value
        with global_config_file.open("rb") as f:
            config_data = tomli.load(f)

        assert config_data["adr_directory"] == "global/adr"


def test_configuration_service_set_value_updates_existing_global_config(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value updates existing global config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create existing global config file
        global_config_dir = Path(tmpdir) / ".config" / "adr-ai-tools"
        global_config_dir.mkdir(parents=True)
        global_config_file = global_config_dir / "config.toml"
        global_config_file.write_text("""
adr_directory = "old/global/adr"
author_name = "Global Author"
""")

        # Mock home directory
        mocker.patch("pathlib.Path.home", return_value=Path(tmpdir))

        service = ConfigurationService()
        service.set_value("adr_directory", "new/global/adr", global_config=True)

        # Check that config file was updated
        with global_config_file.open("rb") as f:
            config_data = tomli.load(f)

        assert config_data["adr_directory"] == "new/global/adr"
        assert (
            config_data["author_name"] == "Global Author"
        )  # Should preserve existing values


def test_configuration_service_set_value_global_flag_defaults_to_false(
    mocker: MockerFixture,
) -> None:
    """Test that ConfigurationService.set_value defaults to project-local when global_config is not specified."""  # noqa: E501
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock current working directory
        mocker.patch("pathlib.Path.cwd", return_value=Path(tmpdir))

        service = ConfigurationService()
        service.set_value("adr_directory", "project/adr")

        # Check that project-local config file was created
        project_config_file = Path(tmpdir) / ".adr-ai-tools" / "config.toml"
        assert project_config_file.exists()

        # Check that config file contains the correct value
        with project_config_file.open("rb") as f:
            config_data = tomli.load(f)

        assert config_data["adr_directory"] == "project/adr"
