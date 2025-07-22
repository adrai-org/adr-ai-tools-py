"""Application constants."""

from pathlib import Path


class PathConstants:
    """File and directory path constants."""

    # Default ADR paths
    DEFAULT_ADR_DIRECTORY = Path("docs/adr")
    DEFAULT_TEMPLATE_FILE = Path("docs/adr/0000-adr-template.md")

    # Configuration paths
    LOCAL_CONFIG_DIR = ".adr-ai-tools"
    GLOBAL_CONFIG_DIR = Path(".config") / "adr-ai-tools"
    CONFIG_FILE = "config.toml"

    @classmethod
    def get_local_config_dir(cls, project_root: Path | None = None) -> Path:
        """Get project-local configuration directory."""
        base = project_root or Path.cwd()
        return base / cls.LOCAL_CONFIG_DIR

    @classmethod
    def get_global_config_dir(cls, home_dir: Path | None = None) -> Path:
        """Get global configuration directory."""
        base = home_dir or Path.home()
        return base / cls.GLOBAL_CONFIG_DIR

    @classmethod
    def get_local_config_file(cls, project_root: Path | None = None) -> Path:
        """Get project-local configuration file path."""
        return cls.get_local_config_dir(project_root) / cls.CONFIG_FILE

    @classmethod
    def get_global_config_file(cls, home_dir: Path | None = None) -> Path:
        """Get global configuration file path."""
        return cls.get_global_config_dir(home_dir) / cls.CONFIG_FILE


class ErrorMessages:
    """Standard error message templates."""

    UNKNOWN_CONFIG_KEY = "Unknown configuration key '{key}'"
