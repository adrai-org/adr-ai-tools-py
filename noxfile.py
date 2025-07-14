"""Nox configuration file for adr-ai-tools."""

import nox

nox.options.default_venv_backend = "uv"

# Supported Python versions
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]


@nox.session(python="3.11")
def tests_unit(session: nox.Session) -> None:
    """Run unit and integration tests (not e2e)."""
    session.install("-e", ".", "--group=dev")
    session.run("pytest", "-m", "not e2e")


@nox.session(python="3.11")
def tests_e2e(session: nox.Session) -> None:
    """Run e2e tests."""
    session.install("-e", ".", "--group=dev")
    session.run("pytest", "-m", "e2e")


@nox.session(python="3.11")
def tests(session: nox.Session) -> None:
    """Run all tests with coverage reporting."""
    session.install("-e", ".", "--group=dev")
    session.run(
        "pytest",
        "--cov=src/adraitools",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=80",
    )


@nox.session(python=PYTHON_VERSIONS)
def tests_all_versions(session: nox.Session) -> None:
    """Run all tests across all supported Python versions."""
    session.install("-e", ".", "--group=dev")
    session.run("pytest")


@nox.session(python="3.11")
def mypy(session: nox.Session) -> None:
    """Run mypy type checking."""
    session.install("-e", ".", "--group=dev")
    session.run("mypy", "src/", "tests/")


@nox.session(python="3.11")
def lint(session: nox.Session) -> None:
    """Run ruff linting."""
    session.install("-e", ".", "--group=dev")
    session.run("ruff", "check", ".")


@nox.session(python="3.11")
def format_code(session: nox.Session) -> None:
    """Run ruff formatting."""
    session.install("-e", ".", "--group=dev")
    session.run("ruff", "format", ".")


@nox.session(python="3.11")
def quality(session: nox.Session) -> None:
    """Run all code quality checks (mypy, ruff)."""
    session.install("-e", ".", "--group=dev")
    session.run("mypy", "src/", "tests/")
    session.run("ruff", "check", ".")


@nox.session(python="3.11")
def check_all(session: nox.Session) -> None:
    """Run all checks and tests."""
    session.install("-e", ".", "--group=dev")
    session.run("pytest")
    session.run("mypy", "src/", "tests/")
    session.run("ruff", "check", ".")
