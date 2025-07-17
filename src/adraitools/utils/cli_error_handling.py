"""CLI error handling utilities."""

import sys
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import typer

F = TypeVar("F", bound=Callable[..., Any])


def handle_command_errors(func: F) -> F:
    """Decorator to handle common CLI command errors.

    Catches KeyError and other common exceptions and converts them to
    user-friendly error messages with appropriate exit codes.

    Args:
        func: CLI command function to wrap

    Returns:
        Wrapped function with error handling
    """

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            typer.echo(f"Error: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            typer.echo(f"Error: File not found - {e}")
            sys.exit(1)
        except PermissionError as e:
            typer.echo(f"Error: Permission denied - {e}")
            sys.exit(1)
        except (ValueError, TypeError, OSError) as e:
            typer.echo(f"Error: An unexpected error occurred - {e}")
            sys.exit(1)

    return wrapper  # type: ignore[return-value]


class CLIErrorHandler:
    """Centralized CLI error handling."""

    @staticmethod
    def handle_configuration_error(error: Exception) -> None:
        """Handle configuration-related errors.

        Args:
            error: The configuration error to handle
        """
        if isinstance(error, KeyError):
            typer.echo(f"Error: {error}")
        elif isinstance(error, FileNotFoundError):
            typer.echo(f"Error: Configuration file not found - {error}")
        elif isinstance(error, PermissionError):
            typer.echo(f"Error: Permission denied accessing configuration - {error}")
        else:
            typer.echo(f"Error: Configuration error - {error}")

        sys.exit(1)

    @staticmethod
    def handle_file_system_error(error: Exception) -> None:
        """Handle file system-related errors.

        Args:
            error: The file system error to handle
        """
        if isinstance(error, FileNotFoundError):
            typer.echo(f"Error: File or directory not found - {error}")
        elif isinstance(error, PermissionError):
            typer.echo(f"Error: Permission denied - {error}")
        elif isinstance(error, FileExistsError):
            typer.echo(f"Error: File or directory already exists - {error}")
        else:
            typer.echo(f"Error: File system error - {error}")

        sys.exit(1)
