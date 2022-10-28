import dataclasses
import typing


class Ball:
    """
    Model of a ball object. Balls have a position value in the form of a
    tuple (x, y) and a historical record of the last X positions which is
    defined by the ``history`` parameter passed during initialisation.
    """

    def __init__(self, uid: int, position: typing.Tuple[float, float], history=15):
        self._uid = uid
        self._history = history
        self._position = position
        self._position_history = list()

    @property
    def uid(self) -> int:
        return self._uid

    @property
    def position(self) -> typing.Tuple[float, float]:
        """
        Get the current ball position.

        Returns:
            tuple: Position in the format (x, y).
        """
        return self._position

    @property
    def position_history(self) -> typing.List[typing.Tuple[float, float]]:
        """
        Get the position history. First elements are the newest positions and
        age increases with index.

        Returns:
            list: List of positions in the format [(x, y), (x, y)]
        """
        return self._position_history

    def set_position(self, position: typing.Tuple[float, float]) -> None:
        """
        Set the current position of the ball. This will also update the
        position history.

        Args:
            position (tuple): Position in the format (x, y).
        """
        self._position_history.insert(0, self._position)
        if len(self._position_history) > self._history:
            self._position_history = self.position_history[: self._history]
        self._position = position


@dataclasses.dataclass
class BallState:
    uid: int
    position: typing.Tuple[float, float]
