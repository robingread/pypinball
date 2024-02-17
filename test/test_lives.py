import random
import unittest
import unittest.mock

from pypinball.events import GameEventPublisher, GameEvents
from pypinball.lives import Lives


class TestInit(unittest.TestCase):
    """Test the Lives class at initialization."""

    def setUp(self) -> None:
        self.event_pub = unittest.mock.MagicMock(spec=GameEventPublisher)
        self.lives = Lives(lives=5, event_pub=self.event_pub)

    def test_get_lives(self) -> None:
        """Test that the number of lives at __init__() is as expected."""
        self.assertEqual(self.lives.get_lives(), 5)


class TestBallLostEvent(unittest.TestCase):
    """Test that calling the event handler with a GameEvents.BALL_LOST method
    behaves as expected."""

    def setUp(self) -> None:
        self.event_pub = unittest.mock.MagicMock(spec=GameEventPublisher)
        self.lives = Lives(lives=5, event_pub=self.event_pub)
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

        self.event_pub = unittest.mock.MagicMock(spec=GameEventPublisher)
        self.lives = Lives(lives=5, event_pub=self.event_pub)
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


class TestRunOutOfLives(unittest.TestCase):
    """Test the scenario in which the last live is lost."""

    def setUp(self) -> None:
        self.event_pub = unittest.mock.MagicMock(spec=GameEventPublisher)
        self.lives = Lives(lives=1, event_pub=self.event_pub)
        self.lives.event_callback(event=GameEvents.BALL_LOST)

    def test_lives_left(self) -> None:
        """Test that the number of lives left is zero."""
        self.assertEqual(self.lives.get_lives(), 0)

    def test_game_over_event_emitted(self) -> None:
        """Test that on the last live lost, the GAME_OVER event is emitted"""
        exp = {"event": GameEvents.GAME_OVER}
        res = self.event_pub.emit.call_args.kwargs
        self.assertEqual(res, exp)

    def test_calling_ball_lost_event_again_has_no_effect(self) -> None:
        """Test that once the lives has reached zero, no more BALL_LOST events have an impact"""
        self.lives.event_callback(event=GameEvents.BALL_LOST)
        self.assertEqual(self.lives.get_lives(), 0)


class TestSetRemainingLives(unittest.TestCase):
    """Test overriding the current lives value with a new user-defined value."""

    def setUp(self) -> None:
        self.event_pub = unittest.mock.MagicMock(spec=GameEventPublisher)
        self.lives = Lives(lives=2, event_pub=self.event_pub)

    def test_set_lives(self) -> None:
        """Test the set_lives() method to confirm it overrides the current lives value."""
        n = 5
        self.lives.set_lives(value=n)
        self.assertEqual(self.lives.get_lives(), n)
