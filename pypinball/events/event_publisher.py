import typing

from .. import log

logger = log.get_logger(name=__name__)


class EventPublisher:
    def __init__(self, event_type) -> None:
        self._event_type = event_type
        self._callbacks: typing.Set[typing.Callable] = set()

    @property
    def num_subscribers(self) -> int:
        return len(self._callbacks)

    def emit(self, event) -> None:
        logger.debug(f"Emitting event: {event}")
        if not isinstance(event, self._event_type):
            raise TypeError(
                f"Incorrect event type. Expecting {self._event_type}, got {type(event)}"
            )
        for callback in self._callbacks:
            callback(event)

    def subscribe(self, callback: typing.Callable) -> bool:
        if callback in self._callbacks:
            return False
        logger.info(f"Added event callback: {callback}")
        self._callbacks.add(callback)
        return True

    def unsubscribe(self, callback: typing.Callable) -> bool:
        if callback not in self._callbacks:
            return False
        logger.info(f"Removing event callback: {callback}")
        self._callbacks.remove(callback)
        return True
