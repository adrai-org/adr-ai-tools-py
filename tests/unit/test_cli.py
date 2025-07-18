"""Unit tests for CLI interface."""

from pathlib import Path

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


def test_verbose_flag_accepted() -> None:
    """Test that --verbose flag is accepted by CLI."""
    # Arrange
    runner = CliRunner()

    # Act
    result = runner.invoke(app, ["--verbose", "--version"])

    # Assert
    assert result.exit_code == 0
    # Should not show "No such option" error
    assert "No such option: --verbose" not in result.output


def test_verbose_flag_enables_debug_logging(mocker: MockerFixture) -> None:
    """Test that --verbose flag enables debug logging."""
    # Arrange
    runner = CliRunner()
    mock_logging_service = mocker.patch("adraitools.cli.LoggingService")
    mock_logging_instance = mock_logging_service.return_value

    # Mock init command dependencies to avoid actual execution
    mocker.patch("adraitools.cli.AdrInitializer")
    mocker.patch("adraitools.cli.ConfigurationService")

    # Act - Use init command to trigger callback
    result = runner.invoke(app, ["--verbose", "init"])

    # Assert
    assert result.exit_code == 0
    # Should create LoggingService and configure with debug level
    mock_logging_service.assert_called_once()
    mock_logging_instance.configure_logging.assert_called_once_with(
        level="DEBUG", log_file=None, quiet=False
    )


def test_quiet_flag_accepted(mocker: MockerFixture) -> None:
    """Test that --quiet flag is accepted by CLI."""
    # Arrange
    runner = CliRunner()
    mock_logging_service = mocker.patch("adraitools.cli.LoggingService")
    mock_logging_instance = mock_logging_service.return_value

    # Mock init command dependencies to avoid actual execution
    mocker.patch("adraitools.cli.AdrInitializer")
    mocker.patch("adraitools.cli.ConfigurationService")

    # Act - Use init command to trigger callback
    result = runner.invoke(app, ["--quiet", "init"])

    # Assert
    assert result.exit_code == 0
    # Should create LoggingService and configure with critical level for quiet
    mock_logging_service.assert_called_once()
    mock_logging_instance.configure_logging.assert_called_once_with(
        level="INFO", log_file=None, quiet=True
    )


def test_log_file_option_accepted(mocker: MockerFixture) -> None:
    """Test that --log-file option is accepted by CLI."""
    # Arrange
    runner = CliRunner()
    mock_logging_service = mocker.patch("adraitools.cli.LoggingService")
    mock_logging_instance = mock_logging_service.return_value

    # Mock init command dependencies to avoid actual execution
    mocker.patch("adraitools.cli.AdrInitializer")
    mocker.patch("adraitools.cli.ConfigurationService")

    # Act - Use init command to trigger callback
    result = runner.invoke(app, ["--log-file", "debug.log", "init"])

    # Assert
    assert result.exit_code == 0
    # Should create LoggingService and configure with log file
    mock_logging_service.assert_called_once()
    mock_logging_instance.configure_logging.assert_called_once_with(
        level="INFO", log_file=Path("debug.log"), quiet=False
    )
