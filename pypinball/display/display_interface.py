import typing


class DisplayInterface(typing.Protocol):
    """The DisplayInterface class provides a Protocol specification
    of what class methods an implementation of an abstracted display
    is expected to have"""

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
