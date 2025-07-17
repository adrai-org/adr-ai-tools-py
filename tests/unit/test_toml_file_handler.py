"""Unit tests for TOML file handler service."""

from pathlib import Path

from adraitools.services.toml_file_handler import TomlFileHandler


def test_load_config_existing_file(isolated_filesystem: Path) -> None:
    """Test loading configuration from existing TOML file."""
    config_file = isolated_filesystem / "config.toml"
    config_file.write_text('adr_directory = "test/adr"\nauthor_name = "Test Author"')

    result = TomlFileHandler.load_config(config_file)

    assert result == {"adr_directory": "test/adr", "author_name": "Test Author"}


def test_load_config_nonexistent_file(isolated_filesystem: Path) -> None:
    """Test loading configuration from non-existent file returns empty dict."""
    config_file = isolated_filesystem / "nonexistent.toml"

    result = TomlFileHandler.load_config(config_file)

    assert result == {}


def test_save_config_new_file(isolated_filesystem: Path) -> None:
    """Test saving configuration to new file."""
    config_file = isolated_filesystem / "config.toml"
    config_data = {"adr_directory": "test/adr", "author_name": "Test Author"}

    TomlFileHandler.save_config(config_data, config_file)

    assert config_file.exists()
    result = TomlFileHandler.load_config(config_file)
    assert result == config_data


def test_save_config_merge_existing(isolated_filesystem: Path) -> None:
    """Test saving configuration merges with existing file."""
    config_file = isolated_filesystem / "config.toml"

    # Create initial config
    initial_data = {"adr_directory": "old/adr", "author_name": "Old Author"}
    TomlFileHandler.save_config(initial_data, config_file)

    # Update with new data
    new_data = {"adr_directory": "new/adr"}
    TomlFileHandler.save_config(new_data, config_file)

    # Verify merge
    result = TomlFileHandler.load_config(config_file)
    expected = {"adr_directory": "new/adr", "author_name": "Old Author"}
    assert result == expected


def test_save_config_creates_parent_directory(isolated_filesystem: Path) -> None:
    """Test saving configuration creates parent directories."""
    config_file = isolated_filesystem / "nested" / "dir" / "config.toml"
    config_data = {"adr_directory": "test/adr"}

    TomlFileHandler.save_config(config_data, config_file)

    assert config_file.exists()
    assert config_file.parent.exists()


def test_update_config_value(isolated_filesystem: Path) -> None:
    """Test updating a single configuration value."""
    config_file = isolated_filesystem / "config.toml"

    # Create initial config
    initial_data = {"adr_directory": "old/adr", "author_name": "Test Author"}
    TomlFileHandler.save_config(initial_data, config_file)

    # Update single value
    TomlFileHandler.update_config_value("adr_directory", "new/adr", config_file)

    # Verify update
    result = TomlFileHandler.load_config(config_file)
    expected = {"adr_directory": "new/adr", "author_name": "Test Author"}
    assert result == expected
