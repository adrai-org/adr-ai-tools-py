"""Command-line interface for ADR AI Tools."""

import sys
from pathlib import Path
from typing import Annotated

import typer

from adraitools import __version__
from adraitools.cli.utils.cli_error_handling import handle_command_errors
from adraitools.infrastructure.configuration_service import ConfigurationService
from adraitools.infrastructure.file_system_service import FileSystemService
from adraitools.infrastructure.logging_service import LoggingService
from adraitools.infrastructure.user_interaction_service import UserInteractionService
from adraitools.services.adr_initializer import AdrInitializer
from adraitools.services.models.result import InitializationResult

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
    version: Annotated[  # noqa: ARG001
        bool,
        typer.Option(
            "--version", callback=version_callback, help="Show version and exit"
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option("--quiet", "-q", help="Suppress output"),
    ] = False,
    log_file: Annotated[
        str | None,
        typer.Option("--log-file", help="Log to file"),
    ] = None,
) -> None:
    """ADR AI Tools - Architecture Decision Records toolkit."""
    # Configure logging using LoggingService
    logging_service = LoggingService()
    logging_service.configure_logging(
        level="DEBUG" if verbose else "INFO",
        log_file=Path(log_file) if log_file else None,
        quiet=quiet,
    )


def main() -> None:
    """Main entry point for the CLI."""
    app()


@app.command()
def init() -> None:
    """Initialize ADR directory structure."""
    # Dependency injection - create service instances
    file_system_service = FileSystemService()
    user_interaction_service = UserInteractionService()
    configuration_service = ConfigurationService()
    initializer = AdrInitializer(
        file_system_service, user_interaction_service, configuration_service
    )

    # Execute initialization
    result = initializer.initialize()

    # Handle result and provide user feedback
    _handle_init_result(result, configuration_service)


def _handle_init_result(
    result: InitializationResult, configuration_service: ConfigurationService
) -> None:
    """Handle initialization result and provide appropriate user feedback."""
    if result.success:
        config = configuration_service.get_configuration()
        typer.echo(f"Created {config.adr_directory}/ directory")
        typer.echo(f"Generated template: {config.template_file}")
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
