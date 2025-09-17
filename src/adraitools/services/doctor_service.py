"""Service for doctor commands."""

from pydantic import ValidationError

from adraitools.infrastructure.configuration_service import ConfigurationService
from adraitools.services.models.result import DiagnosisResult


class DoctorService:
    """Service for doctor commands."""

    def __init__(self, configuration_service: ConfigurationService) -> None:
        """Initialize the doctor service."""
        self.configuration_service = configuration_service

    def diagnose(self) -> DiagnosisResult:
        """Diagnose the configuration."""
        try:
            self.configuration_service.get_configuration()
            return DiagnosisResult(success=True, message="Configuration is valid")
        except ValidationError as e:
            return DiagnosisResult(
                success=False, message=f"Error during diagnosis: {e.errors()}"
            )
