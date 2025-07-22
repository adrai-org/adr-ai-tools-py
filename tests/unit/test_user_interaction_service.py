"""Unit tests for user interaction service."""

from pytest_mock import MockerFixture

from adraitools.infrastructure.user_interaction_service import UserInteractionService


def test_ask_confirmation_returns_true_for_y(mocker: MockerFixture) -> None:
    """Test that ask_confirmation returns True when user inputs 'y'."""
    # Arrange
    service = UserInteractionService()
    mocker.patch("builtins.input", return_value="y")

    # Act
    result = service.ask_confirmation("Continue?")

    # Assert
    assert result is True


def test_ask_confirmation_returns_true_for_y_with_whitespace(
    mocker: MockerFixture,
) -> None:
    """Test that ask_confirmation returns True when user inputs 'y' with whitespace."""
    # Arrange
    service = UserInteractionService()
    mocker.patch("builtins.input", return_value=" y ")

    # Act
    result = service.ask_confirmation("Continue?")

    # Assert
    assert result is True


def test_ask_confirmation_returns_false_for_n(mocker: MockerFixture) -> None:
    """Test that ask_confirmation returns False when user inputs 'n'."""
    # Arrange
    service = UserInteractionService()
    mocker.patch("builtins.input", return_value="n")

    # Act
    result = service.ask_confirmation("Continue?")

    # Assert
    assert result is False


def test_ask_confirmation_returns_false_for_empty_input(mocker: MockerFixture) -> None:
    """Test that ask_confirmation returns False when user inputs nothing."""
    # Arrange
    service = UserInteractionService()
    mocker.patch("builtins.input", return_value="")

    # Act
    result = service.ask_confirmation("Continue?")

    # Assert
    assert result is False


def test_ask_confirmation_returns_false_for_invalid_input(
    mocker: MockerFixture,
) -> None:
    """Test that ask_confirmation returns False for invalid input."""
    # Arrange
    service = UserInteractionService()
    mocker.patch("builtins.input", return_value="maybe")

    # Act
    result = service.ask_confirmation("Continue?")

    # Assert
    assert result is False


def test_ask_confirmation_formats_message_correctly(mocker: MockerFixture) -> None:
    """Test that ask_confirmation formats the message with colon and space."""
    # Arrange
    service = UserInteractionService()
    mock_input = mocker.patch("builtins.input", return_value="y")

    # Act
    service.ask_confirmation("Do you want to continue")

    # Assert
    mock_input.assert_called_once_with("Do you want to continue: ")
