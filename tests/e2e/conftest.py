"""E2E test configuration."""

from pathlib import Path
from typing import NamedTuple, Protocol

import pexpect
import pytest


class PexpectResult(NamedTuple):
    """Result of pexpect command execution."""

    exit_code: int
    output: str


class CommandRunner(Protocol):
    """Protocol for command runner."""

    def __call__(self, command: str, expect_patterns: list[str]) -> PexpectResult:
        """Run command and expect patterns."""
        ...


class ConfigCreator(Protocol):
    """Protocol for configuration creator."""

    def __call__(self, config_data: dict[str, str]) -> Path:
        """Create configuration file with given data."""
        ...


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


@pytest.fixture
def e2e_runner(isolated_e2e_env: Path) -> CommandRunner:
    """Create command runner for E2E tests."""

    def _run_command(command: str, expect_patterns: list[str]) -> PexpectResult:
        """Run command and expect patterns."""
        child = pexpect.spawn(command, cwd=isolated_e2e_env, encoding="utf-8")

        output_lines = []
        try:
            for pattern in expect_patterns:
                child.expect(pattern)
                output_lines.append(child.before or "")

            child.expect(pexpect.EOF)
            child.close()

            return PexpectResult(
                exit_code=child.exitstatus or 0,
                output="\n".join(output_lines),
            )
        except pexpect.exceptions.EOF:
            child.close()
            return PexpectResult(
                exit_code=child.exitstatus or 1,
                output="\n".join(output_lines),
            )

    return _run_command


@pytest.fixture
def config_creator(isolated_e2e_env: Path) -> ConfigCreator:
    """Create configuration creator for E2E tests."""

    def _create_config(config_data: dict[str, str]) -> Path:
        """Create configuration file with given data."""
        config_dir = isolated_e2e_env / ".adr-ai-tools"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.toml"

        toml_content = "\n".join(
            [f'{key} = "{value}"' for key, value in config_data.items()]
        )
        config_file.write_text(toml_content)
        return config_file

    return _create_config
