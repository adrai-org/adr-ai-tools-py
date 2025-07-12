"""Nox configuration file for adr-ai-tools."""

import nox

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.11"])
def lint_code(session: nox.Session) -> None:
    """Run the linter."""
    session.install("-e", ".", "--group=dev")
    session.run("ruff", "check", ".")


@nox.session(python=["3.11"])
def format_code(session: nox.Session) -> None:
    """Run the formatter."""
    session.install("-e", ".", "--group=dev")
    session.run("ruff", "format", ".")
