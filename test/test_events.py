"""
Test the events.py module.
"""

import unittest.mock

import pytest

import pypinball


@pytest.fixture
def mock_sub():
    return unittest.mock.MagicMock()


@pytest.fixture
def game_event_pub():
    return pypinball.events.GameEventPublisher()


def test_new_game_event_pub(game_event_pub):
    assert game_event_pub.num_subscribers == 0


def test_register_new_callback(mock_sub, game_event_pub):
    assert game_event_pub.subscribe(callback=mock_sub) is True
    assert game_event_pub.num_subscribers == 1


def test_register_same_callback_twice(game_event_pub, mock_sub):
    game_event_pub.subscribe(callback=mock_sub)
    assert game_event_pub.subscribe(callback=mock_sub) is False
    assert game_event_pub.num_subscribers == 1


def test_unregister_known_callback(game_event_pub, mock_sub):
    game_event_pub.subscribe(callback=mock_sub)
    assert game_event_pub.unsubscribe(callback=mock_sub) is True
    assert game_event_pub.num_subscribers == 0


def test_attempt_unregister_unknown_callback(game_event_pub, mock_sub):
    assert game_event_pub.unsubscribe(callback=mock_sub) is False
    assert game_event_pub.num_subscribers == 0


def test_emit_event_to_registered_callback(game_event_pub, mock_sub):
    game_event_pub.subscribe(callback=mock_sub)
    game_event_pub.emit(pypinball.events.GameEvents.GAME_STARTED)
    # assert len(mock_sub.events) == 1
    mock_sub.assert_called_once_with(pypinball.events.GameEvents.GAME_STARTED)


def test_emit_event_to_unregistered_callback(game_event_pub, mock_sub):
    game_event_pub.emit(pypinball.events.GameEvents.GAME_STARTED)
    # assert len(mock_sub.events) == 0
    mock_sub.assert_not_called()
