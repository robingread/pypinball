import logging
import typing
from .audio import AudioInterface, Sounds
from .domain import Buttons, Flipper, Collision, CollisionType
from .physics import PhysicsInterface


INPUT_STATE = typing.Dict[Buttons, bool]
BUTTON_SOUND_MAP = typing.Dict[Buttons, Sounds]
SOUND_FILE_MAP = typing.Dict[Sounds, str]


def actuate_flippers(
    input_state: INPUT_STATE,
    flippers: typing.List[Flipper],
    physics: PhysicsInterface,
) -> None:
    """
    Actuate flippers in the Physics model based upon the button input state.

    Args:
        input_state (dict): Dictionary where keys are ``Button`` enums and the value is a ``bool``.
        flippers (list): List of flippers in game.
        physics (PhysicsInterface): Concrete physics interface.

    Returns:
        None
    """
    pressed_buttons = [button for button, state in input_state.items() if state]

    for flipper in flippers:
        if flipper.config.actuation_button in pressed_buttons:
            physics.actuate_flipper(uid=flipper.uid)


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
    a = 0.0 <= ball_position[0] <= width
    b = 0.0 <= ball_position[1] <= height
    return all([a, b])
