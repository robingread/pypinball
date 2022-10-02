import enum
import typing

from . import log

logger = log.get_logger(name=__name__)


class GameEvents(enum.Enum):
    BALL_LAUNCHED = enum.auto()
    BALL_LOST = enum.auto()
    COLLISION_BALL_BALL = enum.auto()
    COLLISION_BALL_BUMPER = enum.auto()
    COLLISION_BALL_FLIPPER = enum.auto()
    COLLISION_BALL_WALL = enum.auto()
    FLIPPER_ACTIVATED = enum.auto()
    GAME_OVER = enum.auto()
    GAME_STARTED = enum.auto()
    LIFE_LOST = enum.auto()
    QUIT = enum.auto()


class MockEventHandler:
    """
    Mock Event Handler class mainly intended for testing purposes. Internally
    this class keeps a record of all the events that have been received.
    """

    def __init__(self):
        self._events = list()

    @property
    def events(self) -> typing.List[GameEvents]:
        """
        Get the list of received events.

        Returns:
            list: Events.
        """
        return self._events

    def clear(self) -> None:
        """
        Clear the list of recorded events.

        Returns:
            None
        """
        self._events.clear()

    def handle_event(self, event: GameEvents) -> None:
        """
        Handle an event. This method will append the event to the internal
        list.

        Args:
            event (GameEvents): Event.

        Returns:
            None
        """
        self._events.append(event)


class GameEventPublisher:
    """
    Class for publishing different game events (see the GameEvent enums).
    """

    def __init__(self):
        self._callbacks: typing.Set[typing.Callable[[GameEvents], None]] = set()

    @property
    def num_subs(self) -> int:
        """
        Get the number of subscribed callback functions.

        Returns:
            int: Number of callbacks.
        """
        return len(self._callbacks)

    def emit(self, event: GameEvents) -> None:
        """
        Emit a game event to the registered subscribers.

        Args:
            event: Event to emit.

        Returns:
            None
        """
        logger.debug(f"Emitting event: {event}")
        for cb in self._callbacks:
            cb(event)

    def subscribe(self, callback: typing.Callable[[GameEvents], None]) -> bool:
        """
        Add a subscriber callback. This will be called each time the emit()
        method is called. If the subscriber is already registered this method
        will return False.

        Args:
            callback: Method/function to call.

        Returns:
            bool: Whether the callback was registered successfully.
        """
        if callback in self._callbacks:
            return False
        logger.info(f"Added event callback: {callback}")
        self._callbacks.add(callback)
        return True

    def unsubscribe(self, callback: typing.Callable[[GameEvents], None]) -> bool:
        """
        Remove a subscriber callback. If the subscriber is already registered
        this method will return False.

        Args:
            callback: Method/function to call.

        Returns:
            bool: Whether the callback was removed successfully.
        """
        if callback not in self._callbacks:
            return False
        logger.info(f"Removing event callback: {callback}")
        self._callbacks.remove(callback)
        return True
