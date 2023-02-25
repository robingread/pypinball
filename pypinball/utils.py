import math
import typing

from .display import DisplayInterface
from .domain import BallState, Bumper, BumperType, FlipperState
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
        display.draw_ball(pos=ball.position, diameter=ball.radius * 2.0, alpha=1.0)


def render_physics_bumpers(
    bumpers: typing.List[Bumper], display: DisplayInterface
) -> None:
    """Render a list fo Bumpers into the dislay.

    Args:
        bumpers (list): List of bumpers to render.
        display (DisplayInterface): Implementation of the display interface.
    """
    for bumper in bumpers:
        if bumper.type == BumperType.ROUND:
            display.draw_round_bumper(
                pos=bumper.position, diameter=bumper.radius * 2.0, alpha=1.0
            )
        elif bumper.type == BumperType.RECTANGE:
            display.draw_rectangle_bumper(
                pos=bumper.position, angle=bumper.angle, alpha=1.0, size=bumper.size
            )


def render_phyisics_flippers(
    flippers: typing.List[FlipperState], display: DisplayInterface
) -> None:
    """Render a list of FlipperState into the display.

    Args:
        flippers (list): List fo FlipperState instances.
        display (DisplayInterface): Implementation of the display interface.
    """
    for flipper in flippers:
        dx = (flipper.length * 0.5) * math.cos(flipper.angle)
        dy = (flipper.length * 0.5) * math.sin(flipper.angle)
        x = flipper.position[0] + dx
        y = flipper.position[1] + dy
        display.draw_flipper(
            pos=(x, y),
            angle=flipper.angle,
            size=(flipper.length, flipper.length * 0.35),
            alpha=1.0,
        )


def render_physics_state(physics: PhysicsInterface, display: DisplayInterface) -> None:
    """
    Render the state of the Physics scene in the display.

    Args:
        physics (PhysicsInterface): Physics to get the state from.
        display (DisplayInterface): Display to draw on.
    """
    render_physics_balls(balls=physics.get_ball_states(), display=display)
    render_physics_bumpers(bumpers=physics.get_bumper_states(), display=display)
    render_phyisics_flippers(flippers=physics.get_flipper_states(), display=display)
