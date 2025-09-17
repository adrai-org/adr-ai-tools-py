"""Unit tests for doctor CLI command."""

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from adraitools.cli.cli import app
from adraitools.services.models.result import InitializationResult


def test_doctor_command_success(mocker: MockerFixture) -> None:
    """Test doctor command with successful diagnosis."""
    # Arrange
    runner = CliRunner()

    # Mock DoctorService and its dependencies
    mock_doctor_service_class = mocker.patch("adraitools.cli.cli.DoctorService")
    mock_doctor_service = mock_doctor_service_class.return_value
    success_result = InitializationResult(
        success=True, message="Configuration is valid"
    )
    mock_doctor_service.diagnose.return_value = success_result

    # Mock ConfigurationService dependency
    mock_config_service_class = mocker.patch("adraitools.cli.cli.ConfigurationService")

    # Act
    result = runner.invoke(app, ["doctor"])

    # Assert
    assert result.exit_code == 0
    assert "Configuration is valid" in result.output

    # Verify DoctorService was created with ConfigurationService
    mock_config_service_class.assert_called_once_with()
    mock_doctor_service_class.assert_called_once_with(
        configuration_service=mock_config_service_class.return_value
    )

    # Verify diagnose was called with correct subcommand
    mock_doctor_service.diagnose.assert_called_once_with()
