import typing

from .. import log

logger = log.get_logger(name=__name__)


class EventPublisher:
    """
    The ``EventPublisher`` class is a generic mechnaism that allows you to emit events
    and connect callback methods to those events.
    """

    def __init__(self, event_type) -> None:
        self._event_type = event_type
        self._callbacks: typing.Set[typing.Callable] = set()

    @property
    def num_subscribers(self) -> int:
        """Get the number of subscrber callback methods.

        Returns:
            int: Subscriber count.
        """
        return len(self._callbacks)

    def emit(self, event: typing.Any) -> None:
        """Emit an event. The ``event`` is expected to be an enum and should match
        the type passed to the class ``__init__()`` method.

        Args:
            event (Any): The event payload/identifier to emit.

        Raises:
            TypeError: If the ``event`` does not match the registered ``event_type``.
        """
        logger.debug(f"Emitting event: {event}")
        if not isinstance(event, self._event_type):
            raise TypeError(
                f"Incorrect event type. Expecting {self._event_type}, got {type(event)}"
            )
        for callback in self._callbacks:
            callback(event)

    def subscribe(self, callback: typing.Callable) -> bool:
        """Subscribe to events with a callback method.

        Args:
            callback (typing.Callable): Callback method.

        Returns:
            bool: ``True`` if the callback was added successfully else ``False``.
        """
        if callback in self._callbacks:
            return False
        logger.info(f"Added event callback: {callback}")
        self._callbacks.add(callback)
        return True

    def unsubscribe(self, callback: typing.Callable) -> bool:
        """Unsubscribe a callback method form events.

        Args:
            callback (typing.Callable): Callback method.

        Returns:
            bool: ``True`` if the callback was removed successfully else ``False``.
        """
        if callback not in self._callbacks:
            return False
        logger.info(f"Removing event callback: {callback}")
        self._callbacks.remove(callback)
        return True
