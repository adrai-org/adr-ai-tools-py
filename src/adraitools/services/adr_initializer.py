"""ADR initialization service."""

from pathlib import Path

from adraitools.models.result import InitializationResult
from adraitools.services.configuration_service import ConfigurationService
from adraitools.services.file_system_service import FileSystemService
from adraitools.services.user_interaction_service import UserInteractionService


class AdrInitializer:
    """Service for initializing ADR directory structure."""

    def __init__(
        self,
        file_system_service: FileSystemService,
        user_interaction_service: UserInteractionService,
        configuration_service: ConfigurationService,
    ) -> None:
        """Initialize the ADR initializer."""
        self.file_system_service = file_system_service
        self.user_interaction_service = user_interaction_service
        self.configuration_service = configuration_service

    def initialize(self) -> InitializationResult:
        """Initialize ADR directory structure."""
        config = self.configuration_service.get_configuration()
        adr_dir = config.adr_directory
        template_file = config.template_file

        try:
            # Check if directory already exists and handle user confirmation
            if self._should_cancel_due_to_existing_directory(adr_dir):
                return InitializationResult(
                    success=False, message="Initialization cancelled"
                )

            # Create directory and template file
            self._create_adr_structure(adr_dir, template_file)

            return InitializationResult(
                success=True, message="ADR directory structure initialized successfully"
            )

        except OSError as e:
            return InitializationResult(
                success=False, message=f"Error during initialization: {e}"
            )

    def _should_cancel_due_to_existing_directory(self, adr_dir: Path) -> bool:
        """Check if initialization should be cancelled due to existing directory."""
        return self.file_system_service.directory_exists(
            adr_dir
        ) and not self.user_interaction_service.ask_confirmation(
            f"Directory '{adr_dir}' already exists. Continue? (y/N)"
        )

    def _create_adr_structure(self, adr_dir: Path, template_file: Path) -> None:
        """Create the ADR directory structure and template file."""
        self.file_system_service.create_directory(adr_dir)
        self.file_system_service.create_template_file(template_file)
