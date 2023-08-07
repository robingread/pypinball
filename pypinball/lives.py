from .events import GameEvents


class Lives:
    """The Lives class is used to track the current number of lives that the player
    has left in the game. It has a callback method that should be used to subscribe to
    GameEvents and handle the scenario in which a ball is lost.
    """

    def __init__(self, lives: int) -> None:
        self._lives = lives

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
        if event == GameEvents.BALL_LOST:
            self._lives -= 1
