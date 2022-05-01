import dataclasses
from .buttons import Buttons


@dataclasses.dataclass(frozen=True)
class FlipperConfig:
    """
    Flipper configuration dataclass. Flippers have the following properties:

    - position (tuple): Position in the format (x, y).
    - length (float): Length of the flipper arm.
    - rest_angle (float):
    - actuation_angle (float):
    - actuation_button (Buttons): Button that actuates the flipper.
    - actuation_direction (int): Direction the flipper actuates in. 1 corresponds to counter clockwise and -1 clockwise.
    """

    position: tuple
    length: float
    rest_angle: float
    actuation_angle: float
    actuation_button: Buttons
    actuation_direction: int


class Flipper:
    def __init__(self, uid: int, config: FlipperConfig):
        self._uid = uid
        self._angle = config.min_angle
        self._config = config

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def config(self) -> FlipperConfig:
        return self._config

    @property
    def uid(self) -> int:
        return self._uid
