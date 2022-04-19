import logging
from .input_interface import InputInterface
from .. import domain


class KeyboardInput(InputInterface):
    """
    Keyboard Input. This class reads the keyboard as inputs and maps the "f" key to the left button, the "j" key
    to the right button and the "spacebar" to firing the center button. Under the hood it uses the ``pyunput`` package.
    """

    def __init__(self):

        # We import here to avoid the unit tests from failing on Gitlab CI.
        logging.debug("Importing the pynput package")
        import pynput

        listener = pynput.keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release
        )
        listener.start()

        self._center_button_state = False
        self._left_button_state = False
        self._right_button_state = False

    def _on_press(self, key) -> None:
        logging.debug(f"Key pressed: {type(key)}")

        key_bode = pynput.keyboard.KeyCode()

        if not self._center_button_state and key == pynput.keyboard.Key.space:
            logging.debug("Center button pressed")
            self._center_button_state = True

        if not self._left_button_state and key == key_bode.from_char("f"):
            logging.debug("Left button pressed")
            self._left_button_state = True

        if not self._right_button_state and key == key_bode.from_char("j"):
            logging.debug("Right button pressed")
            self._right_button_state = True

    def _on_release(self, key) -> None:
        logging.debug(f"Key released: {key}")

        key_bode = pynput.keyboard.KeyCode()

        if self._center_button_state and key == pynput.keyboard.Key.space:
            logging.debug("Center button released")
            self._center_button_state = False

        if self._left_button_state and key == key_bode.from_char("f"):
            logging.debug("Left button released")
            self._left_button_state = False

        if self._right_button_state and key == key_bode.from_char("j"):
            logging.debug("Right button released")
            self._right_button_state = False

    def get_input_state(self) -> dict:

        ret = {
            domain.Buttons.CENTER: self._center_button_state,
            domain.Buttons.LEFT: self._left_button_state,
            domain.Buttons.RIGHT: self._right_button_state,
        }

        self._center_button_state = False
        self._left_button_state = False
        self._right_button_state = False

        return ret
