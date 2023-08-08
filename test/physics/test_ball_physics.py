import unittest
import unittest.mock

import numpy

import pypinball


class TestBallGeneration(unittest.TestCase):
    """
    Test adding a ball to the PymunkPhysics class.
    """

    def setUp(self) -> None:
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)

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


class TestRemoveBall(unittest.TestCase):
    """
    Test the remove_ball() method in the PymunkPhysics class.
    """

    def setUp(self) -> None:
        self.ball = pypinball.domain.Ball(uid=0, position=(50.0, 50.0))
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball)

    def test_remove_ball_success(self):
        """
        Test that removing an added ball is successful.
        """
        self.assertTrue(self.physics.remove_ball(uid=self.ball.uid))

    def test_remove_unknown_ball_fails(self):
        """
        Test that removing an unknown ball fails.
        """
        self.assertFalse(self.physics.remove_ball(uid=10))

    def test_get_state_fails_after_ball_remove(self):
        """
        Test that getting the state of an unknown ball throws an Exception.
        """
        with self.assertRaises(KeyError):
            self.physics.get_ball_state(uid=10)


class TestBallLaunch(unittest.TestCase):
    """
    Test the general functionality of launching a ball via the PymunkPhysics class.
    """

    def setUp(self) -> None:
        self.ball = pypinball.domain.Ball(uid=0, position=(100, 100))
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball)

    def test_launch_ball(self):
        """
        Test that the launch_ball() method returns ``True``.
        """
        ret = self.physics.launch_ball(uid=self.ball.uid)
        self.assertTrue(ret, msg="Failed to launch valid ball.")

    def test_launch_undefined_ball(self):
        """
        Test that the launch_ball() method returns ``False`` when attempting
        to launch ball that is not registered within the physics simulation.
        """
        ret = self.physics.launch_ball(uid=100)
        self.assertFalse(ret, msg="Launched an unregistered ball.")

    def test_launch_ball_motion(self):
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
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)

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
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)

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


class TestBallDropOnDiagonalWall(unittest.TestCase):
    """
    Test condition where we add a ball to the scene with a wall that is diagonal.
    The ball should fall down, hit the wall, bounce to the right and register
    a collision.
    """

    def setUp(self):
        self.ball = pypinball.domain.Ball(uid=0, position=(100.0, 0.0))
        self.wall = pypinball.domain.Wall(uid=1, points=[(75.0, 50.0), (125.0, 100.0)])
        self.event_pub = unittest.mock.MagicMock(
            wraps=pypinball.events.GameEventPublisher()
        )
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball)
        self.physics.add_wall(wall=self.wall)

        for _ in range(100):
            self.physics.update()

    def test_ball_has_moved_to_right_after_bounce(self):
        """
        Test that after hitting the wall, the wall bounces to the right.
        """
        ball_state = self.physics.get_ball_state(uid=self.ball.uid)

        self.assertGreater(
            ball_state.position[0],
            self.ball.position[0],
            msg="Ball has not bounced to the right.",
        )
        self.assertGreater(
            ball_state.position[1],
            self.ball.position[1],
            msg="Ball has not fallen down in Y axis under gravity.",
        )

    def test_physics_reports_collision_between_ball_and_wall(self):
        """
        Test that the PymunkPhysics call registers a collision between the
        ball and the wall.
        """
        self.event_pub.emit.assert_called_once_with(
            event=pypinball.events.GameEvents.COLLISION_BALL_WALL
        )


class TestBallDropInEmptyScene(unittest.TestCase):
    """
    Test dropping a ball in an empty scene.
    """

    def setUp(self) -> None:
        self.ball = pypinball.domain.Ball(uid=0, position=(100.0, 0.0))
        self.event_pub = unittest.mock.MagicMock(
            wraps=pypinball.events.GameEventPublisher()
        )
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball)

        for _ in range(100):
            self.physics.update()

    def test_ball_drop_downwards(self):
        """
        Test that after hitting the wall, the wall bounces to the right.
        """
        ball_state = self.physics.get_ball_state(uid=self.ball.uid)

        self.assertAlmostEqual(
            ball_state.position[0],
            self.ball.position[0],
            delta=0.001,
            msg="Ball X component has changed when falling under gravity.",
        )
        self.assertGreater(
            ball_state.position[1],
            self.ball.position[1],
            msg="Ball has not fallen down in Y axis under gravity.",
        )

    def test_no_collisions_reported(self):
        """
        Test that a ball falling within a scene with nothing else reports
        no collisions.
        """
        self.event_pub.emit.assert_not_called()


class TestBallDropsOnLaunchedBall(unittest.TestCase):
    """
    Test condition where a ball is launched into another ball and only a
    single collision between the two balls is registered.
    """

    def setUp(self) -> None:
        self.ball_1 = pypinball.domain.Ball(uid=0, position=(100.0, 100.0))
        self.ball_2 = pypinball.domain.Ball(uid=1, position=(100.0, 0.0))
        self.event_pub = unittest.mock.MagicMock(
            wraps=pypinball.events.GameEventPublisher()
        )

        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball_1)
        self.physics.add_ball(ball=self.ball_2)
        self.physics.launch_ball(uid=self.ball_1.uid)

        for _ in range(100):
            self.physics.update()

    def test_physics_reports_collision_between_ball_and_ball(self):
        """
        Test that the PymunkPhysics call registers a collision between the
        two balls.
        """
        # This is because we expect two collisions from two balls hitting each other.
        calls = [
            unittest.mock.call(event=pypinball.events.GameEvents.COLLISION_BALL_BALL)
        ] * 2
        self.event_pub.emit.assert_has_calls(calls, any_order=True)


