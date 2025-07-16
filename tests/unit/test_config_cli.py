"""Unit tests for config CLI commands."""

from pathlib import Path
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from adraitools.cli import app
from adraitools.models.configuration import AdrConfiguration
from adraitools.services.configuration_service import ConfigurationService


def test_config_list_command_success() -> None:
    """Test config list command shows all configuration values."""
    # Mock configuration service
    mock_config_service = Mock(spec=ConfigurationService)
    mock_config = AdrConfiguration(
        adr_directory=Path("docs/adr"),
        template_file=Path("docs/adr/0000-adr-template.md"),
        author_name="Test Author",
    )
    mock_config_service.get_configuration.return_value = mock_config

    # Mock service creation
    with patch("adraitools.cli.ConfigurationService", return_value=mock_config_service):
        runner = CliRunner()
        result = runner.invoke(app, ["config", "list"])

    assert result.exit_code == 0
    assert "adr_directory: docs/adr" in result.stdout
    assert "template_file: docs/adr/0000-adr-template.md" in result.stdout
    assert "author_name: Test Author" in result.stdout


def test_config_get_command_success() -> None:
    """Test config get command returns specific configuration value."""
    # Mock configuration service
    mock_config_service = Mock(spec=ConfigurationService)
    mock_config_service.get_value.return_value = "docs/adr"

    # Mock service creation
    with patch("adraitools.cli.ConfigurationService", return_value=mock_config_service):
        runner = CliRunner()
        result = runner.invoke(app, ["config", "get", "adr_directory"])

    assert result.exit_code == 0
    assert "docs/adr" in result.stdout
    mock_config_service.get_value.assert_called_once_with("adr_directory")


def test_config_set_command_success() -> None:
    """Test config set command updates configuration value."""
    # Mock configuration service
    mock_config_service = Mock(spec=ConfigurationService)
    mock_config_service.set_value.return_value = None

    # Mock service creation
    with patch("adraitools.cli.ConfigurationService", return_value=mock_config_service):
        runner = CliRunner()
        result = runner.invoke(
            app, ["config", "set", "adr_directory", "architecture/decisions"]
        )

    assert result.exit_code == 0
    expected_msg = (
        "Configuration updated (project-local): adr_directory = architecture/decisions"
    )
    assert expected_msg in result.stdout
    mock_config_service.set_value.assert_called_once_with(
        "adr_directory", "architecture/decisions", global_config=False
    )


def test_config_set_global_command_success() -> None:
    """Test config set --global command updates global configuration."""
    # Mock configuration service
    mock_config_service = Mock(spec=ConfigurationService)
    mock_config_service.set_value.return_value = None

    # Mock service creation
    with patch("adraitools.cli.ConfigurationService", return_value=mock_config_service):
        runner = CliRunner()
        result = runner.invoke(
            app, ["config", "set", "--global", "adr_directory", "global/decisions"]
        )

    assert result.exit_code == 0
    expected_msg = "Configuration updated (global): adr_directory = global/decisions"
    assert expected_msg in result.stdout
    mock_config_service.set_value.assert_called_once_with(
        "adr_directory", "global/decisions", global_config=True
    )
