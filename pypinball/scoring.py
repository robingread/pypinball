from . import log
from .events import GameEventPublisher, GameEvents

LOGGER = log.get_logger(name=__name__)


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
        """Callback method for handling GameEvents. The intention is that this method
        is used to subscribe to GameEvents via an instance of a GameEVentPublisher.

        When a GameEvents.COLLISION_BALL_BUMPER event occurs, the internal score count
        is increased based upon the multiplier amount.

        Args:
            event (GameEvents): Event to handle.
        """
        LOGGER.debug(f"Handing event: {event}, updating score...")
        if event != GameEvents.COLLISION_BALL_BUMPER:
            return
        new_score = self._score + int(self._multiplier * 1.0)
        self.set_score(value=new_score)
        LOGGER.debug(f"Score: {self.current_score}")

    def reset(self) -> None:
        """Reset the score back to zero."""
        LOGGER.debug("Resetting the score.")
        self.set_score(value=0)

    def set_multiplier(self, value: float) -> None:
        """
        Set the multiplier value.

        Args:
            value (float): New value.
        """
        self._multiplier = value

    def set_score(self, value: int) -> None:
        """Set the current score value.

        Args:
            value (int): Value to set the score to.
        """
        LOGGER.debug(f"Setting a new score value: {value}")
        self._score = int(value)


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
