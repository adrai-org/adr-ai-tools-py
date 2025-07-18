"""Unit tests for logging service."""

import logging
import tempfile
from pathlib import Path

from adraitools.services.logging_service import LoggingService


def test_configure_logging_sets_default_level() -> None:
    """Test that configure_logging sets default INFO level."""
    # Arrange
    service = LoggingService()

    # Act
    service.configure_logging()

    # Assert
    logger = service.get_logger("test")
    assert logger.isEnabledFor(logging.INFO)


def test_configure_logging_accepts_custom_level() -> None:
    """Test that configure_logging accepts custom logging level."""
    # Arrange
    service = LoggingService()

    # Act
    service.configure_logging(level="DEBUG")

    # Assert
    logger = service.get_logger("test")
    assert logger.isEnabledFor(logging.DEBUG)


def test_configure_logging_with_file_output() -> None:
    """Test that configure_logging configures file output."""
    # Arrange
    service = LoggingService()

    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test.log"

        # Act
        service.configure_logging(log_file=log_file)
        service.log_info("Test message")

        # Assert
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content


def test_get_logger_returns_configured_logger() -> None:
    """Test that get_logger returns properly configured logger."""
    # Arrange
    service = LoggingService()
    service.configure_logging()

    # Act
    logger = service.get_logger("test_logger")

    # Assert
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_log_info_calls_logger_info() -> None:
    """Test that log_info calls the logger info method."""
    # Arrange
    service = LoggingService()

    # Act & Assert - Should not raise an exception
    service.log_info("Test info message")


def test_log_debug_calls_logger_debug() -> None:
    """Test that log_debug calls the logger debug method."""
    # Arrange
    service = LoggingService()

    # Act & Assert - Should not raise an exception
    service.log_debug("Test debug message")


def test_log_warning_calls_logger_warning() -> None:
    """Test that log_warning calls the logger warning method."""
    # Arrange
    service = LoggingService()

    # Act & Assert - Should not raise an exception
    service.log_warning("Test warning message")


def test_log_error_calls_logger_error() -> None:
    """Test that log_error calls the logger error method."""
    # Arrange
    service = LoggingService()

    # Act & Assert - Should not raise an exception
    service.log_error("Test error message")


def test_log_critical_calls_logger_critical() -> None:
    """Test that log_critical calls the logger critical method."""
    # Arrange
    service = LoggingService()

    # Act & Assert - Should not raise an exception
    service.log_critical("Test critical message")