class TestBallDropsOnFlipper(unittest.TestCase):
    """
    Test the condition when a ball drops onto a flipper which is angled towards
    the right.
    """

    def setUp(self) -> None:
        self.ball = pypinball.domain.Ball(uid=0, position=(100.0, 0.0))
        self.flipper = pypinball.domain.Flipper(
            uid=1,
            config=pypinball.domain.FlipperConfig(
                position=(75.0, 250.0),
                angle=1.0,
                length=25,
                actuation_angle=1.0,
                actuation_direction=1,
                actuation_input=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
            ),
        )
        self.event_pub = unittest.mock.MagicMock(
            wraps=pypinball.events.GameEventPublisher()
        )
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball)
        self.physics.add_flipper(flipper=self.flipper)

        for _ in range(100):
            self.physics.update()

    def test_ball_bounces_right_after_collision(self):
        """
        Test that the ball has fallen under gravity and that it has moved
        to the right after the collision with the flipper.
        """
        state = self.physics.get_ball_state(uid=self.ball.uid)

        self.assertGreater(
            state.position[0],
            self.ball.position[0],
            msg="Ball position Y component has not increased",
        )

        self.assertGreater(
            state.position[1],
            self.ball.position[1],
            msg="Ball has not moved right after collision",
        )

    def test_physics_reports_collision_between_ball_and_flipper(self):
        """
        Test that the Physics interface registers a collision between the
        ball and the flipper.
        """
        self.event_pub.emit.assert_called_once_with(
            event=pypinball.events.GameEvents.COLLISION_BALL_FLIPPER
        )


class TestBallDroppedOnRoundBumper(unittest.TestCase):
    def setUp(self):
        self.ball = pypinball.domain.Ball(uid=0, position=(100.0, 0.0))
        self.bumper = pypinball.domain.RoundBumper(uid=1, radius=10, position=(90, 150))
        self.event_pub = unittest.mock.MagicMock(
            wraps=pypinball.events.GameEventPublisher()
        )
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball)
        self.physics.add_bumper(bumper=self.bumper)

        for _ in range(100):
            self.physics.update()

    def test_ball_bounces_right(self):
        """
        Test that when the ball is dropped on the bumper, it bounces off
        and moves to the right and continues to fall downwards
        """
        state = self.physics.get_ball_state(uid=self.ball.uid)

        self.assertGreater(
            state.position[0],
            self.ball.position[0],
            msg="Ball position Y component has not increased",
        )

        self.assertGreater(
            state.position[1],
            self.ball.position[1],
            msg="Ball has not moved right after collision",
        )

    def test_physics_reports_collision_between_ball_and_bumper(self):
        self.event_pub.emit.assert_called_once_with(
            event=pypinball.events.GameEvents.COLLISION_BALL_BUMPER
        )


class TestBallDroppedOnRectangleBumper(unittest.TestCase):
    def setUp(self):
        self.ball = pypinball.domain.Ball(uid=0, position=(100.0, 0.0))
        self.event_pub = unittest.mock.MagicMock(
            wraps=pypinball.events.GameEventPublisher()
        )
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)
        self.physics.add_ball(ball=self.ball)

    def test_ball_bounces_right_when_bumper_rotated_clockwise(self):
        """
        Test that when the ball is dropped on the bumper, it bounces off
        and moves to the right and continues to fall downwards
        """
        self.bumper = pypinball.domain.RectangleBumper(
            uid=1, position=(100, 150), angle=1.0, size=(100, 25)
        )
        self.physics.add_bumper(bumper=self.bumper)

        for _ in range(100):
            self.physics.update()

        state = self.physics.get_ball_state(uid=self.ball.uid)

        self.assertGreater(
            state.position[0],
            self.ball.position[0],
            msg="Ball position Y component has not increased",
        )

        self.assertGreater(
            state.position[1],
            self.ball.position[1],
            msg="Ball has not moved right after collision",
        )

    def test_ball_bounces_left_when_bumper_rotated_counter_clockwise(self):
        """
        Test that when the ball is dropped on the bumper, it bounces off
        and moves to the left and continues to fall downwards
        """
        self.bumper = pypinball.domain.RectangleBumper(
            uid=1, position=(100, 150), angle=-1.0, size=(100, 25)
        )
        self.physics.add_bumper(bumper=self.bumper)

        for _ in range(100):
            self.physics.update()

        state = self.physics.get_ball_state(uid=self.ball.uid)

        self.assertLess(
            state.position[0],
            self.ball.position[0],
            msg="Ball has not moved right after collision",
        )

        self.assertGreater(
            state.position[1],
            self.ball.position[1],
            msg="Ball position Y component has not increased",
        )

    def test_physics_reports_collision_between_ball_and_bumper(self):
        self.bumper = pypinball.domain.RectangleBumper(
            uid=1, position=(100, 150), angle=1.0, size=(100, 25)
        )
        self.physics.add_bumper(bumper=self.bumper)

        # exp = [pypinball.events.GameEvents.COLLISION_BALL_BUMPER]

        for _ in range(100):
            self.physics.update()

        self.event_pub.emit.assert_called_once_with(
            event=pypinball.events.GameEvents.COLLISION_BALL_BUMPER
        )

    def test_ball_does_not_hit_removed_bumper(self):
        self.bumper = pypinball.domain.RectangleBumper(
            uid=1, position=(100, 150), angle=1.0, size=(100, 25)
        )
        self.physics.add_bumper(bumper=self.bumper)
        self.physics.remove_bumper(uid=self.bumper.uid)

        for _ in range(100):
            self.physics.update()

        self.event_pub.emit.assert_not_called()
