"""Unit tests for ADR initializer."""

from pathlib import Path
from unittest.mock import Mock

from adraitools.services.adr_initializer import AdrInitializer
from adraitools.services.file_system_service import FileSystemService
from adraitools.services.user_interaction_service import UserInteractionService


def test_initialize_creates_directory_and_template() -> None:
    """Test that initialize creates directory and template file."""
    # Arrange
    file_system_service = Mock(spec=FileSystemService)
    user_interaction_service = Mock(spec=UserInteractionService)
    file_system_service.directory_exists.return_value = False

    initializer = AdrInitializer(file_system_service, user_interaction_service)

    # Act
    result = initializer.initialize()

    # Assert
    assert result.success is True
    assert result.message == "ADR directory structure initialized successfully"
    file_system_service.create_directory.assert_called_once_with(Path("docs/adr"))
    file_system_service.create_template_file.assert_called_once_with(
        Path("docs/adr/0000-adr-template.md")
    )
    user_interaction_service.ask_confirmation.assert_not_called()


def test_initialize_with_existing_directory_user_confirms() -> None:
    """Test initialize with existing directory when user confirms."""
    # Arrange
    file_system_service = Mock(spec=FileSystemService)
    user_interaction_service = Mock(spec=UserInteractionService)
    file_system_service.directory_exists.return_value = True
    user_interaction_service.ask_confirmation.return_value = True

    initializer = AdrInitializer(file_system_service, user_interaction_service)

    # Act
    result = initializer.initialize()

    # Assert
    assert result.success is True
    assert result.message == "ADR directory structure initialized successfully"
    file_system_service.create_directory.assert_called_once_with(Path("docs/adr"))
    file_system_service.create_template_file.assert_called_once_with(
        Path("docs/adr/0000-adr-template.md")
    )
    user_interaction_service.ask_confirmation.assert_called_once_with(
        "Directory 'docs/adr' already exists. Continue? (y/N)"
    )


def test_initialize_with_existing_directory_user_cancels() -> None:
    """Test initialize with existing directory when user cancels."""
    # Arrange
    file_system_service = Mock(spec=FileSystemService)
    user_interaction_service = Mock(spec=UserInteractionService)
    file_system_service.directory_exists.return_value = True
    user_interaction_service.ask_confirmation.return_value = False

    initializer = AdrInitializer(file_system_service, user_interaction_service)

    # Act
    result = initializer.initialize()

    # Assert
    assert result.success is False
    assert result.message == "Initialization cancelled"
    file_system_service.create_directory.assert_not_called()
    file_system_service.create_template_file.assert_not_called()
    user_interaction_service.ask_confirmation.assert_called_once_with(
        "Directory 'docs/adr' already exists. Continue? (y/N)"
    )


def test_initialize_handles_file_system_error() -> None:
    """Test that initialize handles file system errors gracefully."""
    # Arrange
    file_system_service = Mock(spec=FileSystemService)
    user_interaction_service = Mock(spec=UserInteractionService)
    file_system_service.directory_exists.return_value = False
    file_system_service.create_directory.side_effect = OSError("Permission denied")

    initializer = AdrInitializer(file_system_service, user_interaction_service)

    # Act
    result = initializer.initialize()

    # Assert
    assert result.success is False
    assert "Permission denied" in result.message
    file_system_service.create_directory.assert_called_once_with(Path("docs/adr"))
    file_system_service.create_template_file.assert_not_called()
