"""Logging service for application-wide logging operations."""

import logging
import sys
from pathlib import Path


class LoggingService:
    """Service for managing application logging operations."""

    def __init__(self) -> None:
        """Initialize the logging service."""
        self._configured = False
        self._default_logger: logging.Logger

    def configure_logging(
        self,
        level: str = "INFO",
        log_file: Path | None = None,
        format_string: str | None = None,
        *,
        quiet: bool = False,
    ) -> None:
        """Configure application logging settings.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for log output
            format_string: Optional custom log format
            quiet: Whether to suppress most log output
        """
        # Determine logging level
        if quiet:
            numeric_level = logging.CRITICAL
        else:
            numeric_level = getattr(logging, level.upper(), logging.INFO)

        # Set default format if not provided
        if format_string is None:
            format_string = "%(levelname)s: %(message)s"

        # Configure logging handlers
        handlers: list[logging.Handler] = []

        # Always add console handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(logging.Formatter(format_string))
        handlers.append(console_handler)

        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)  # Always log debug to file
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
            )
            handlers.append(file_handler)

        # Configure root logger
        logging.basicConfig(
            level=logging.DEBUG if log_file else numeric_level,
            handlers=handlers,
            force=True,  # Override any existing configuration
        )

        self._configured = True
        self._default_logger = logging.getLogger("adraitools")

        # Show debug message when debug logging is enabled
        if level.upper() == "DEBUG":
            self._default_logger.debug("Debug logging enabled")

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance for the specified name.

        Args:
            name: Logger name (typically module name)

        Returns:
            Configured logger instance
        """
        if not self._configured:
            self.configure_logging()

        return logging.getLogger(name)

    def _ensure_configured(self) -> None:
        """Ensure logging is configured and default logger is available."""
        if not self._configured:
            self.configure_logging()

    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        self._ensure_configured()
        self._default_logger.debug(message)

    def log_info(self, message: str) -> None:
        """Log an info message."""
        self._ensure_configured()
        self._default_logger.info(message)

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self._ensure_configured()
        self._default_logger.warning(message)

    def log_error(self, message: str) -> None:
        """Log an error message."""
        self._ensure_configured()
        self._default_logger.error(message)

    def log_critical(self, message: str) -> None:
        """Log a critical message."""
        self._ensure_configured()
        self._default_logger.critical(message)
