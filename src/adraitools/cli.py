"""Command-line interface for ADR AI Tools."""

import sys
from typing import Annotated

import typer

from adraitools import __version__
from adraitools.services.adr_initializer import AdrInitializer
from adraitools.services.file_system_service import FileSystemService
from adraitools.services.user_interaction_service import UserInteractionService

app = typer.Typer(help="ADR AI Tools - Architecture Decision Records toolkit")


def version_callback(*, value: bool) -> None:
    """Show version and exit."""
    if value:
        typer.echo(f"adr-ai-tools {__version__}")
        raise typer.Exit


@app.callback()
def callback(
    *,
    version: Annotated[
        bool,
        typer.Option(
            "--version", callback=version_callback, help="Show version and exit"
        ),
    ] = False,
) -> None:
    """ADR AI Tools - Architecture Decision Records toolkit."""


def main() -> None:
    """Main entry point for the CLI."""
    app()


@app.command()
def init() -> None:
    """Initialize ADR directory structure."""
    # Dependency injection - create service instances
    file_system_service = FileSystemService()
    user_interaction_service = UserInteractionService()
    initializer = AdrInitializer(file_system_service, user_interaction_service)

    # Execute initialization
    result = initializer.initialize()

    if result.success:
        typer.echo("Created docs/adr/ directory")
        typer.echo("Generated template: docs/adr/0000-adr-template.md")
        typer.echo(
            "Ready to create your first ADR with: "
            'adr-ai-tools new "Your decision title"'
        )
    elif "cancelled" in result.message.lower():
        typer.echo(result.message)
    else:
        typer.echo(f"Error: {result.message}")
        sys.exit(1)


if __name__ == "__main__":
    app()
