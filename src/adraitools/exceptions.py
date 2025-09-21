"""Exceptions for the ADR AI Tools project."""

from pathlib import Path


class BaseError(Exception):
    """Base exception for the ADR AI Tools project."""


class ConfigurationFileCorruptedError(BaseError):
    """Exception for configuration file corruption."""

    def __init__(self, file_path: Path) -> None:
        """Initialize the exception."""
        super().__init__(f"Configuration file {file_path} is corrupted.")
        self.file_path = file_path
