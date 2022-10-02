import typing

from .. import domain


class InputInterface(typing.Protocol):
    """
    Input Interface protocol definition. This is an interface class and does not implement any actual behaviour.
    Concrete implementations of input interfaces should either inherit from this class or implement the same
    methods.
    """

    def get_input_state(self) -> typing.Dict[domain.Buttons, bool]:
        """
        Get the state of the input buttons. This method returns a dictionary where each button is a key and the value
        is a boolean value. ``True`` denotes that the button is pressed, and ``False`` denotes that the button is not
        pressed.

        Returns:
            dict: State dictionary.
        """
