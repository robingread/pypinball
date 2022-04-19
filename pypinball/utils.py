import logging
import typing
from .audio import Sounds
from .domain import Buttons
from .physics import PhysicsInterface


INPUT_STATE = typing.Dict[Buttons, bool]
BUTTON_SOUND_MAP = typing.Dict[Buttons, Sounds]


def actuate_flippers(input_state: INPUT_STATE, physics: PhysicsInterface) -> None:
    """
    Actuate flippers in the Physics model based upon the button input state.

    Args:
        input_state (dict): Dictionary where keys are ``Button`` enums and the value is a ``bool``.
        physics (PhysicsInterface): Concrete physics interface.

    Returns:
        None
    """
    for button, state in input_state.items():
        if button == Buttons.CENTER:
            continue
        elif not state:
            continue
        physics.actuate_flippers(actuate_button=button)


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
