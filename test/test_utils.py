import random
import unittest
import unittest.mock

import pypinball


class MockDisplay(pypinball.DisplayInterface):
    """Mock DisplayInterface class to be used to unit-testing purposes."""

    def __init__(self) -> None:
        self.draw_ball = unittest.mock.MagicMock()
        self.draw_flipper = unittest.mock.MagicMock()
        self.draw_rectangle_bumper = unittest.mock.MagicMock()
        self.draw_round_bumper = unittest.mock.MagicMock()


class TestBallWithinAreaFunction(unittest.TestCase):
    """
    Test the utils.check_ball_is_within_area() method.
    """

    def setUp(self) -> None:
        self.width = 100
        self.height = 100

    def test_ball_within_area(self):
        """
        Test the condition where the ball is within the area.
        """
        position = (10, 10)
        self.assertTrue(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_above(self):
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

    def test_ball_outside_area_below(self):
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

    def test_ball_outside_area_left(self):
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

    def test_ball_outside_area_right(self):
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
            ball = pypinball.domain.BallState(uid=uid, position=(0.0, 0.0))
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
        pypinball.utils.render_phyisics_flippers(
            flippers=flippers, display=self.display
        )
        self.display.draw_flipper.assert_not_called()

    def test_call_with_single_flipper(self) -> None:
        """Test call the method with a list containing a single flipper state."""
        flippers = [
            pypinball.domain.FlipperState(
                uid=0, position=(10, 10), angle=1.0, length=20
            )
        ]
        pypinball.utils.render_phyisics_flippers(
            flippers=flippers, display=self.display
        )
        self.display.draw_flipper.assert_called_once()
