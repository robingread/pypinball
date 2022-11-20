import typing

from .display import DisplayInterface
from .domain import BallState, Bumper, BumperType
from .physics import PhysicsInterface


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


def render_physics_balls(
    balls: typing.List[BallState], display: DisplayInterface
) -> None:
    """
    Render/draw the current state of the Balls in the Phyics simulation.

    Args:
        balls (list): List of ``BallState`` values.
        display (DisplayInterface): Display to draw the balls onto.
    """
    for ball in balls:
        display.draw_ball(pos=ball.position, diameter=30, alpha=1.0)


def render_physics_bumpers(
    bumpers: typing.List[Bumper], display: DisplayInterface
) -> None:
    for bumper in bumpers:
        if bumper.type == BumperType.ROUND:
            display.draw_round_bumper(
                pos=bumper.position, diameter=bumper.radius * 2.0, alpha=1.0
            )


# TODO: Unit test this method.
def render_physics_state(physics: PhysicsInterface, display: DisplayInterface) -> None:
    """
    Render the state of the Physics scene in the display.

    Args:
        physics (PhysicsInterface): Physics to get the state from.
        display (DisplayInterface): Display to draw on.
    """
    render_physics_balls(balls=physics.get_ball_states(), display=display)
    render_physics_bumpers(bumpers=physics.get_bumper_states(), display=display)
