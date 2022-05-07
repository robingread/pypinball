import pypinball
import unittest


class TestBallGeneration(unittest.TestCase):
    """
    Test adding a ball to the PymunkPhysics class.
    """

    def setUp(self) -> None:
        self.physics = pypinball.physics.PymunkPhysics()

    def test_add_ball(self):
        """
        Test adding a new ball to the physics scene returns ``True``.
        """
        ball = pypinball.domain.Ball(uid=0, position=(50.0, 50.0))
        ret = self.physics.add_ball(ball=ball)
        self.assertTrue(ret)

    def test_add_same_ball_twice(self):
        """
        Test that adding a ball with the same UID twice returns a ``False`` value.
        """
        ball = pypinball.domain.Ball(uid=0, position=(50.0, 50.0))
        ret = self.physics.add_ball(ball=ball)
        self.assertTrue(ret)

        ret = self.physics.add_ball(ball=ball)
        self.assertFalse(ret)

    def test_get_ball_state(self):
        """
        Test getting the state of a ball that has been added to the Physics scene.
        """
        ball = pypinball.domain.Ball(uid=0, position=(50.0, 50.0))
        self.physics.add_ball(ball=ball)
        state = self.physics.get_ball_state(uid=ball.uid)
        self.assertTupleEqual(state.position, ball.position)

    def test_get_ball_state_unknown_ball_id(self):
        """
        Test that getting the state of an unregistered ball throws an exception.
        """
        with self.assertRaises(KeyError):
            self.physics.get_ball_state(uid=10)


class TestBallLaunch(unittest.TestCase):
    """
    Test the general functionality of launching a ball via the PymunkPhysics class.
    """

    def setUp(self) -> None:
        self.ball = pypinball.domain.Ball(uid=0, position=(100, 100))
        self.physics = pypinball.physics.PymunkPhysics()
        self.physics.add_ball(ball=self.ball)

    def test_launch_ball(self):
        """
        Test that after being launched, the ball position has changed from the
        initial position when it was created, and it is moving against the
        gravity vector.
        """
        initial_state = self.physics.get_ball_state(uid=self.ball.uid)
        self.assertTupleEqual(self.ball.position, initial_state.position)

        self.physics.launch_ball(uid=self.ball.uid)

        for _ in range(100):
            self.physics.update()

        new_state = self.physics.get_ball_state(uid=self.ball.uid)
        self.assertLessEqual(new_state.position[1], initial_state.position[1])
