"""Configuration management service."""

from adraitools.constants import ErrorMessages, PathConstants
from adraitools.models.configuration import AdrConfiguration
from adraitools.services.toml_file_handler import TomlFileHandler
from adraitools.services.type_converter import TypeConverter


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
            msg = ErrorMessages.UNKNOWN_CONFIG_KEY.format(key=key)
            raise KeyError(msg)
        value = getattr(self.configuration, key)
        return str(value)

    def set_value(self, key: str, value: str, *, global_config: bool = False) -> None:
        """Set a configuration value."""
        if not hasattr(self.configuration, key):
            msg = ErrorMessages.UNKNOWN_CONFIG_KEY.format(key=key)
            raise KeyError(msg)

        # Convert string value to appropriate type and back to string for storage
        converted_value = TypeConverter.convert_config_value(key, value)

        # Choose config file location
        config_file = (
            PathConstants.get_global_config_file()
            if global_config
            else PathConstants.get_local_config_file()
        )

        # Save to TOML file
        TomlFileHandler.update_config_value(key, str(converted_value), config_file)
