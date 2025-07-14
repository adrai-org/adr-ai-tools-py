"""ADR initialization service."""

from pathlib import Path

from adraitools.models.result import InitializationResult
from adraitools.services.file_system_service import FileSystemService
from adraitools.services.user_interaction_service import UserInteractionService


class AdrInitializer:
    """Service for initializing ADR directory structure."""

    def __init__(
        self,
        file_system_service: FileSystemService,
        user_interaction_service: UserInteractionService,
    ) -> None:
        """Initialize the ADR initializer."""
        self.file_system_service = file_system_service
        self.user_interaction_service = user_interaction_service

    def initialize(self) -> InitializationResult:
        """Initialize ADR directory structure."""
        adr_dir = Path("docs/adr")
        template_file = adr_dir / "0000-adr-template.md"

        try:
            # Check if directory already exists
            if (self.file_system_service.directory_exists(adr_dir)
                and not self.user_interaction_service.ask_confirmation(
                    "Directory 'docs/adr' already exists. Continue? (y/N)"
                )):
                    return InitializationResult(
                        success=False, message="Initialization cancelled"
                    )

            # Create directory and template file
            self.file_system_service.create_directory(adr_dir)
            self.file_system_service.create_template_file(template_file)

            return InitializationResult(
                success=True, message="ADR directory structure initialized successfully"
            )

        except OSError as e:
            return InitializationResult(
                success=False, message=f"Error during initialization: {e}"
            )
