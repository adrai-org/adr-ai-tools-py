"""Command-line interface for ADR AI Tools."""

import sys
from typing import Annotated

import typer

from adraitools import __version__
from adraitools.services.adr_initializer import AdrInitializer
from adraitools.services.configuration_service import ConfigurationService
from adraitools.services.file_system_service import FileSystemService
from adraitools.services.user_interaction_service import UserInteractionService
from adraitools.utils.cli_error_handling import handle_command_errors

app = typer.Typer(help="ADR AI Tools - Architecture Decision Records toolkit")
config_app = typer.Typer(help="Configuration management commands")
app.add_typer(config_app, name="config")


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


@config_app.command(name="list")
def list_config() -> None:
    """List all configuration values."""
    config_service = ConfigurationService()
    config = config_service.get_configuration()

    typer.echo(f"adr_directory: {config.adr_directory}")
    typer.echo(f"template_file: {config.template_file}")
    typer.echo(f"author_name: {config.author_name}")


@config_app.command()
@handle_command_errors
def get(key: str) -> None:
    """Get a specific configuration value."""
    config_service = ConfigurationService()
    value = config_service.get_value(key)
    typer.echo(str(value))


@config_app.command(name="set")
@handle_command_errors
def set_config(
    key: str,
    value: str,
    *,
    global_config: bool = typer.Option(
        False,  # noqa: FBT003
        "--global",
        help="Set configuration globally instead of project-local",
    ),
) -> None:
    """Set a configuration value."""
    config_service = ConfigurationService()
    config_service.set_value(key, value, global_config=global_config)
    scope = "global" if global_config else "project-local"
    typer.echo(f"Configuration updated ({scope}): {key} = {value}")


if __name__ == "__main__":
    app()
