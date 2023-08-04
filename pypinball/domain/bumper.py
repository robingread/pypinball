import enum
import typing


class BumperType(enum.Enum):
    """
    Enums to specify the different types of Bumper that can exist.
    """

    ROUND = enum.auto()
    RECTANGLE = enum.auto()


class Bumper:
    """
    Class containing configuration for a round bumper.
    """

    def __init__(
        self, uid: int, position: typing.Tuple[float, float], bumper_type: BumperType
    ) -> None:
        self._uid = uid
        self._position = position
        self._type = bumper_type

    @property
    def uid(self) -> int:
        """
        Get the unique ID of the bumper.

        Returns:
            int: Unique ID.
        """
        return self._uid

    @property
    def position(self) -> typing.Tuple[float, float]:
        """
        Get the position of the bumper in the global physics coordinate frame.

        Returns:
            tuple: In the format (x, y).
        """
        return self._position

    @property
    def type(self) -> BumperType:
        """
        Get the BumperType.

        Returns:
            BumperType: Type.
        """
        return self._type


class RoundBumper(Bumper):
    """
    The RoundBumper class extends the Bumper class to capture the instance
    where the shape of the bumper is a circle.

    The only extra member variable is the ``radius`` which is specified in
    pixels.

    Args:
        radius (float): Radius of the bumper.
    """

    def __init__(self, radius: float, *args, **kwargs) -> None:
        super().__init__(bumper_type=BumperType.ROUND, *args, **kwargs)
        self._radius = radius

    @property
    def radius(self) -> float:
        """
        Get the radius of the bumper.

        Returns:
            float: Radius in pixels.
        """
        return self._radius


class RectangleBumper(Bumper):
    """
    The ``RectangleBumper`` class extends the ``Bumper`` class to capture the
    instance where the shape of the bumper is a rectangle/square.

    The extra class member variables are the ``angle`` and ``size``. The
    ``angle`` is the rotation angle of the bumper in the world coordinate frame
    of the physics environment. The ``size`` member is a two element tuple with
    the first element being the side length in the X axis of the bumper's
    local coordinate frame, and the second element being the length along
    the Y axis.

    Args:
        angle (float): Rotation angle in radians.
        size (tuple): Bumper size in the format (width, height).
    """

    def __init__(
        self, angle: float, size: typing.Tuple[float, float], *args, **kwargs
    ) -> None:
        super().__init__(bumper_type=BumperType.RECTANGLE, *args, **kwargs)
        self._angle = angle
        self._size = size

    @property
    def angle(self) -> float:
        """
        The angle of rotation of the bumper in the physics global coordinate
        frame.

        Returns:
            float: Angle in radians.
        """
        return self._angle

    @property
    def size(self) -> typing.Tuple[float, float]:
        """
        Get the size of the bumper in the local coordinate system.

        Returns:
            tuple: Size in the format (x, y).
        """
        return self._size
