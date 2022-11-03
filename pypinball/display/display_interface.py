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

    def draw_round_bumper(
        self,
        pos: typing.Tuple[float, float],
        diameter: float,
        alpha: float,
    ) -> None:
        """
        Helper function to draw a round bumper.

        Args:
            pos (tuple): Position in the format (x, y) both in pixel coordinates.
            diameter (float): Diameter of the bumper in of the ball in pixels.
            alpha (float): Alpha transparency. Values expected to be in the range [0, 1] where 1.0 means full opacity.
        """

    def update(self) -> None:
        """ """
