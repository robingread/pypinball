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


class TestFlipperCache(unittest.TestCase):
    """Test the FlipperCache class in the pygame.display.ball_cache module."""

    def setUp(self) -> None:
        pygame.display.set_mode((1, 1), pygame.NOFRAME)
        path = pypinball.resources.get_image_resource_path(filename="ball.png")
        self.cache = pypinball.display.ball_cache.FlipperCache(
            icon_path=path, angle_rounding=10
        )

    def test_len_at_init(self) -> None:
        """Test that the length of the cache is zero at initialisation."""
        self.assertEqual(len(self.cache), 0)

    def test_get_new_value(self) -> None:
        """Test that getting a new value for the first time increments the size of the cache."""
        self.cache.get(uid=0, size=(10, 10), angle=0.0)
        self.assertEqual(len(self.cache), 1)

    def test_get_new_value_twice(self) -> None:
        """Test that getting the same value twice doesn't add anything new to the cache."""
        self.cache.get(uid=0, size=(10, 10), angle=0.0)
        self.cache.get(uid=0, size=(10, 10), angle=0.0)
        self.assertEqual(len(self.cache), 1)

    def test_get_two_new_values(self) -> None:
        """Test that getting the same value twice doesn't add anything new to the cache."""
        self.cache.get(uid=0, size=(10, 10), angle=0.0)
        self.cache.get(uid=0, size=(10, 10), angle=11.0)
        self.assertEqual(len(self.cache), 2)

    def test_the_cached_surfaces_matches_the_input_size(self) -> None:
        """Test that the cached Surface has the correct dimensions."""
        surface = self.cache.get(uid=0, size=(10, 20), angle=0.0)
        self.assertEqual(surface.get_width(), 10)
        self.assertEqual(surface.get_height(), 20)

    def test_clear_cache(self) -> None:
        """Test that the clear() method works."""
        for i in range(100):
            self.cache.get(uid=0, size=(10, 20), angle=float(i))
        self.assertGreater(len(self.cache), 1)
        self.cache.clear()
        self.assertEqual(len(self.cache), 0)
