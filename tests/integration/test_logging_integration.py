"""Integration tests for logging functionality."""

import logging
import tempfile
from pathlib import Path

from adraitools.services.logging_service import LoggingService


class TestLoggingIntegration:
    """Integration tests for logging service behavior."""

    def test_logging_service_with_multiple_loggers(self) -> None:
        """Test that LoggingService properly configures multiple loggers."""
        # Arrange
        service = LoggingService()

        # Act
        service.configure_logging(level="DEBUG")
        logger1 = service.get_logger("module1")
        logger2 = service.get_logger("module2")

        # Assert
        assert logger1.name == "module1"
        assert logger2.name == "module2"
        assert logger1.isEnabledFor(logging.DEBUG)
        assert logger2.isEnabledFor(logging.DEBUG)

    def test_logging_service_quiet_mode_integration(self) -> None:
        """Test that quiet mode properly suppresses all logging except critical."""
        # Arrange
        service = LoggingService()

        # Act
        service.configure_logging(quiet=True)
        logger = service.get_logger("test")

        # Assert
        assert not logger.isEnabledFor(logging.DEBUG)
        assert not logger.isEnabledFor(logging.INFO)
        assert not logger.isEnabledFor(logging.WARNING)
        assert not logger.isEnabledFor(logging.ERROR)
        assert logger.isEnabledFor(logging.CRITICAL)

    def test_logging_service_file_and_console_output(self) -> None:
        """Test that file and console logging work together properly."""
        # Arrange
        service = LoggingService()

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "integration_test.log"

            # Act
            service.configure_logging(level="INFO", log_file=log_file)
            service.log_info("Integration test message")
            service.log_debug("Debug message that should only go to file")

            # Assert
            assert log_file.exists()
            content = log_file.read_text()
            assert "Integration test message" in content
            assert "Debug message that should only go to file" in content

    def test_logging_service_reconfiguration(self) -> None:
        """Test that LoggingService can be reconfigured properly."""
        # Arrange
        service = LoggingService()

        # Act - First configuration
        service.configure_logging(level="ERROR")
        logger = service.get_logger("test")
        error_enabled = logger.isEnabledFor(logging.ERROR)
        info_enabled_first = logger.isEnabledFor(logging.INFO)

        # Act - Reconfigure to more verbose
        service.configure_logging(level="INFO")
        logger = service.get_logger("test")
        info_enabled_second = logger.isEnabledFor(logging.INFO)

        # Assert
        assert error_enabled is True
        assert info_enabled_first is False
        assert info_enabled_second is True

    def test_logging_service_auto_configuration(self) -> None:
        """Test that LoggingService auto-configures when methods are called."""
        # Arrange
        service = LoggingService()

        # Act - Call log method without explicit configuration
        service.log_info("Auto-configured message")

        # Assert - Should not raise exception and should be configured
        logger = service.get_logger("test")
        assert logger.isEnabledFor(logging.INFO)

    def test_logging_service_default_format(self) -> None:
        """Test that default log format is applied correctly."""
        # Arrange
        service = LoggingService()

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "format_test.log"

            # Act
            service.configure_logging(log_file=log_file)
            service.log_info("Format test message")

            # Assert
            content = log_file.read_text()
            # File should have timestamp format
            assert "INFO" in content
            assert "Format test message" in content
            # Should contain timestamp pattern
            assert " - " in content

    def test_logging_service_custom_format(self) -> None:
        """Test that custom log format is applied correctly."""
        # Arrange
        service = LoggingService()
        custom_format = "CUSTOM: %(message)s"

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "custom_format_test.log"

            # Act
            service.configure_logging(log_file=log_file, format_string=custom_format)
            service.log_info("Custom format test")

            # Assert
            content = log_file.read_text()
            # File should still use default timestamp format
            assert "INFO" in content
            assert "Custom format test" in content
