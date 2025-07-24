"""User interaction service."""


class UserInteractionService:
    """Service for user interaction."""

    def ask_confirmation(self, message: str) -> bool:
        """Ask user for confirmation."""
        response = input(f"{message}: ").strip().lower()
        return response == "y"
