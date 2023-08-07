import random
import unittest

from pypinball.events import GameEvents
from pypinball.lives import Lives


class TestInit(unittest.TestCase):
    """Test the Lives class at initialization."""

    def setUp(self) -> None:
        self.lives = Lives(lives=5)

    def test_get_lives(self) -> None:
        """Test that the number of lives at __init__() is as expected."""
        self.assertEqual(self.lives.get_lives(), 5)


class TestBallLostEvent(unittest.TestCase):
    """Test that calling the event handler with a GameEvents.BALL_LOST method
    behaves as expected."""

    def setUp(self) -> None:
        self.lives = Lives(lives=5)
        self.lives.event_callback(event=GameEvents.BALL_LOST)

    def test_live_has_been_lost(self) -> None:
        """Test that calling the event handler reduces the number of lives by one."""
        self.assertEqual(self.lives.get_lives(), 4)


class TestOtherEvent(unittest.TestCase):
    """Test that any other event other than the BALL_LOST event does not impact the
    remaining lives."""

    def setUp(self) -> None:
        events = list(GameEvents)
        events.remove(GameEvents.BALL_LOST)
        event = random.choice(events)

        self.lives = Lives(lives=5)
        self.lives.event_callback(event=event)

    def test_get_lives(self) -> None:
        """Test that the number of lives at __init__() is as expected."""
        self.assertEqual(self.lives.get_lives(), 5)

    def test_calling_all_other_events(self) -> None:
        """Brute force testing that all other events have no impact."""
        events = list(GameEvents)
        events.remove(GameEvents.BALL_LOST)

        for event in events:
            self.lives.event_callback(event=event)
            self.assertEqual(self.lives.get_lives(), 5)
