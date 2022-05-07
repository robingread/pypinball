import typing
from .. import domain


class PhysicsInterface(typing.Protocol):
    def actuate_flipper(self, flipper: domain.Flipper) -> bool:
        ...

    def actuate_flippers(self, actuate_button: domain.Buttons) -> None:
        ...

    def add_ball(self, ball: domain.Ball) -> bool:
        ...

    def add_flipper(self, flipper: domain.Flipper) -> bool:
        ...

    def get_ball_state(self, uid: int) -> domain.BallState:
        """
        Get the state of a ball.

        Args:
            uid (int): Unique ID of the ball.

        Returns:
            BallState: State of the ball.
        """
        ...

    def get_flipper_state(self, uid: int) -> domain.FlipperState:
        """
        Get the state of a flipper.

        Args:
            uid (int): ID of the flipper.

        Returns:
            FlipperState: State of the flipper.
        """
        ...

    def launch_ball(self, uid: int) -> bool:
        """
        Launch a ball by applying a high impulse/force to it.

        Args:
            uid (int): ID of the target ball.

        Returns:
            bool: ``True`` if successful else ``False``. For example specifying a ball that doesn't exist.
        """
        ...

    def set_gravity_vector(self, vec: typing.Tuple[float, float]) -> None:
        """
        Set the 2D gravity vector in the format (x, y).

        Args:
            vec: Vector.

        Returns:
            None
        """
        ...

    def update(self) -> None:
        ...
