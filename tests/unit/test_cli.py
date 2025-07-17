"""Unit tests for CLI interface."""

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from adraitools.cli import app
from adraitools.models.result import InitializationResult


def test_init_command_success(mocker: MockerFixture) -> None:
    """Test init command with successful initialization."""
    # Arrange
    runner = CliRunner()

    # Mock the AdrInitializer class
    mock_initializer_class = mocker.patch("adraitools.cli.AdrInitializer")
    mock_initializer = mock_initializer_class.return_value
    success_result = InitializationResult(
        success=True, message="ADR directory structure initialized successfully"
    )
    mock_initializer.initialize.return_value = success_result

    # Mock the ConfigurationService to return predictable values
    mock_config_service = mocker.patch("adraitools.cli.ConfigurationService")
    mock_config = mock_config_service.return_value.get_configuration.return_value
    mock_config.adr_directory = "docs/adr"
    mock_config.template_file = "docs/adr/0000-adr-template.md"

    # Act
    result = runner.invoke(app, ["init"])

    # Assert
    assert result.exit_code == 0
    assert "Created docs/adr/ directory" in result.output
    assert "Generated template: docs/adr/0000-adr-template.md" in result.output
    assert (
        'Ready to create your first ADR with: adr-ai-tools new "Your decision title"'
        in result.output
    )


def test_init_command_cancelled(mocker: MockerFixture) -> None:
    """Test init command when user cancels initialization."""
    # Arrange
    runner = CliRunner()

    # Mock the AdrInitializer class
    mock_initializer_class = mocker.patch("adraitools.cli.AdrInitializer")
    mock_initializer = mock_initializer_class.return_value
    cancelled_result = InitializationResult(
        success=False, message="Initialization cancelled"
    )
    mock_initializer.initialize.return_value = cancelled_result

    # Act
    result = runner.invoke(app, ["init"])

    # Assert
    assert result.exit_code == 0
    assert "Initialization cancelled" in result.output


def test_init_command_error(mocker: MockerFixture) -> None:
    """Test init command with system error."""
    # Arrange
    runner = CliRunner()

    # Mock the AdrInitializer class
    mock_initializer_class = mocker.patch("adraitools.cli.AdrInitializer")
    mock_initializer = mock_initializer_class.return_value
    error_result = InitializationResult(
        success=False, message="Permission denied: Cannot create directory"
    )
    mock_initializer.initialize.return_value = error_result

    # Act
    result = runner.invoke(app, ["init"])

    # Assert
    assert result.exit_code == 1
    assert "Error: Permission denied: Cannot create directory" in result.output


def test_app_help_shows_init_command() -> None:
    """Test that help shows init command."""
    # Arrange
    runner = CliRunner()

    # Act
    result = runner.invoke(app, ["--help"])

    # Assert
    assert result.exit_code == 0
    assert "init" in result.output
    assert "Initialize ADR directory structure" in result.output
