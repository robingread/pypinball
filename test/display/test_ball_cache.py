import unittest

import pygame

import pypinball
import pypinball.display.ball_cache


class TestBallCache(unittest.TestCase):
    """Test the BallCache class."""

    def setUp(self) -> None:
        # Tell pygame not to show a window
        pygame.display.set_mode((1, 1), pygame.NOFRAME)

        self.diameter = 20
        path = pypinball.resources.get_image_resource_path(filename="ball.png")
        self.cache = pypinball.display.ball_cache.BallCache(
            icon_path=path, diameter=self.diameter
        )

    def test_get_surface_instance(self) -> None:
        """Test that the get() method returns an pygame.Surface instance"""
        res = self.cache.get()
        self.assertIsInstance(res, pygame.Surface)

    def test_get_surface_size(self) -> None:
        """Test that the size of the surface matches the diameter specified at init."""
        exp = self.diameter
        width = self.cache.get().get_width()
        height = self.cache.get().get_height()
        self.assertEqual(exp, width)
        self.assertEqual(exp, height)
