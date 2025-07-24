"""Unit test fixtures."""

from pathlib import Path
from typing import NamedTuple
from unittest.mock import Mock

import pytest

from adraitools.infrastructure.configuration_service import ConfigurationService
from adraitools.infrastructure.file_system_service import FileSystemService
from adraitools.infrastructure.user_interaction_service import UserInteractionService
from adraitools.services.adr_initializer import AdrInitializer
from adraitools.services.models.configuration import AdrConfiguration


class MockServices(NamedTuple):
    """Container for mocked services."""

    file_system: Mock
    user_interaction: Mock
    configuration: Mock


class InitializerTestSetup(NamedTuple):
    """Container for initializer test setup."""

    initializer: AdrInitializer
    mocks: MockServices


@pytest.fixture
def mock_services() -> MockServices:
    """Create mock services for testing."""
    return MockServices(
        file_system=Mock(spec=FileSystemService),
        user_interaction=Mock(spec=UserInteractionService),
        configuration=Mock(spec=ConfigurationService),
    )


@pytest.fixture
def default_config() -> AdrConfiguration:
    """Create default configuration for testing."""
    return AdrConfiguration(
        adr_directory=Path("docs/adr"),
        template_file=Path("docs/adr/0000-adr-template.md"),
    )


@pytest.fixture
def custom_config() -> AdrConfiguration:
    """Create custom configuration for testing."""
    return AdrConfiguration(
        adr_directory=Path("custom/adr"),
        template_file=Path("custom/adr/0000-adr-template.md"),
    )


@pytest.fixture
def custom_template_config() -> AdrConfiguration:
    """Create configuration with custom template file for testing."""
    return AdrConfiguration(
        adr_directory=Path("docs/adr"),
        template_file=Path("custom/template.md"),
    )


@pytest.fixture
def initializer_setup(mock_services: MockServices) -> InitializerTestSetup:
    """Create AdrInitializer with mocked services."""
    initializer = AdrInitializer(
        mock_services.file_system,
        mock_services.user_interaction,
        mock_services.configuration,
    )
    return InitializerTestSetup(initializer=initializer, mocks=mock_services)
