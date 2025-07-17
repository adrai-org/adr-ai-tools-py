"""Type conversion service for configuration values."""

from pathlib import Path
from typing import get_origin

from adraitools.models.configuration import AdrConfiguration

T = Path | str | int | float | bool


class TypeConverter:
    """Service for converting string values to appropriate Python types."""

    @staticmethod
    def convert_config_value(key: str, value: str) -> T:
        """Convert string value to appropriate type based on configuration field type.

        Args:
            key: Configuration field name
            value: String value to convert

        Returns:
            Converted value with appropriate type

        Raises:
            KeyError: If key is not a valid configuration field
        """
        if not hasattr(AdrConfiguration, "__annotations__"):
            # Fallback to model_fields for Pydantic models
            if key not in AdrConfiguration.model_fields:
                msg = f"Unknown configuration key '{key}'"
                raise KeyError(msg)
            field_info = AdrConfiguration.model_fields[key]
            field_type = field_info.annotation
        else:
            # Use type annotations if available
            if key not in AdrConfiguration.__annotations__:
                msg = f"Unknown configuration key '{key}'"
                raise KeyError(msg)
            field_type = AdrConfiguration.__annotations__[key]

        return TypeConverter.convert_by_type(value, field_type)

    @staticmethod
    def convert_by_type(value: str, target_type: type[T] | None) -> T:
        """Convert string value to target type.

        Args:
            value: String value to convert
            target_type: Target type annotation

        Returns:
            Converted value
        """
        # Handle Path types
        if target_type == Path or get_origin(target_type) is Path:
            return Path(value)

        # Handle string types (no conversion needed)
        if target_type is str:
            return value

        # Handle int types
        if target_type is int:
            return int(value)

        # Handle float types
        if target_type is float:
            return float(value)

        # Handle bool types
        if target_type is bool:
            return value.lower() in ("true", "1", "yes", "on")

        # Default: return as string
        return value
