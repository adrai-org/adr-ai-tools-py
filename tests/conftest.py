"""Shared test fixtures."""

import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Protocol

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def isolated_filesystem(mocker: MockerFixture) -> Generator[Path, None, None]:
    """Provide isolated temporary filesystem with mocked home and cwd."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        mocker.patch("pathlib.Path.home", return_value=tmp_path)
        mocker.patch("pathlib.Path.cwd", return_value=tmp_path)
        yield tmp_path


@pytest.fixture
def mock_home_directory(mocker: MockerFixture) -> Generator[Path, None, None]:
    """Mock the home directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        mocker.patch("pathlib.Path.home", return_value=tmp_path)
        yield tmp_path


@pytest.fixture
def mock_current_directory(mocker: MockerFixture) -> Generator[Path, None, None]:
    """Mock the current working directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        mocker.patch("pathlib.Path.cwd", return_value=tmp_path)
        yield tmp_path


class ConfigFileFactory(Protocol):
    """Protocol for configuration file factory."""

    def __call__(self, path: Path, content: dict[str, str]) -> Path:
        """Create a TOML configuration file with given content."""
        ...


@pytest.fixture
def config_file_factory() -> ConfigFileFactory:
    """Factory for creating test configuration files."""

    def _create_config_file(path: Path, content: dict[str, str]) -> Path:
        """Create a TOML configuration file with given content."""
        path.parent.mkdir(parents=True, exist_ok=True)

        # Convert dict to TOML format
        toml_content = "\n".join(
            [f'{key} = "{value}"' for key, value in content.items()]
        )
        path.write_text(toml_content)
        return path

    return _create_config_file


@pytest.fixture
def sample_config_data() -> dict[str, str]:
    """Provide sample configuration data for testing."""
    return {
        "adr_directory": "test/adr",
        "template_file": "test/template.md",
        "author_name": "Test Author",
    }


@pytest.fixture
def isolated_e2e_env(mocker: MockerFixture) -> Generator[Path, None, None]:
    """Provide isolated environment for E2E tests with mocked HOME."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        mocker.patch.dict("os.environ", {"HOME": str(tmp_path)})
        yield tmp_path
