import unittest
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
