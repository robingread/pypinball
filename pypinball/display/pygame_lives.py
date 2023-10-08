import typing

import pygame

from .. import log

logger = log.get_logger(name=__name__)


def get_surface_size(
    num_lives: int, icon_size: int, icon_spacing: int
) -> typing.Tuple[int, int]:
    """Get the size of the surface used to display a given number of lives.

    Args:
        num_lives (int): Number of lives to be drawn.
        icon_size (int): Size of the life icon.
        icon_spacing (int): Spacing between the icons.

    Returns:
        typing.Tuple[int, int]: Size of the surface in the format (width, height).
    """
    w = (icon_size * num_lives) + (icon_spacing * max(num_lives - 1, 0))
    return (w, icon_size)


def get_life_icon_coordinate(
    width: int, icon_spacing: int, life_index: int
) -> typing.Tuple[int, int]:
    """Get the top-left coordinate of the icon to be drawn.

    Args:
        width (int): Icon width (in pixels).
        icon_spacing (int): Horizontal spacing between icons (in pixels).
        life_index (int): Index of the life to be drawn.

    Returns:
        typing.Tuple[int, int]: Coordinate of the top-left corner in the format (x, y).
    """
    w = (width + icon_spacing) * life_index
    return (w, 0)


class LivesCache:
    """Class that loads and caches different ``pygame.Surface`` instances that are used
    to represent the number of remaining lives. This class should be liked like a
    dictionary where the key is the number of lives to be remaining, and the value is
    the ``pygame.Surface`` that can be used to render the visual representation of this.
    """

    def __init__(
        self, max_lives: int, icon_path: str, icon_width: int, icon_spacing: int
    ) -> None:
        icon = pygame.image.load(icon_path).convert_alpha()
        icon = pygame.transform.scale(icon, (icon_width, icon_width))

        self._cache = dict()

        for l in range(max_lives + 1):
            surface = pygame.Surface(
                size=get_surface_size(
                    num_lives=l,
                    icon_size=icon_width,
                    icon_spacing=icon_spacing,
                )
            ).convert_alpha()
            surface.fill((0, 0, 0, 0))

            for i in range(l + 1):
                coord = get_life_icon_coordinate(
                    width=icon_width,
                    icon_spacing=icon_spacing,
                    life_index=i,
                )
                surface.blit(icon, coord)

            self._cache[l] = surface

    def __getitem__(self, index: int) -> pygame.Surface:
        if not isinstance(index, int):
            raise TypeError(f"Type of index must be an int, got: {type(index)}")

        if index not in self._cache.keys():
            logger.warning(f"LivesCache value not in the cache, index: {index}")
            return self._cache[0]

        return self._cache[index]
