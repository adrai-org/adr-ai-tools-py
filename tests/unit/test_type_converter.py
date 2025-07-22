"""Unit tests for type converter service."""

from pathlib import Path

import pytest

from adraitools.infrastructure.type_converter import TypeConverter


def test_convert_config_value_path_field() -> None:
    """Test conversion of Path field."""
    result = TypeConverter.convert_config_value("adr_directory", "test/path")
    assert isinstance(result, Path)
    assert result == Path("test/path")


def test_convert_config_value_string_field() -> None:
    """Test conversion of string field."""
    result = TypeConverter.convert_config_value("author_name", "Test Author")
    assert isinstance(result, str)
    assert result == "Test Author"


def test_convert_config_value_unknown_key() -> None:
    """Test conversion with unknown key raises KeyError."""
    with pytest.raises(KeyError, match="Unknown configuration key 'invalid_key'"):
        TypeConverter.convert_config_value("invalid_key", "value")


def test_convert_by_type_path() -> None:
    """Test conversion to Path type."""
    result = TypeConverter.convert_by_type("test/path", Path)
    assert isinstance(result, Path)
    assert result == Path("test/path")


def test_convert_by_type_string() -> None:
    """Test conversion to string type."""
    result = TypeConverter.convert_by_type("test value", str)
    assert isinstance(result, str)
    assert result == "test value"


def test_convert_by_type_int() -> None:
    """Test conversion to int type."""
    result = TypeConverter.convert_by_type("42", int)
    assert isinstance(result, int)
    expected = 42
    assert result == expected


def test_convert_by_type_float() -> None:
    """Test conversion to float type."""
    result = TypeConverter.convert_by_type("3.14", float)
    assert isinstance(result, float)
    assert result == pytest.approx(3.14)


def test_convert_by_type_bool_true() -> None:
    """Test conversion to bool type (true values)."""
    for value in ["true", "True", "1", "yes", "on"]:
        result = TypeConverter.convert_by_type(value, bool)
        assert isinstance(result, bool)
        assert result is True


def test_convert_by_type_bool_false() -> None:
    """Test conversion to bool type (false values)."""
    for value in ["false", "False", "0", "no", "off"]:
        result = TypeConverter.convert_by_type(value, bool)
        assert isinstance(result, bool)
        assert result is False


def test_convert_by_type_unknown_type() -> None:
    """Test conversion with unknown type returns string."""

    class CustomType:
        pass

    result = TypeConverter.convert_by_type("test", CustomType)  # type: ignore[arg-type]
    assert isinstance(result, str)
    assert result == "test"
