"""Module contains the BallCache class which is used to speed up rendering of the Game
graphics."""

import math
import typing

import pygame

from .. import log

logger = log.get_logger(name=__name__)


class BallCache:
    """The BallCache class is used to pre-load the Ball icon and prepare a PyGame Surface
    which can be used to quickly render the ball at runtime. This provides a significant
    real-time speedup of the rendering process."""

    def __init__(self, icon_path: str, diameter: int) -> None:
        self._img = pygame.image.load(icon_path).convert_alpha()
        self._img = pygame.transform.scale(self._img, size=(diameter, diameter))
        self._img = pygame.transform.rotate(self._img, angle=0.0)
        self._img.set_alpha(255)

    def get(self) -> pygame.Surface:
        """Get the pre-loaded PyGame surface representing the graphic for the ball.

        Returns:
            pygame.Surface: PyGame surface.
        """
        return self._img


class BumperCache:
    """The BumperCache class is used to maintain a cache of the bumper states that have
    been render previously. The aim of this is to increase by rendering efficiency
    during runtime.
    """

    def __init__(self, icon_path: str) -> None:
        self._icon_img = pygame.image.load(icon_path).convert_alpha()
        self._cache: typing.Dict[int, pygame.Surface] = dict()

    def __len__(self) -> int:
        return len(self._cache.keys())

    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()

    def get(
        self, uid: int, size: typing.Tuple[int, int], angle: float
    ) -> pygame.Surface:
        """Get the pre-loaded PyGame surface representing the graphic for a bumper.

        Args:
            uid (int): Unique ID of the bumper to get.
            size (typing.Tuple[int, int]): The size of the bumper in the format (width, heigth), in pixels.
            angle (float): Angle of the bumper.

        Returns:
            pygame.Surface: PyGame surface.
        """
        if uid not in self._cache.keys():
            logger.debug(f"Loading bumper into cache, uid: {uid}")
            img = pygame.transform.scale(self._icon_img, size=size)
            img = pygame.transform.rotate(img, angle=math.degrees(-angle))
            img.set_alpha(255)
            self._cache[uid] = img
        return self._cache[uid]


class FlipperCache:
    """The FlipperCache class is used to cache the various states of the flippers
    during the game at runtime. This is done to be able to speed up the rendering
    process during runtime and make things more efficient.

    As the cache is queried, if a Flipper with a given UID and angle isn't already within
    the cache (i.e. this is the first time it is being rendered), then a ``pygame.Surface``
    is crated, added to the cache and then returned to the user.

    Given that the flippers have a limited range of motion, the benefits of this caching
    quickly become apparent!
    """

    def __init__(self, icon_path: str, angle_rounding: int) -> None:
        self._icon_img = pygame.image.load(icon_path).convert_alpha()
        self._cache: typing.Dict[typing.Tuple[int, int], pygame.Surface] = dict()
        self._rounding_angle = int(angle_rounding)

    def __len__(self) -> int:
        return len(self._cache.keys())

    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()

    def get(
        self, uid: int, size: typing.Tuple[int, int], angle: float
    ) -> pygame.Surface:
        """Get the (cached) ``pygame.Surface`` for a given flipper with a given
        angle. Both the UID and the angle are used to create the hash value for the
        internal cache, and the angle is rounded to the nearest degrees specified
        rounding angle (as an `int`).

        If the unique has value is not already in the cache, then it is added within
        this call.

        Args:
            uid (int): Unique ID of the flipper.
            size (typing.Tuple[int, int]): The size of the flipper icon to render (in pixels).
            angle (float): Angle of the flipper in the global frame (in radians).

        Returns:
            pygame.Surface: PyGame surface to that can be used for rendering.
        """
        _angle = int(math.degrees(-angle) / self._rounding_angle) * self._rounding_angle
        _key = (uid, _angle)

        if _key not in self._cache.keys():
            logger.debug(f"Loading flipper into cache, uid: {uid}, angle: {_angle}")
            img = pygame.transform.scale(self._icon_img, size=size)
            img = pygame.transform.rotate(img, angle=math.degrees(-angle))
            img.set_alpha(255)
            self._cache[_key] = img

        return self._cache[_key]
