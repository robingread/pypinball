"""Module for generating and querying the cache of pygame surfaces used for rendering
the score of the game."""

import typing

import pygame

from .. import log

logger = log.get_logger(name=__name__)


def generate_scoring_cache(
    max_score: int,
    font: str = "Comic Sans MS",
    size: int = 35,
    color: typing.Tuple[int, int, int] = (255, 255, 255),
) -> typing.Dict[int, pygame.Surface]:
    """Generate a dictionary that maps score values (as ints) to ``pygame.Surfaces`` that
    can be used to render the score itself. The range of values will be [-1, max_score].
    An index of -1 can be used in situations if an unknown score is provided.

    Args:
        max_score (int): Maximum score value.
        font (str, optional): Font to use. Defaults to "Comic Sans MS".
        size (int, optional): Size of the font. Defaults to 35.
        color (typing.Tuple[int, int, int], optional): Font RGB color. Defaults to (255, 255, 255).

    Returns:
        typing.Dict[int, pygame.Surface]: Dictionary mapping score ints to pygame Surfaces.
    """
    pygame.font.init()
    _font = pygame.font.SysFont(name=font, size=size)
    ret = {i: _font.render(str(i), False, color) for i in range(max_score + 1)}
    ret[-1] = _font.render("---", False, color)
    return ret


class ScoringCache:
    """The ScoringCache class contains an internal mapping between a score and the
    pygame.Surface that can be used to render the score to the main pygame.Surface.

    This can be used as if it were a dictionary via index accessing, though the index
    should be an ``int``. If another type is used to access then an ``TypeError`` is
    thrown and if the score value is not in the cache (e.g., a score higher than the
    maximum score has been requested) then a default Surface with '---' is returned.
    """

    def __init__(self, max_score: int) -> None:
        self._cache = generate_scoring_cache(max_score=max_score)

    def __getitem__(self, index: int) -> pygame.Surface:
        if not isinstance(index, int):
            raise TypeError(f"Type of index must be an int, got: {type(index)}")

        if index not in self._cache.keys():
            logger.warning(f"ScoreCache value not in the cache, index: {index}")
            return self._cache[-1]

        return self._cache[index]
