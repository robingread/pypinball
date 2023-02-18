import math
import unittest

import pypinball


class TestCalculateRectangleBoundingBox(unittest.TestCase):
    def setUp(self) -> None:
        self.width = 100
        self.height = 25

    def test_rectangle_rotated_0_rad(self) -> None:
        angle = 0.0

        res = pypinball.display.utils.calculate_rotated_rectangle_bounding_box(
            width=self.width, height=self.height, angle=angle
        )
        exp = (self.width, self.height)

        self.assertTupleEqual(
            res,
            exp,
            msg="The expected bounding box size does not match the expected one",
        )

    def test_rectangle_rotated_360_rad(self) -> None:
        """Test the function on a bounding box rotated +360 degrees."""
        angle = math.pi

        res = pypinball.display.utils.calculate_rotated_rectangle_bounding_box(
            width=self.width, height=self.height, angle=angle
        )
        exp = (self.width, self.height)

        self.assertTupleEqual(
            res,
            exp,
            msg="The expected bounding box size does not match the expected one",
        )

    def test_rectangle_rotated_neg_360_rad(self) -> None:
        """Test the function on a bounding box rotated -360 degrees."""
        angle = math.pi * -1.0

        res = pypinball.display.utils.calculate_rotated_rectangle_bounding_box(
            width=self.width, height=self.height, angle=angle
        )
        exp = (self.width, self.height)

        self.assertTupleEqual(
            res,
            exp,
            msg="The expected bounding box size does not match the expected one",
        )

    def test_rectangle_rotated_90_deg(self) -> None:
        angle = math.pi * 0.5

        res = pypinball.display.utils.calculate_rotated_rectangle_bounding_box(
            width=self.width, height=self.height, angle=angle
        )
        exp = (self.height, self.width)

        self.assertTupleEqual(
            res,
            exp,
            msg="The expected bounding box size does not match the expected one",
        )

    def test_rectangle_rotated_neg_90_deg(self) -> None:
        angle = math.pi * -0.5

        res = pypinball.display.utils.calculate_rotated_rectangle_bounding_box(
            width=self.width, height=self.height, angle=angle
        )
        exp = (self.height, self.width)

        self.assertTupleEqual(
            res,
            exp,
            msg="The expected bounding box size does not match the expected one",
        )
