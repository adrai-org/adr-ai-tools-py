"""E2E test configuration."""

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def current_dir() -> Path:
    """The current directory."""
    return Path(__file__).parent


@pytest.fixture(autouse=True)
def test_dir(current_dir: Path) -> Path:
    """The test directory."""
    return current_dir.parent


@pytest.fixture(autouse=True)
def project_dir(test_dir: Path) -> Path:
    """The project directory."""
    return test_dir.parent
