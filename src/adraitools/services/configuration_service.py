"""Configuration management service."""

from pathlib import Path
from typing import Any, get_origin

import tomli
import tomli_w

from adraitools.models.configuration import AdrConfiguration


class ConfigurationService:
    """Service for managing application configuration."""

    def __init__(self) -> None:
        """Initialize the configuration service."""
        self.configuration = AdrConfiguration()

    def get_configuration(self) -> AdrConfiguration:
        """Get the complete configuration."""
        return self.configuration

    def get_value(self, key: str) -> str:
        """Get a specific configuration value as string for CLI display."""
        if not hasattr(self.configuration, key):
            msg = f"Unknown configuration key '{key}'"
            raise KeyError(msg)
        value = getattr(self.configuration, key)
        return str(value)

    def set_value(self, key: str, value: str, *, global_config: bool = False) -> None:
        """Set a configuration value."""
        if not hasattr(self.configuration, key):
            msg = f"Unknown configuration key '{key}'"
            raise KeyError(msg)

        # Convert string value to appropriate type based on field type
        field_info = AdrConfiguration.model_fields[key]
        field_type = field_info.annotation

        if field_type == Path or get_origin(field_type) is Path:
            converted_value: Any = Path(value)
        else:
            converted_value = value

        # Prepare config data for saving
        config_data = {key: str(converted_value)}

        # Choose config location based on global_config flag
        if global_config:
            # Global config directory
            config_dir = Path.home() / ".config" / "adr-ai-tools"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.toml"
        else:
            # Project-local config directory
            config_dir = Path.cwd() / ".adr-ai-tools"
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / "config.toml"

        # Load existing config if it exists
        existing_config: dict[str, Any] = {}
        if config_file.exists():
            with config_file.open("rb") as f:
                existing_config = tomli.load(f)

        # Update with new value
        existing_config.update(config_data)

        # Write back to file
        with config_file.open("wb") as f:
            tomli_w.dump(existing_config, f)
