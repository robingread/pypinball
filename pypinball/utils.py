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


def launch_new_ball(
    input_state: INPUT_STATE, lives: int, physics: PhysicsInterface
) -> bool:
    """
    Launch a new ball, but only if there are enough lives and the center
    button has been pressed.

    Args:
        input_state (dict): Dictionary where keys are ``Button`` enums and the value is a ``bool``.
        lives (int): Number of lives left.
        physics (PhysicsInterface): Concrete physics interface.

    Returns:
        bool: Whether a new ball has been launched.
    """
    if lives == 0:
        return False
    elif not input_state[Buttons.CENTER]:
        return False
    return True


def handle_input_button_audio(
    input_state: INPUT_STATE,
    audio_interface: AudioInterface,
    button_to_sound_map: BUTTON_SOUND_MAP,
    sound_to_file_map: SOUND_FILE_MAP,
) -> None:
    """
    Play audio files based on input button state.

    Args:
        input_state (dict): Input button state.
        audio_interface (AudioInterface): Audio interface for playing audio.
        button_to_sound_map (dict): Mapping buttons to game sounds.
        sound_to_file_map (dict): Mapping game sounds to audio file paths.

    Returns:
        None
    """
    sounds = map_button_state_to_sound_type(
        input_state=input_state, sound_map=button_to_sound_map
    )

    for sound in sounds:
        file_path = sound_to_file_map[sound]
        audio_interface.play_sound_file(file_path)


def map_button_state_to_sound_type(
    input_state: INPUT_STATE, sound_map: BUTTON_SOUND_MAP
) -> list:
    """
    Map the input ``Button`` state to a specified ``Sound`` type. This method
    checks the state of the inputs and specifies which sound types should be
    played as a result.

    Args:
        input_state (dict): Dictionary where keys are ``Button`` enums and the value is a ``bool``.
        sound_map (dict): Dictionary where keys are ``Button`` enums and the value is a ``Sound`` enum.

    Returns:
        list: List of ``Sound`` types to play.
    """
    ret = list()
    for input_key, state in input_state.items():
        if not state:
            continue
        try:
            sound = sound_map[input_key]
            ret.append(sound)
        except KeyError:
            logging.warning(
                f"Unable to map button: {input_key}. The button is not in the sound map."
            )
    return ret
