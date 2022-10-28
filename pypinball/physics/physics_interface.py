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

    def add_ball(self, ball: domain.Ball) -> bool:
        """
        Add a ball to the Physics simulation.

        Args:
            ball (Ball): Ball instance.

        Returns:
            bool: ``True`` if the ball was added else ``False``.
        """

    def add_bumper(self, bumper: domain.Bumper) -> bool:
        """
        Add a bumper to the Physics simulation.


        Args:
            bumper (Bumper): Bumper instance.

        Returns:
            bool: ``True`` is the bumper was added else ``False``.
        """

    def add_flipper(self, flipper: domain.Flipper) -> bool:
        """
        Addd a flipper to the Physics simulation
        Args:
            flipper (Flipper): Flipper instance.

        Returns:
            bool: ``True`` if the flipper was added else ``False``.
        """

    def add_wall(self, wall: domain.Wall) -> bool:
        """
        Add a wall section to the Physics simulation.

        Args:
            wall (Wall): Wall section to add.

        Returns:
            bool: ``True`` if the wall was added successfully, else ``False``.
        """

    def get_ball_state(self, uid: int) -> domain.BallState:
        """
        Get the state of a ball.

        Args:
            uid (int): Unique ID of the ball.

        Returns:
            BallState: State of the ball.
        """

    def get_ball_states(self) -> typing.List[domain.BallState]:
        """
        Get the state of all the balls.

        Returns:
            list: List of ``BallState`` instances.
        """

    def get_flipper_state(self, uid: int) -> domain.FlipperState:
        """
        Get the state of a flipper.

        Args:
            uid (int): ID of the flipper.

        Returns:
            FlipperState: State of the flipper.
        """

    def launch_ball(self, uid: int) -> bool:
        """
        Launch a ball by applying a high impulse/force to it.

        Args:
            uid (int): ID of the target ball.

        Returns:
            bool: ``True`` if successful else ``False``. For example specifying a ball that doesn't exist.
        """

    def remove_ball(self, uid: int) -> bool:
        """
        Remove a ball from the Physics simulation.

        Args:
            uid (int): Ball unique identifier.

        Returns:
            bool: ``True`` if the ball was removed, else ``False``.
        """

    def remove_bumper(self, uid) -> bool:
        """
        Remove a bumper from the Physics simulation.

        Args:
              uid (int): Bumper identifier.

        Returns:
            bool: ``True`` is the bumper was removed, else ``False``.
        """

    def set_gravity_vector(self, vec: typing.Tuple[float, float]) -> None:
        """
        Set the 2D gravity vector in the format (x, y).

        Args:
            vec: Vector.

        Returns:
            None
        """

    def update(self) -> None:
        """
        Perform an update/tick of the Physics engine. This method should be
        called on a regular basis.

        Returns:
            None
        """
