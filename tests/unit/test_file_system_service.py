"""Unit tests for file system service."""

import tempfile
from pathlib import Path

from adraitools.infrastructure.file_system_service import FileSystemService


def test_directory_exists_returns_true_for_existing_directory() -> None:
    """Test that directory_exists returns True for existing directory."""
    # Arrange
    service = FileSystemService()

    with tempfile.TemporaryDirectory() as tmpdir:
        existing_dir = Path(tmpdir) / "existing"
        existing_dir.mkdir()

        # Act
        result = service.directory_exists(existing_dir)

        # Assert
        assert result is True


def test_directory_exists_returns_false_for_nonexistent_directory() -> None:
    """Test that directory_exists returns False for nonexistent directory."""
    # Arrange
    service = FileSystemService()
    nonexistent_dir = Path("/nonexistent/directory")

    # Act
    result = service.directory_exists(nonexistent_dir)

    # Assert
    assert result is False


def test_directory_exists_returns_false_for_file() -> None:
    """Test that directory_exists returns False for file path."""
    # Arrange
    service = FileSystemService()

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "file.txt"
        file_path.write_text("content")

        # Act
        result = service.directory_exists(file_path)

        # Assert
        assert result is False


def test_create_directory_creates_new_directory() -> None:
    """Test that create_directory creates a new directory."""
    # Arrange
    service = FileSystemService()

    with tempfile.TemporaryDirectory() as tmpdir:
        new_dir = Path(tmpdir) / "new_directory"

        # Act
        service.create_directory(new_dir)

        # Assert
        assert new_dir.exists()
        assert new_dir.is_dir()


def test_create_directory_creates_nested_directories() -> None:
    """Test that create_directory creates nested directories."""
    # Arrange
    service = FileSystemService()

    with tempfile.TemporaryDirectory() as tmpdir:
        nested_dir = Path(tmpdir) / "parent" / "child" / "grandchild"

        # Act
        service.create_directory(nested_dir)

        # Assert
        assert nested_dir.exists()
        assert nested_dir.is_dir()


def test_create_directory_handles_existing_directory() -> None:
    """Test that create_directory handles existing directory gracefully."""
    # Arrange
    service = FileSystemService()

    with tempfile.TemporaryDirectory() as tmpdir:
        existing_dir = Path(tmpdir) / "existing"
        existing_dir.mkdir()

        # Act - should not raise exception
        service.create_directory(existing_dir)

        # Assert
        assert existing_dir.exists()
        assert existing_dir.is_dir()


def test_create_template_file_creates_file_with_content() -> None:
    """Test that create_template_file creates file with correct content."""
    # Arrange
    service = FileSystemService()

    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = Path(tmpdir) / "template.md"

        # Act
        service.create_template_file(template_path)

        # Assert
        assert template_path.exists()
        assert template_path.is_file()

        content = template_path.read_text()
        assert "# Architecture Decision Record (ADR)" in content
        assert "## Title" in content
        assert "## Status" in content
        assert "## Date" in content
        assert "## Context" in content
        assert "## Decision" in content


def test_create_template_file_overwrites_existing_file() -> None:
    """Test that create_template_file overwrites existing file."""
    # Arrange
    service = FileSystemService()

    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = Path(tmpdir) / "template.md"
        template_path.write_text("old content")

        # Act
        service.create_template_file(template_path)

        # Assert
        content = template_path.read_text()
        assert "old content" not in content
        assert "# Architecture Decision Record (ADR)" in content
