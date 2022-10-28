import enum
import typing

from .. import log

logger = log.get_logger(name=__name__)


class InputEvents(enum.Enum):
    """
    Input events that can be emitted. They represent the state for each input button.
    """

    CENTER_BUTTON_PRESSED = enum.auto()
    LEFT_BUTTON_PRESSED = enum.auto()
    RIGHT_BUTTON_PRESSED = enum.auto()


class InputEventPublisher:
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
        self._callbacks = set()

    ##############
    # Properties #
    ##############
    @property
    def num_callbacks(self) -> int:
        """
        Get the number of registered callbacks.

        Returns:
            int: Number of callbacks.
        """
        return len(self._callbacks)

    ##################
    # Public Methods #
    ##################
    def emit(self, event: InputEvents) -> None:
        """
        Emit an event to the subscribers.

        Args:
            event (InputEvents): Event to emit.
        """
        logger.debug(f"Emitting event: {event}")
        for callback in self._callbacks:
            callback(event)

    def subscribe(self, callback: typing.Callable[[InputEvents], None]) -> bool:
        """
        Subscribe a handler callback function. If the callback is already registered then this method returns ``False``.

        Args:
            callback: Callback function.

        Returns:
            bool: Whether the callback was added successfully.
        """
        if callback in self._callbacks:
            return False
        logger.info(f"Added event callback: {callback}")
        self._callbacks.add(callback)
        return True

    def unsubscribe(self, callback: typing.Callable[[InputEvents], None]) -> bool:
        """
        Unsubscribe a handler callback function. If the callback is not already registered then this method returns ``False``.

        Args:
            callback: Callback function.

        Returns:
            bool: Whether the callback was removed successfully.
        """
        if callback not in self._callbacks:
            return False
        logger.info(f"Removing event callback: {callback}")
        self._callbacks.remove(callback)
        return True
