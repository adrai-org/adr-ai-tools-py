"""Unit tests for doctor service."""

from unittest.mock import MagicMock

from adraitools.infrastructure.configuration_service import ConfigurationService
from adraitools.services.doctor_service import DoctorService
from adraitools.services.models.result import DiagnosisResult


def test_doctor_service() -> None:
    """Test that doctor service is created."""
    expected = DiagnosisResult(success=True, message="Configuration is valid")
    config_service = MagicMock(spec=ConfigurationService)
    service = DoctorService(configuration_service=config_service)

    actual = service.diagnose()

    config_service.get_configuration.assert_called_once_with()
    assert actual == expected
