"""TOML file handling service."""

from pathlib import Path
from typing import Any

import tomli
import tomli_w


class TomlFileHandler:
    """Service for handling TOML file operations."""

    @staticmethod
    def load_config(file_path: Path) -> dict[str, Any]:
        """Load configuration from TOML file.

        Args:
            file_path: Path to TOML file

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If file doesn't exist
            tomllib.TOMLDecodeError: If file contains invalid TOML
        """
        if not file_path.exists():
            return {}

        with file_path.open("rb") as f:
            return tomli.load(f)

    @staticmethod
    def save_config(config_data: dict[str, Any], file_path: Path) -> None:
        """Save configuration to TOML file with merge support.

        Args:
            config_data: Configuration dictionary to save
            file_path: Path to TOML file
        """
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing configuration
        existing_config = TomlFileHandler.load_config(file_path)

        # Merge with new data
        existing_config.update(config_data)

        # Write back to file
        with file_path.open("wb") as f:
            tomli_w.dump(existing_config, f)

    @staticmethod
    def update_config_value(key: str, value: str, file_path: Path) -> None:
        """Update a single configuration value in TOML file.

        Args:
            key: Configuration key
            value: String representation of value
            file_path: Path to TOML file
        """
        config_data = {key: value}
        TomlFileHandler.save_config(config_data, file_path)
