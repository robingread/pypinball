import pypinball
import pytest


class Handler:
    def __init__(self):
        self.events = list()

    def handle_input(self, event: pypinball.inputs.InputEvents) -> None:
        self.events.append(event)


@pytest.fixture()
def handler():
    return Handler()


@pytest.fixture()
def publisher():
    return pypinball.inputs.InputEventPublisher()


def test_handler_init(handler):
    assert len(handler.events) == 0


def test_handler_callback(handler):
    exp = [
        pypinball.inputs.InputEvents.CENTER_BUTTON_PRESSED,
        pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
        pypinball.inputs.InputEvents.RIGHT_BUTTON_PRESSED,
    ]
    for e in exp:
        handler.handle_input(event=e)
    assert len(handler.events) == len(exp)
    assert all([a == b for a, b in zip(handler.events, exp)])


def test_input_event_publisher_init(publisher):
    assert publisher.num_callbacks == 0


def test_input_event_publisher_subscribe_callback(handler, publisher):
    res = publisher.subscribe(callback=handler.handle_input)
    assert res is True
    assert publisher.num_callbacks == 1


def test_input_event_publisher_subscribe_callback_twice(handler, publisher):
    res = publisher.subscribe(callback=handler.handle_input)
    assert res is True
    assert publisher.num_callbacks == 1

    res = publisher.subscribe(callback=handler.handle_input)
    assert res is False
    assert publisher.num_callbacks == 1


def test_input_event_publisher_unsubscribe_known_callback(handler, publisher):
    publisher.subscribe(callback=handler.handle_input)
    res = publisher.unsubscribe(handler.handle_input)
    assert res is True
    assert publisher.num_callbacks == 0


def test_input_event_publisher_unsubscribe_unknown_callback(handler, publisher):
    res = publisher.unsubscribe(handler.handle_input)
    assert res is False
    assert publisher.num_callbacks == 0


def test_input_event_emit_events(handler, publisher):
    publisher.subscribe(callback=handler.handle_input)
    publisher.emit(event=pypinball.inputs.InputEvents.CENTER_BUTTON_PRESSED)
    assert len(handler.events) == 1
    assert handler.events == [pypinball.inputs.InputEvents.CENTER_BUTTON_PRESSED]
