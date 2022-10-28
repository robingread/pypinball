from .. import log
from .events import InputEventPublisher, InputEvents

logger = log.get_logger(name=__name__)

try:
    import pynput
except ImportError:
    logger.error(
        "Unable to import the pynput module. Beware, things may not work properly when it comes to reading keyboard input!"
    )


class KeyboardInput:
    """
    Keyboard Input. This class reads the keyboard as inputs and maps the "f" key to the left button, the "j" key
    to the right button and the "spacebar" to firing the center button. Under the hood it uses the ``pyunput`` package.
    """

    def __init__(self, event_pub: InputEventPublisher):

        self._event_pub = event_pub

        listener = pynput.keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release
        )
        listener.start()

        self._center_button_state = False
        self._left_button_state = False
        self._right_button_state = False

    def _on_press(self, key) -> None:
        logger.debug(f"Key pressed: {type(key)}")

        key_bode = pynput.keyboard.KeyCode()

        if not self._center_button_state and key == pynput.keyboard.Key.space:
            logger.debug("Center button pressed")
            self._center_button_state = True
            self._event_pub.emit(event=InputEvents.CENTER_BUTTON_PRESSED)

        if not self._left_button_state and key == key_bode.from_char("f"):
            logger.debug("Left button pressed")
            self._left_button_state = True
            self._event_pub.emit(event=InputEvents.LEFT_BUTTON_PRESSED)

        if not self._right_button_state and key == key_bode.from_char("j"):
            logger.debug("Right button pressed")
            self._right_button_state = True
            self._event_pub.emit(event=InputEvents.RIGHT_BUTTON_PRESSED)

    def _on_release(self, key) -> None:
        logger.debug(f"Key released: {key}")

        key_bode = pynput.keyboard.KeyCode()

        if self._center_button_state and key == pynput.keyboard.Key.space:
            logger.debug("Center button released")
            self._center_button_state = False

        if self._left_button_state and key == key_bode.from_char("f"):
            logger.debug("Left button released")
            self._left_button_state = False

        if self._right_button_state and key == key_bode.from_char("j"):
            logger.debug("Right button released")
            self._right_button_state = False
