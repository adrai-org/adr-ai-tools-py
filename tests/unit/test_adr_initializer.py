"""Unit tests for ADR initializer."""

from pathlib import Path

from adraitools.models.configuration import AdrConfiguration
from tests.unit.conftest import InitializerTestSetup


def test_initialize_creates_directory_and_template(
    initializer_setup: InitializerTestSetup, default_config: AdrConfiguration
) -> None:
    """Test that initialize creates directory and template file."""
    # Arrange
    initializer_setup.mocks.file_system.directory_exists.return_value = False
    initializer_setup.mocks.configuration.get_configuration.return_value = (
        default_config
    )

    # Act
    result = initializer_setup.initializer.initialize()

    # Assert
    assert result.success is True
    assert result.message == "ADR directory structure initialized successfully"
    initializer_setup.mocks.file_system.create_directory.assert_called_once_with(
        Path("docs/adr")
    )
    initializer_setup.mocks.file_system.create_template_file.assert_called_once_with(
        Path("docs/adr/0000-adr-template.md")
    )
    initializer_setup.mocks.user_interaction.ask_confirmation.assert_not_called()
    initializer_setup.mocks.configuration.get_configuration.assert_called_once()


def test_initialize_with_existing_directory_user_confirms(
    initializer_setup: InitializerTestSetup, default_config: AdrConfiguration
) -> None:
    """Test initialize with existing directory when user confirms."""
    # Arrange
    initializer_setup.mocks.file_system.directory_exists.return_value = True
    initializer_setup.mocks.user_interaction.ask_confirmation.return_value = True
    initializer_setup.mocks.configuration.get_configuration.return_value = (
        default_config
    )

    # Act
    result = initializer_setup.initializer.initialize()

    # Assert
    assert result.success is True
    assert result.message == "ADR directory structure initialized successfully"
    initializer_setup.mocks.file_system.create_directory.assert_called_once_with(
        Path("docs/adr")
    )
    initializer_setup.mocks.file_system.create_template_file.assert_called_once_with(
        Path("docs/adr/0000-adr-template.md")
    )
    initializer_setup.mocks.user_interaction.ask_confirmation.assert_called_once_with(
        "Directory 'docs/adr' already exists. Continue? (y/N)"
    )


def test_initialize_with_existing_directory_user_cancels(
    initializer_setup: InitializerTestSetup, default_config: AdrConfiguration
) -> None:
    """Test initialize with existing directory when user cancels."""
    # Arrange
    initializer_setup.mocks.file_system.directory_exists.return_value = True
    initializer_setup.mocks.user_interaction.ask_confirmation.return_value = False
    initializer_setup.mocks.configuration.get_configuration.return_value = (
        default_config
    )

    # Act
    result = initializer_setup.initializer.initialize()

    # Assert
    assert result.success is False
    assert result.message == "Initialization cancelled"
    initializer_setup.mocks.file_system.create_directory.assert_not_called()
    initializer_setup.mocks.file_system.create_template_file.assert_not_called()
    initializer_setup.mocks.user_interaction.ask_confirmation.assert_called_once_with(
        "Directory 'docs/adr' already exists. Continue? (y/N)"
    )


def test_initialize_handles_file_system_error(
    initializer_setup: InitializerTestSetup, default_config: AdrConfiguration
) -> None:
    """Test that initialize handles file system errors gracefully."""
    # Arrange
    initializer_setup.mocks.file_system.directory_exists.return_value = False
    initializer_setup.mocks.file_system.create_directory.side_effect = OSError(
        "Permission denied"
    )
    initializer_setup.mocks.configuration.get_configuration.return_value = (
        default_config
    )

    # Act
    result = initializer_setup.initializer.initialize()

    # Assert
    assert result.success is False
    assert "Permission denied" in result.message
    initializer_setup.mocks.file_system.create_directory.assert_called_once_with(
        Path("docs/adr")
    )
    initializer_setup.mocks.file_system.create_template_file.assert_not_called()


def test_initialize_uses_configured_adr_directory(
    initializer_setup: InitializerTestSetup, custom_config: AdrConfiguration
) -> None:
    """Test that initialize uses configured adr_directory instead of default."""
    # Arrange
    initializer_setup.mocks.file_system.directory_exists.return_value = False
    initializer_setup.mocks.configuration.get_configuration.return_value = custom_config

    # Act
    result = initializer_setup.initializer.initialize()

    # Assert
    assert result.success is True
    initializer_setup.mocks.file_system.create_directory.assert_called_once_with(
        Path("custom/adr")
    )
    initializer_setup.mocks.file_system.create_template_file.assert_called_once_with(
        Path("custom/adr/0000-adr-template.md")
    )
    initializer_setup.mocks.configuration.get_configuration.assert_called_once()


def test_initialize_uses_configured_template_file(
    initializer_setup: InitializerTestSetup, custom_template_config: AdrConfiguration
) -> None:
    """Test that initialize uses configured template_file instead of default."""
    # Arrange
    initializer_setup.mocks.file_system.directory_exists.return_value = False
    initializer_setup.mocks.configuration.get_configuration.return_value = (
        custom_template_config
    )

    # Act
    result = initializer_setup.initializer.initialize()

    # Assert
    assert result.success is True
    initializer_setup.mocks.file_system.create_directory.assert_called_once_with(
        Path("docs/adr")
    )
    initializer_setup.mocks.file_system.create_template_file.assert_called_once_with(
        Path("custom/template.md")
    )
    initializer_setup.mocks.configuration.get_configuration.assert_called_once()
