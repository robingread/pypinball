"""
Test the events.py module.
"""

import pypinball
import pytest


class MockSubscriber:
    def __init__(self):
        self._events_called = list()
        self.called = False

    def update(self, event: pypinball.events.GameEvents) -> None:
        self._events_called.append(event)
        self.called = True


@pytest.fixture
def mock_sub():
    return MockSubscriber()


@pytest.fixture
def game_event_pub():
    return pypinball.events.GameEventPublisher()


def test_new_game_event_pub(game_event_pub):
    assert game_event_pub.num_subs == 0


def test_register_new_callback(mock_sub, game_event_pub):
    assert game_event_pub.subscribe(callback=mock_sub.update) is True
    assert game_event_pub.num_subs == 1


def test_register_same_callback_twice(game_event_pub, mock_sub):
    game_event_pub.subscribe(callback=mock_sub.update)
    assert game_event_pub.subscribe(callback=mock_sub.update) is False
    assert game_event_pub.num_subs == 1


def test_unregister_known_callback(game_event_pub, mock_sub):
    game_event_pub.subscribe(callback=mock_sub.update)
    assert game_event_pub.unsubscribe(callback=mock_sub.update) is True
    assert game_event_pub.num_subs == 0


def test_attempt_unregister_unknown_callback(game_event_pub, mock_sub):
    assert game_event_pub.unsubscribe(callback=mock_sub.update) is False
    assert game_event_pub.num_subs == 0


def test_emit_event_to_registered_callback(game_event_pub, mock_sub):
    game_event_pub.subscribe(callback=mock_sub.update)
    game_event_pub.emit(pypinball.events.GameEvents.GAME_STARTED)
    assert mock_sub.called is True


def test_emit_event_to_unregistered_callback(game_event_pub, mock_sub):
    game_event_pub.emit(pypinball.events.GameEvents.GAME_STARTED)
    assert mock_sub.called is False
