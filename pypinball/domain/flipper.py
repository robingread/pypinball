import dataclasses
import typing

from ..inputs import InputEvents


@dataclasses.dataclass(frozen=True)
class FlipperConfig:
    """
    Flipper configuration dataclass. Flippers have the following properties:

    - position (tuple): Position in the format (x, y) in the world coordinates. This should represent the point of rotation of the flipper.
    - angle (float): Angle of the flipper in the world coordinates.
    - length (float): Length of the flipper arm.
    - actuation_angle (float):
    - actuation_direction (int): Direction the flipper actuates in. 1 corresponds to counter clockwise and -1 clockwise.
    """

    position: tuple
    angle: float
    length: float
    actuation_angle: float
    actuation_direction: int
    actuation_input: InputEvents


class Flipper:
    """
    Flipper class used to store the (static) configuration data as well as
    the dynamic data which changes as Flippers are actuated via the Physics
    implementation.
    """

    def __init__(self, uid: int, config: FlipperConfig):
        self._uid = uid
        self._config = config

    @property
    def config(self) -> FlipperConfig:
        """
        Get the flipper config.

        Returns:
            FlipperConfig: The flipper config data.
        """
        return self._config

    @property
    def uid(self) -> int:
        """
        Get the flipper unique ID.

        Returns:
            int: Unique ID.
        """
        return self._uid


@dataclasses.dataclass
class FlipperState:
    """
    State of the flipper, including the position and angle in the world frame.
    """

    uid: int
    angle: float
    position: typing.Tuple[float, float]
    length: float
