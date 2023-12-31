import random
import unittest
import unittest.mock

import pypinball


class MockDisplay(pypinball.DisplayInterface):
    """Mock DisplayInterface class to be used to unit-testing purposes."""

    def __init__(self) -> None:
        self.draw_background = unittest.mock.MagicMock()
        self.draw_ball = unittest.mock.MagicMock()
        self.draw_flipper = unittest.mock.MagicMock()
        self.draw_rectangle_bumper = unittest.mock.MagicMock()
        self.draw_round_bumper = unittest.mock.MagicMock()


class MockPhysics(pypinball.PhysicsInterface):
    """Mock PhysicsInterface class to be used to unit-testing purposes."""

    def __init__(self) -> None:
        self.get_ball_states = unittest.mock.MagicMock()
        self.get_bumper_states = unittest.mock.MagicMock()
        self.get_flipper_states = unittest.mock.MagicMock()


class TestBallWithinAreaFunction(unittest.TestCase):
    """
    Test the utils.check_ball_is_within_area() method.
    """

    def setUp(self) -> None:
        self.width = 100
        self.height = 100

    def test_ball_within_area(self) -> None:
        """
        Test the condition where the ball is within the area.
        """
        position = (10, 10)
        self.assertTrue(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_above(self) -> None:
        """
        Test the condition where the ball is outside the area where the ball is
        above the playable area.
        """
        position = (10, -10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_below(self) -> None:
        """
        Test the condition where the ball is outside the area where the ball is
        below the playable area.
        """
        position = (10, self.height + 10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_left(self) -> None:
        """
        Test the condition where the ball is outside the area where the ball is
        to the left of the playable area.
        """
        position = (-10, 10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_right(self) -> None:
        """
        Test the condition where the ball is outside the area where the ball is
        to the right of the playable area.
        """
        position = (self.width + 10, 10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )


class TestRenderPhysicsBalls(unittest.TestCase):
    """Test the utils.render_physics_balls() method."""

    def setUp(self) -> None:
        self.display = MockDisplay()

    def test_render_zero_balls(self) -> None:
        """
        Test that passing an empty list results in the DisplayInterface.draw_ball()
        not being called.
        """
        balls = list()
        pypinball.utils.render_physics_balls(balls, self.display)
        self.display.draw_ball.assert_not_called()

    def test_render_multiple_balls(self) -> None:
        """
        Test that passing a non-empty list results in the DisplayInterface.draw_ball()
        being called multiple times.

        """
        n = random.randint(1, 100)
        balls = list()
        for uid in range(n):
            ball = pypinball.domain.BallState(uid=uid, position=(0.0, 0.0), radius=10)
            balls.append(ball)

        pypinball.utils.render_physics_balls(balls, self.display)

        self.assertEqual(self.display.draw_ball.call_count, n)


class TestRenderPhysicsBumpers(unittest.TestCase):
    """Test the utils.render_physics_bumpers() method."""

    def setUp(self) -> None:
        self.display = MockDisplay()

        self.round_bumper = pypinball.domain.RoundBumper(
            uid=0,
            radius=10,
            position=(10, 10),
        )

        self.rectangle_bumper = pypinball.domain.RectangleBumper(
            uid=1, angle=0.0, position=(20, 20), size=(10, 20)
        )

    def test_render_zero_bumpers(self) -> None:
        """Call method with an empty list of bumpers. This should result in no calls to the display."""
        bumpers = list()
        pypinball.utils.render_physics_bumpers(bumpers=bumpers, display=self.display)
        self.display.draw_rectangle_bumper.assert_not_called()
        self.display.draw_round_bumper.assert_not_called()

    def test_render_round_bumper(self) -> None:
        """Call the method with a single round bumper. This should make a single display call."""
        bumpers = [self.round_bumper]
        pypinball.utils.render_physics_bumpers(bumpers=bumpers, display=self.display)
        self.display.draw_rectangle_bumper.assert_not_called()
        self.display.draw_round_bumper.assert_called_once()

    def test_render_rectangle_bumper(self) -> None:
        """Call the method with a single rectangle bumper. This should make a single display call."""
        bumpers = [self.rectangle_bumper]
        pypinball.utils.render_physics_bumpers(bumpers=bumpers, display=self.display)
        self.display.draw_rectangle_bumper.assert_called_once()
        self.display.draw_round_bumper.assert_not_called()

    def test_two_bumpers(self) -> None:
        """Call the method with a round and rectangle bumper. This should make two calls to the displya."""
        bumpers = [self.rectangle_bumper, self.round_bumper]
        pypinball.utils.render_physics_bumpers(bumpers=bumpers, display=self.display)
        self.display.draw_rectangle_bumper.assert_called_once()
        self.display.draw_round_bumper.assert_called_once()


class TestRenderPhysicsFlippers(unittest.TestCase):
    """Test the pypinballs.utils.render_physics_flippers() method."""

    def setUp(self) -> None:
        self.display = MockDisplay()

    def test_call_with_no_flippers(self) -> None:
        """Test calling the method with an empty list."""
        flippers = list()
        pypinball.utils.render_physics_flippers(flippers=flippers, display=self.display)
        self.display.draw_flipper.assert_not_called()

    def test_call_with_single_flipper(self) -> None:
        """Test call the method with a list containing a single flipper state."""
        flippers = [
            pypinball.domain.FlipperState(
                uid=0, position=(10, 10), angle=1.0, length=20
            )
        ]
        pypinball.utils.render_physics_flippers(flippers=flippers, display=self.display)
        self.display.draw_flipper.assert_called_once()


class TestRenderPhysicsState(unittest.TestCase):
    """Test the pypinball.utils.render_phyiscs_state() method."""

    def setUp(self) -> None:
        ball = pypinball.domain.BallState(uid=0, position=(10, 10), radius=20)
        flipper = pypinball.domain.FlipperState(
            uid=1, angle=0.0, position=(10, 20), length=10
        )
        round_bumper = pypinball.domain.RoundBumper(uid=2, position=(20, 20), radius=15)
        rect_bumper = pypinball.domain.RectangleBumper(
            uid=3, size=(13, 30), position=(30, 30), angle=0.5
        )

        self.physics = MockPhysics()
        self.physics.get_ball_states.return_value = [ball]
        self.physics.get_bumper_states.return_value = [round_bumper, rect_bumper]
        self.physics.get_flipper_states.return_value = [flipper]

        self.display = MockDisplay()

        pypinball.utils.render_physics_state(physics=self.physics, display=self.display)

    def test_display_methods_called(self) -> None:
        """Test that the expected display methods are called."""
        self.display.draw_background.assert_called_once()
        self.display.draw_ball.assert_called_once()
        self.display.draw_flipper.assert_called_once()
        self.display.draw_rectangle_bumper.assert_called_once()
        self.display.draw_round_bumper.assert_called_once()


class TestRenderScoreAndLives(unittest.TestCase):
    """Test the utils.render_score_and_lives() method."""

    def setUp(self) -> None:
        self.display = unittest.mock.MagicMock(spec=pypinball.DisplayInterface)
        self.lives = unittest.mock.MagicMock(spec=pypinball.lives.Lives)
        self.lives.get_lives.returns = 5

        self.scoring = unittest.mock.MagicMock(spec=pypinball.scoring.Scoring)
        self.scoring.current_score = unittest.mock.PropertyMock(return_value=100)

        pypinball.utils.render_score_and_lives(
            scoring=self.scoring, lives=self.lives, display=self.display
        )

    def test_lives_get_lives_called(self) -> None:
        """Test that teh lives object is accessed."""
        self.lives.get_lives.assert_called_once()

    def test_display_draw_lives_called_once(self) -> None:
        """Test that the draw_lives method is called in the DisplayInterface"""
        self.display.draw_lives.assert_called_once()

    def test_display_draw_score_called_once(self) -> None:
        """Test that the draw_score() method is called in the DisplayInterface"""
        self.display.draw_score.assert_called_once()


class TestHandleCenterButtonPressedWithRemainingBalls(unittest.TestCase):
    """Test the utils.handle_center_button_pressed() method when there are some balls
    left in the physics scene. In this case we do not expect a new ball to be added or
    launched via the PhysicsInterface
    """

    def setUp(self) -> None:
        cfg = pypinball.GameConfig(playing_area=(400, 400))
        self.id_gen = unittest.mock.MagicMock(wrap=pypinball.utils.ObjectIdGenerator())
        self.physics = unittest.mock.MagicMock(spec=pypinball.PhysicsInterface)
        self.physics.get_num_balls.return_value = 10

        pypinball.utils.handle_center_button_press(
            physics=self.physics,
            config=cfg,
            id_gen=self.id_gen,
        )

    def test_get_num_balls_called(self) -> None:
        """Test that the get_num_balls() is called"""
        self.physics.get_num_balls.assert_called_once()

    def test_add_ball_not_called(self) -> None:
        """Test that no new balls are added to the physics scene"""
        self.physics.add_ball.assert_not_called()

    def test_launch_ball_not_called(self) -> None:
        """Test that the launch_ball() method is not called."""
        self.physics.launch_ball.assert_not_called()

    def test_id_gen_not_called(self) -> None:
        """Test that the ID generator has not been called/used"""
        self.id_gen.generate_id.assert_not_called()


class TestHandleCenterButtonPressedWithNoBalls(unittest.TestCase):
    """Test the utils.handle_center_button_pressed() method when there are no balls
    left in the physics scene. In this case we expect that a new ball is both added and
    launched via the PhysicsInterface"""

    def setUp(self) -> None:
        cfg = pypinball.GameConfig(playing_area=(400, 400))
        self.id_gen = unittest.mock.MagicMock(wrap=pypinball.utils.ObjectIdGenerator())
        self.physics = unittest.mock.MagicMock(spec=pypinball.PhysicsInterface)
        self.physics.get_num_balls.return_value = 0

        pypinball.utils.handle_center_button_press(
            physics=self.physics, config=cfg, id_gen=self.id_gen
        )

    def test_get_num_balls_called(self) -> None:
        """Test that the get_num_balls() is called"""
        self.physics.get_num_balls.assert_called_once()

    def test_add_ball_called(self) -> None:
        """Test that no new balls are added to the physics scene"""
        self.physics.add_ball.assert_called_once()

    def test_launch_ball_called(self) -> None:
        """Test that the launch_ball() method is not called."""
        self.physics.launch_ball.assert_called_once()

    def test_id_gen_called(self) -> None:
        """Test that the ID generator has not been called/used"""
        self.id_gen.generate_id.assert_called_once()
