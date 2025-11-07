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

from pydantic import BaseModel, ConfigDict, Field


class BaseResultModel(BaseModel):
    """Base class for result models."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)


class InitializationResult(BaseResultModel):
    """Result of ADR initialization operation."""

    success: bool = Field(description="Whether the initialization was successful")
    message: str = Field(description="Human-readable message describing the result")


class DiagnosisResult(BaseResultModel):
    """Result of ADR diagnosis operation."""

    success: bool = Field(description="Whether the diagnosis was successful")
    message: str = Field(description="Human-readable message describing the result")
