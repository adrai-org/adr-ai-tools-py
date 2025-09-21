"""Service for doctor commands."""

from pydantic import ValidationError

from adraitools.exceptions import ConfigurationFileCorruptedError
from adraitools.infrastructure.configuration_service import ConfigurationService
from adraitools.services.models.result import DiagnosisResult, DiagnosisStepResult


class DoctorService:
    """Service for doctor commands."""

    def __init__(self, configuration_service: ConfigurationService) -> None:
        """Initialize the doctor service."""
        self.configuration_service = configuration_service

    def diagnose(self) -> DiagnosisResult:
        """Diagnose the configuration."""
        try:
            self.configuration_service.get_configuration()
            return DiagnosisResult(
                success=True,
                steps=[
                    DiagnosisStepResult(
                        step_name="CONFIG_VALIDATION",
                        result_level="PASS",
                        message="Configuration is valid",
                    )
                ],
            )
        except ValidationError as e:
            return DiagnosisResult(
                success=False,
                steps=[
                    DiagnosisStepResult(
                        step_name="CONFIG_VALIDATION",
                        result_level="FAIL",
                        message=f"Error during diagnosis: {e.errors()}",
                    )
                ],
            )
        except ConfigurationFileCorruptedError as e:
            return DiagnosisResult(
                success=False,
                steps=[
                    DiagnosisStepResult(
                        step_name="CONFIG_VALIDATION",
                        result_level="FAIL",
                        message="Configuration file is corrupted:"
                        f" {e.file_path.absolute()}",
                    )
                ],
            )
