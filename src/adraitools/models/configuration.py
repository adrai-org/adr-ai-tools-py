"""Configuration data models."""

from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class AdrConfiguration(BaseSettings):
    """Configuration settings for ADR AI Tools."""

    model_config = SettingsConfigDict(
        env_prefix="ADRAI_",
        case_sensitive=False,
        extra="forbid",  # Strict validation - forbid extra keys (ADR-0019)
        frozen=True,
        str_strip_whitespace=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize settings sources to include TOML files."""
        config_files = []

        # Project-local configuration (highest precedence)
        current_dir = Path.cwd()
        project_config = current_dir / ".adr-ai-tools" / "config.toml"
        if project_config.exists():
            config_files.append(project_config)

        # Global configuration (lower precedence)
        home_dir = Path.home()
        global_config = home_dir / ".config" / "adr-ai-tools" / "config.toml"
        if global_config.exists():
            config_files.append(global_config)

        toml_sources = []
        for config_file in config_files:
            try:
                toml_source = TomlConfigSettingsSource(
                    settings_cls, toml_file=config_file
                )
                toml_sources.append(toml_source)
            finally:
                pass

        return (
            init_settings,
            env_settings,
            *toml_sources,
            dotenv_settings,
            file_secret_settings,
        )

    adr_directory: Path = Path("docs/adr")
    template_file: Path = Path("docs/adr/0000-adr-template.md")
    author_name: str = ""
