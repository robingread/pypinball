import random
import unittest
import unittest.mock

import pypinball


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
    """
    Test the utils.render_physics_balls() method.
    """

    def setUp(self) -> None:
        class MockDisplay(pypinball.DisplayInterface):
            """Mock display class used for testing purposes"""

        self.display = MockDisplay()
        self.display.draw_ball = unittest.mock.MagicMock()

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
