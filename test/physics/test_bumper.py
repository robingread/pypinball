import pypinball
import unittest


class TestBumper(unittest.TestCase):
    """
    Test the interface for managing bumpers in the PymunkPhysics class.
    """

    def setUp(self) -> None:
        self.physics = pypinball.physics.PymunkPhysics()

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
