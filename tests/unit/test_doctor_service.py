"""Unit tests for doctor service."""

from pathlib import Path
from unittest.mock import MagicMock

from pydantic import ValidationError
from pydantic_core import InitErrorDetails

from adraitools.exceptions import ConfigurationFileCorruptedError
from adraitools.infrastructure.configuration_service import ConfigurationService
from adraitools.services.doctor_service import DoctorService
from adraitools.services.models.result import DiagnosisResult


def test_doctor_service_diagnose_success() -> None:
    """Test that doctor service is created."""
    expected = DiagnosisResult(success=True, message="Configuration is valid")
    config_service = MagicMock(spec=ConfigurationService)
    service = DoctorService(configuration_service=config_service)

    actual = service.diagnose()

    config_service.get_configuration.assert_called_once_with()
    assert actual == expected


def test_doctor_service_diagnose_invalid_config() -> None:
    """Test that doctor service is created."""
    errors = [
        InitErrorDetails(type="missing", loc=("adr_directory",), input={}),
        InitErrorDetails(
            type="string_type",
            loc=("author_name",),
            input=123,
        ),
    ]

    validation_error = ValidationError.from_exception_data("AdrConfiguration", errors)

    expected = DiagnosisResult(
        success=False,
        message="Error during diagnosis: [{'type': 'missing', 'loc': ('adr_directory',)"
        ", 'msg': 'Field required', 'input': {}, "
        "'url': 'https://errors.pydantic.dev/2.11/v/missing'}, "
        "{'type': 'string_type', 'loc': ('author_name',), 'msg': "
        "'Input should be a valid string', 'input': 123, 'url': 'https://errors.pydantic.dev/2.11/v/string_type'}]",
    )
    config_service = MagicMock(spec=ConfigurationService)
    config_service.get_configuration.side_effect = validation_error
    service = DoctorService(configuration_service=config_service)

    actual = service.diagnose()

    config_service.get_configuration.assert_called_once_with()
    assert actual == expected


def test_doctor_service_diagnose_corrupted_config() -> None:
    """Test that doctor service is created."""
    config_file = Path(".adr-ai-tools.toml")
    expected = DiagnosisResult(
        success=False,
        message="Error during diagnosis: Configuration file"
        f" {config_file} is corrupted.",
    )
    config_service = MagicMock(spec=ConfigurationService)
    config_service.get_configuration.side_effect = ConfigurationFileCorruptedError(
        file_path=config_file
    )
    service = DoctorService(configuration_service=config_service)
    actual = service.diagnose()
    assert actual == expected
