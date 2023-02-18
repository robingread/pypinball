import math
import typing


def calculate_rotated_rectangle_bounding_box(
    width: float,
    height: float,
    angle: float,
) -> typing.Tuple[float, float]:
    """Given a rectangle with a known rotation angle, calulatue the encompasing bounding
    box. The width and height of the box are expected to be in the frame of the box.

    Args:
        width (float): Width of the rectangle.
        height (float): Height of the rectangle.
        angle (float): Angle the rectangle has been rotated by (in radians).

    Returns:
        typing.Tuple[float, float]: Width and height of the bounding box.
    """
    _width = math.fabs(math.sin(angle) * height) + math.fabs(math.cos(angle) * width)
    _height = math.fabs(math.sin(angle) * width) + math.fabs(math.cos(angle) * height)
    return (round(_width, 4), round(_height, 4))


def calculate_rectangle_bounding_box_image_coordinates(
    pos: typing.Tuple[float, float], size: typing.Tuple[float, float], angle: float
) -> typing.Tuple[float, float]:
    """
    Calculate the top-left coordinate of a bounding box for a rotated rectangle. This is
    useful when rendinering images (which have been scaled and rotated) using PyGame.

    Args:
        pos (tuple): Position of the rectangle centre in (x, y) format.
        size (tuple): Size of the rectangle in pixels in (width, height) format.
        angle (float): Angle of rectangle rotation in radians.

    Returns:
        typing.Tuple[float, float]: Top-left, (x, y) pixel coordinates of the bounding box.
    """
    width, height = calculate_rotated_rectangle_bounding_box(
        width=size[0], height=size[1], angle=angle
    )
    x = pos[0] - (width * 0.5)
    y = pos[1] - (height * 0.5)
    return x, y
