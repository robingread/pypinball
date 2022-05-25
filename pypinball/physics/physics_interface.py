import typing
from .. import domain


class PhysicsInterface(typing.Protocol):
    """
    Definition of the Interface to a Physics Engine for the game. This class
    does not provide any implementation and should be inherited by any
    concrete implementation classes.
    """

    def actuate_flipper(self, uid: int) -> bool:
        """
        Actuate a flipper in the Physics simulation.

        Args:
            uid (int): Unique ID of the flipper.

        Returns:
            bool: ``True`` if the flipper has been added and was actuated, else ``False``.
        """

    def actuate_flippers(self, actuate_button: domain.Buttons) -> None:
        ...

    def add_ball(self, ball: domain.Ball) -> bool:
        ...

    def add_flipper(self, flipper: domain.Flipper) -> bool:
        ...

    def add_wall(self, wall: domain.Wall) -> bool:
        """
        Add a wall section to the Phyics scene.

        Args:
            wall (Wall): Wall section to add.

        Returns:
            bool: ``True`` if the wall was added successfully, else ``False``.
        """

    def get_collisions(self) -> typing.List[domain.Collision]:
        """
        Get a list of collisions that have taken place in the last update.

        Returns:
            list: List of collisions.
        """
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
        """
        Perform an update/tick of the Physics engine. This method should be
        called on a regular basis.

        Returns:
            None
        """
        ...
