"""Result models for operation outcomes.

Examples:
    >>> result = InitializationResult(success=True, message="Success")
    >>> result.success
    True
    >>> result.message
    'Success'

    >>> failure = InitializationResult(success=False, message="Failed")
    >>> failure.success
    False
    >>> failure.message
    'Failed'

    >>> # Test immutability
    >>> result.success = False  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValidationError: ...
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BaseResultModel(BaseModel):
    """Base class for result models."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)


class InitializationResult(BaseResultModel):
    """Result of ADR initialization operation."""

    success: bool = Field(description="Whether the initialization was successful")
    message: str = Field(description="Human-readable message describing the result")


class DiagnosisStepResult(BaseResultModel):
    """Result of a single diagnosis step."""

    step_name: Literal["CONFIG_VALIDATION", "LLM_CONNECTION"] = Field(
        description="Name of the diagnosis step"
    )
    result_level: Literal["PASS", "INFO", "WARNING", "FAIL"] = Field(
        description="Result level of the diagnosis step"
    )
    message: str = Field(...)

    @property
    def display_step_name(self) -> str:
        """Get a user-friendly name for the diagnosis step."""
        return {
            "CONFIG_VALIDATION": "Configuration Validation",
            "LLM_CONNECTION": "LLM Connection",
        }[self.step_name]

    @property
    def display_icon(self) -> str:
        """Get an icon representing the result level."""
        return {
            "PASS": "✅",
            "INFO": "ℹ️",  # noqa: RUF001
            "WARNING": "⚠️",
            "FAIL": "❌",
        }[self.result_level]

    @property
    def display_status(self) -> str:
        """Get a user-friendly status message."""
        return self.result_level

    @property
    def display_message(self) -> str:
        """Get a formatted message for display."""
        return (
            f"{self.display_icon} {self.display_step_name}:"
            f" {self.display_status} ({self.message})"
        )


class DiagnosisResult(BaseResultModel):
    """Result of ADR diagnosis operation."""

    success: bool = Field(description="Whether the diagnosis was successful")
    steps: list[DiagnosisStepResult] = Field(
        description="List of results for each diagnosis step"
    )
