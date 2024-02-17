from .events import GameEventPublisher, GameEvents
from .log import get_logger

LOGGER = get_logger(name="Lives")


class Lives:
    """The Lives class is used to track the current number of lives that the player
    has left in the game. It has a callback method that should be used to subscribe to
    GameEvents and handle the scenario in which a ball is lost.
    """

    def __init__(self, lives: int, event_pub: GameEventPublisher) -> None:
        self._lives = lives
        self._pub = event_pub

    def get_lives(self) -> int:
        """Get the number of remaining lives that remain.

        Returns:
            int: Number of lives.
        """
        return self._lives

    def event_callback(self, event: GameEvents) -> None:
        """Callback method used to handle ``GameEvents``. In the case of a
        ``GameEvents.BALL_LOST`` event, this will reduce the number of lives left.

        Args:
            event (GameEvents): Game event to handle
        """
        if self._lives == 0:
            return

        if event != GameEvents.BALL_LOST:
            return

        self._lives -= 1

        if self._lives > 0:
            return
        self._pub.emit(event=GameEvents.GAME_OVER)
