"""Unit tests for doctor CLI command."""

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from adraitools.cli.cli import app
from adraitools.services.models.result import DiagnosisResult


def test_doctor_command_success(mocker: MockerFixture) -> None:
    """Test doctor command with successful diagnosis."""
    # Arrange
    runner = CliRunner()

    # Mock DoctorService and its dependencies
    mock_doctor_service_class = mocker.patch("adraitools.cli.cli.DoctorService")
    mock_doctor_service = mock_doctor_service_class.return_value
    success_result = DiagnosisResult(success=True, message="Configuration is valid")
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


def test_doctor_command_invalid_config(mocker: MockerFixture) -> None:
    """Test doctor command with invalid configuration."""
    # Arrange
    runner = CliRunner()

    # Mock DoctorService and its dependencies
    mock_doctor_service_class = mocker.patch("adraitools.cli.cli.DoctorService")
    mock_doctor_service = mock_doctor_service_class.return_value
    error_result = DiagnosisResult(success=False, message="Invalid configuration")
    mock_doctor_service.diagnose.return_value = error_result

    # Mock ConfigurationService dependency
    mock_config_service_class = mocker.patch("adraitools.cli.cli.ConfigurationService")

    # Act
    result = runner.invoke(app, ["doctor"])

    # Assert
    assert result.exit_code == 1
    assert "Invalid configuration" in result.output

    # Verify DoctorService was created with ConfigurationService
    mock_config_service_class.assert_called_once_with()
    mock_doctor_service_class.assert_called_once_with(
        configuration_service=mock_config_service_class.return_value
    )

    # Verify diagnose was called with correct subcommand
    mock_doctor_service.diagnose.assert_called_once_with()
