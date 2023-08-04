import logging

from . import log
from .events import GameEventPublisher, GameEvents

LOGGER = log.get_logger(name="scoring", level=logging.DEBUG)


class Scoring:
    """The ``Scoring`` class is used to calculate and keep track of the current game
    score. The intention is that it listens to the GameEvents and is updated as
    events occur."""

    def __init__(self) -> None:
        self._score = 0
        self._multiplier = 1.0

    @property
    def current_score(self) -> int:
        """
        Return the current score value.

        Returns:
            int: Score value.
        """
        return self._score

    @property
    def multiplier(self) -> float:
        """
        Get the current multiplier value.

        Returns:
            float: Multiplier.
        """
        return self._multiplier

    def event_callback(self, event: GameEvents) -> None:
        LOGGER.debug(f"Handing event: {event}, updating score...")
        if event != GameEvents.COLLISION_BALL_BUMPER:
            return
        self._score += int(self._multiplier * 1.0)
        LOGGER.debug(f"Score: {self.current_score}")

    def set_multiplier(self, value: float) -> None:
        """
        Set the multiplier value.

        Args:
            value (float): New value.
        """
        self._multiplier = value


def get_scorer(event_pub: GameEventPublisher) -> Scoring:
    """Create an instance of a ``Scoring`` class, and setup the subscription to the
    event publisher.

    Args:
        event_pub (GameEventPublisher): Event publisher to subscribe to for events.

    Returns:
        Scoring: New instance.
    """
    ret = Scoring()
    event_pub.subscribe(callback=ret.event_callback)
    return ret