import typing
from ..event import Event


class DisplayInterface(typing.Protocol):

    window_close: Event

    def clear(self) -> None:
        """
        Clear the display window.

        Returns:
            None
        """

    def close(self) -> None:
        """
        Close the display window.

        Returns:
            None
        """

    def display_image(self, path: str) -> None:
        """ """

    def draw_ball(self, pos: list, radius: int) -> None:
        """ """

    def draw_flipper(self) -> None:
        """ """

    def update(self) -> None:
        """ """
