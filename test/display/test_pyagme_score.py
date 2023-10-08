import unittest

import pygame

from pypinball.display.pygame_score import ScoringCache, generate_scoring_cache


class GenerateScoringCache(unittest.TestCase):
    """Test the generate_scoring_cache() method in the pygame.display.pygame_scoring.py module."""

    def setUp(self) -> None:
        self.max_score = 100
        self.cache = generate_scoring_cache(max_score=self.max_score)

    def test_return_dict_size(self) -> None:
        """Test the number of keys in the returned dictionary"""
        res = len(list(self.cache.keys()))
        self.assertEqual(res, self.max_score + 2)

    def test_access_max_score(self) -> None:
        """Test that we can access the max score value."""
        result = self.cache[self.max_score]
        self.assertIsInstance(result, pygame.Surface)

    def test_access_error_value(self) -> None:
        """Test that we can access the 'error' value."""
        result = self.cache[-1]
        self.assertIsInstance(result, pygame.Surface)


class TestScoringCache(unittest.TestCase):
    """Test the ScoringCache class"""

    def setUp(self) -> None:
        self.cache = ScoringCache(max_score=100)

    def test_access_unknown_score(self) -> None:
        """Test we can access a score NOT within the max value and get a Surface back"""
        result = self.cache[200]
        self.assertIsInstance(result, pygame.Surface)

    def test_access_known_score(self) -> None:
        """Test we can access a score within the max value and get a Surface back"""
        result = self.cache[2]
        self.assertIsInstance(result, pygame.Surface)

    def test_access_with_wrong_index_type(self) -> None:
        """Test that accessing the cache with an incorrect type throws a TypeError"""
        with self.assertRaises(TypeError):
            _ = self.cache["foo"]
