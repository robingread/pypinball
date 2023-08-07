import typing


class DisplayInterface(typing.Protocol):
    """The DisplayInterface class provides a Protocol specification
    of what class methods an implementation of an abstracted display
    is expected to have"""

    def clear(self) -> None:
        """
        Clear the display window.
        """

    def close(self) -> None:
        """
        Close the display window.
        """

    def draw_background(self) -> None:
        """
        Draw the background image in the display.
        """

    def draw_ball(
        self, pos: typing.Tuple[float, float], diameter: float, alpha: float
    ) -> None:
        """
        Helper function to draw a ball.

        Args:
            pos (tuple): Position in the format (x, y) both in pixel coordinates.
            diameter (float): Diameter of the ball in pixels.
            alpha (float): Alpha transparency. Values expected to be in the range [0, 1] where 1.0 means full opacity.
        """

    def draw_flipper(
        self,
        pos: typing.Tuple[float, float],
        angle: float,
        size: typing.Tuple[float, float],
        alpha: float,
    ) -> None:
        """Helper funcion to draw a flippper.

        Args:
            pos (tuple): Position of the center of the flipper in the format (x, y) both in pixel coordinates.
            size (tuple): Size of the bumper in (width, height) format in pixel coordinates.
            angle (float): Angle of the bumper.
            alpha (float): Alpha transparency. Values expected to be in the range [0, 1] where 1.0 means full opacity.
        """

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

    def draw_rectangle_bumper(
        self,
        pos: typing.Tuple[float, float],
        size: typing.Tuple[float, float],
        angle: float,
        alpha: float,
    ) -> None:
        """
        Args:
            pos (tuple): Position in the format (x, y) both in pixel coordinates.
            size (tuple): Size of the bumper in (width, height) format in pixel coordinates.
            angle (float): Angle of the bumper.
            alpha (float): Alpha transparency. Values expected to be in the range [0, 1] where 1.0 means full opacity.

        """

    def draw_lives(self, lives: int) -> None:
        """Draw the remaining number of lives the player has remaining.

        Args:
            lives (int): Number of lives.
        """

    def update(self) -> None:
        """
        Update the display. This is something that should be called on each loop of the game.
        """
