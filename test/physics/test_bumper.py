import unittest

import pypinball


class TestBumper(unittest.TestCase):
    """
    Test the interface for managing bumpers in the PymunkPhysics class.
    """

    def setUp(self) -> None:
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(
            event_pub=self.event_pub, fps=60.0
        )

    def test_add_bumper(self):
        """
        Test adding a new bumper with an unregistered ID.
        """
        bumper = pypinball.domain.RoundBumper(uid=0, position=(50, 100), radius=15.0)
        ret = self.physics.add_bumper(bumper=bumper)
        self.assertTrue(ret)

    def test_add_same_bumper_twice(self):
        """
        Test that adding the same bumper twice fails.
        """
        bumper = pypinball.domain.RoundBumper(uid=0, position=(50, 100), radius=15.0)
        ret = self.physics.add_bumper(bumper=bumper)
        self.assertTrue(ret)

        ret = self.physics.add_bumper(bumper=bumper)
        self.assertFalse(ret)

    def test_add_two_different_bumpers(self):
        """
        Test that adding two different bumpers works.
        """
        bumper1 = pypinball.domain.RoundBumper(uid=0, position=(50, 100), radius=15.0)
        ret = self.physics.add_bumper(bumper=bumper1)
        self.assertTrue(ret)

        bumper2 = pypinball.domain.RoundBumper(uid=1, position=(50, 100), radius=15.0)
        ret = self.physics.add_bumper(bumper=bumper2)
        self.assertTrue(ret)

    def test_remove_bumper_method_returns_true(self):
        """
        Test the remove_bumper() method returns ``True``
        """
        bumper = pypinball.domain.RoundBumper(uid=0, position=(50, 100), radius=15.0)
        self.physics.add_bumper(bumper=bumper)
        ret = self.physics.remove_bumper(uid=bumper.uid)
        self.assertTrue(ret)

    def test_remove_unknown_bumper(self):
        """
        Test removing an unknown bumper fails.
        """
        ret = self.physics.remove_bumper(uid=100)
        self.assertFalse(ret)

    def test_get_state_of_known_bumper(self) -> None:
        bumper = pypinball.domain.RoundBumper(uid=0, position=(50, 100), radius=15.0)
        self.physics.add_bumper(bumper=bumper)
        res = self.physics.get_bumper_state(uid=bumper.uid)

        self.assertIsInstance(res, pypinball.domain.Bumper)
        self.assertEqual(res.type, pypinball.domain.BumperType.ROUND)

    def test_get_bumper_states(self) -> None:
        bumper = pypinball.domain.RoundBumper(uid=0, position=(50, 100), radius=15.0)
        self.physics.add_bumper(bumper=bumper)
        res = self.physics.get_bumper_states()
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 1)

    def test_get_state_of_unknwon_bumper(self) -> None:
        """
        Test that looking up the state of an unknown bumper throws an exception.
        """
        with self.assertRaises(KeyError):
            self.physics.get_bumper_state(uid=100)

    def test_get_bumper_states_unknown(self) -> None:
        self.assertEqual(len(self.physics.get_bumper_states()), 0)
