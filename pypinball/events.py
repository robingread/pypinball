import abc
import enum
import logging
import typing


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


# TODO: Add unit-tests for this class.
class MockEventHandler:
    def __init__(self):
        self._events = list()

    @property
    def events(self) -> typing.List[GameEvents]:
        return self._events

    def handle_event(self, event: GameEvents) -> None:
        self._events.append(event)


class GameEventPublisher:
    """
    Class for publishing different game events (see the GameEvent enums).
    """

    def __init__(self):
        self._callbacks: typing.Set[typing.Callable[[GameEvents], None]] = set()

    @property
    def num_subs(self) -> int:
        return len(self._callbacks)

    def emit(self, event: GameEvents) -> None:
        """
        Emit a game event to the registered subscribers.

        Args:
            event: Event to emit.

        Returns:
            None
        """
        logging.debug(f"Emitting event: {event}")
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
        logging.info(f"Added event callback: {callback}")
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
        logging.info(f"Removing event callback: {callback}")
        self._callbacks.remove(callback)
        return True
