import enum

from .. import events, log

logger = log.get_logger(name=__name__)


class InputEvents(enum.Enum):
    """
    Input events that can be emitted. They represent the state for each input button.
    """

    CENTER_BUTTON_PRESSED = enum.auto()
    LEFT_BUTTON_PRESSED = enum.auto()
    RIGHT_BUTTON_PRESSED = enum.auto()


class InputEventPublisher(events.EventPublisher):
    """
    The ``InputEventPublisher`` class is used to emit events regarding the
    input system to callback functions. This is useful as it allows for loose
    coupling between different components and reduces overall dependencies.

    Example use::

        import pypinball

        def callback_func(event):
            print("Running callback")

        publisher = pypinball.inputs.InputEventPublisher()
        publisher.subscribe(callback=callback_func)
        publisher.emit(InputEvents.CENTER_BUTTON_PRESSED)

        >>> Running callback
    """

    def __init__(self):
        super().__init__(event_type=InputEvents)
