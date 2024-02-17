import random
import unittest

import pypinball


class TestScoring(unittest.TestCase):
    """
    Test the ``Scoring`` class, the interaction is has with the GameEventPublisher
    (i.e. it handles events correctly) and the creation using the ``get_scorer()``
    method.
    """

    def setUp(self) -> None:
        self._event_pub = pypinball.events.GameEventPublisher()
        self._scorer = pypinball.scoring.get_scorer(event_pub=self._event_pub)

    def test_publisher_has_handler(self) -> None:
        """Test that the event publisher has a registered subscriber method after calling the ``get_scorer()`` method."""
        self.assertEqual(
            self._event_pub.num_subscribers,
            1,
            msg="Event publisher does not have a registered subscriber method",
        )

    def test_initial_score(self) -> None:
        """Test that once initialized, the Scorer class has a score of zero"""
        self.assertEqual(
            self._scorer.current_score, 0, msg="Scoring class current value is not zero"
        )

    def test_set_scoring_multiplier(self) -> None:
        """Test the ability to update the scoring multiplier"""
        self._scorer.set_multiplier(value=2.0)
        self.assertEqual(
            self._scorer.multiplier,
            2.0,
            msg="Multiplier has not been updated after calling set_multiplier method.",
        )

    def test_score_updated_with_ball_bumper_collision(self) -> None:
        """Test that the score updates when a COLLISION_BALL_BUMPER GameEvent is emitted."""
        self.assertEqual(
            self._scorer.current_score, 0, msg="Initial score is not zero."
        )
        self._event_pub.emit(event=pypinball.events.GameEvents.COLLISION_BALL_BUMPER)
        self.assertEqual(
            self._scorer.current_score,
            1,
            msg="Collision event has not updated the score properly",
        )

    def test_score_not_updated_with_random_event(self) -> None:
        """Test that emitting random GameEvents does not impact the score."""
        events = set(pypinball.events.GameEvents)
        events.remove(pypinball.events.GameEvents.COLLISION_BALL_BUMPER)

        for _ in range(100):
            event = random.choice(list(events))
            self._event_pub.emit(event=event)
            self.assertEqual(
                self._scorer.current_score,
                0,
                msg="Random game event has impacted the score!",
            )


class TestResetScore(unittest.TestCase):
    """Test case of resetting a score back to zero."""

    def setUp(self) -> None:
        self.score = pypinball.scoring.Scoring()

    def test_set_score(self) -> None:
        """Test setting the score to a given value."""
        self.score.set_score(10)
        self.assertEqual(self.score.current_score, 10)

    def test_reset_score(self) -> None:
        """Test the reset() method to check that the score goes back to zero."""
        self.score.set_score(10)
        self.score.reset()
        self.assertEqual(self.score.current_score, 0)
