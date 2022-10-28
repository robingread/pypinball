import typing


def check_ball_is_within_area(
    ball_position: typing.Tuple[float, float], width: float, height: float
) -> bool:
    """
    Check whether a ball position is within the playing area.

    Args:
        ball_position (tuple): Ball position in the format (x, y).
        width (float): Area width.
        height (float): Area height.

    Returns:
        bool: ``True`` if the ball is within the area else ``False``.
    """
    ball_in_width = 0.0 <= ball_position[0] <= width
    ball_in_height = 0.0 <= ball_position[1] <= height
    return all([ball_in_width, ball_in_height])
