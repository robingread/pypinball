"""Module contains the BallCache class which is used to speed up rendering of the Game
graphics."""

import pygame


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
