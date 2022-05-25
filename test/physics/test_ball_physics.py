import numpy
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


class TestGravity(unittest.TestCase):
    """
    Test that balls behave under gravity as expected.
    """

    def setUp(self) -> None:
        self.physics = pypinball.physics.PymunkPhysics()

    def test_default_gravity(self):
        """
        Test that the default value for the gravity vector is (0, 1), and that
        the ball indeed falls under gravity in the expected direction.
        """
        ball = pypinball.domain.Ball(uid=0, position=(100, 100))
        self.physics.add_ball(ball=ball)
        initial_state = self.physics.get_ball_state(uid=ball.uid)

        for _ in range(10):
            self.physics.update()

        new_state = self.physics.get_ball_state(uid=ball.uid)

        a = numpy.array(initial_state.position)
        b = numpy.array(new_state.position)
        diff = b - a
        motion_unit_vec = diff / numpy.linalg.norm(diff)

        exp_unit_vec = numpy.array([0.0, 1.0])

        self.assertTrue(numpy.allclose(motion_unit_vec, exp_unit_vec))


class TestWallGeneration(unittest.TestCase):
    """
    Test that wall sections can be added to the Physics scene.
    """

    def setUp(self):
        self.physics = pypinball.physics.PymunkPhysics()

    def test_add_wall_section(self):
        """
        Test that adding a wall section to the scene returns ``True``.
        """
        wall = pypinball.domain.Wall(uid=0, points=[(0.0, 0.0), (10.0, 10.0)])
        ret = self.physics.add_wall(wall=wall)
        self.assertTrue(ret)

    def test_adding_wall_section_twice_fails(self):
        """
        Test that adding the same wall section to the scene twice fails. The
        first time the section is added should work, but not the second time.
        """
        wall = pypinball.domain.Wall(uid=0, points=[(0.0, 0.0), (10.0, 10.0)])

        ret = self.physics.add_wall(wall=wall)
        self.assertTrue(ret)

        ret = self.physics.add_wall(wall=wall)
        self.assertFalse(ret)
