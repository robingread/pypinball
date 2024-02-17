"""Module for testing the pypinball.physics.utils module."""

from pypinball.domain import Ball
from pypinball.physics import PymunkPhysics, utils


def test_remove_all_balls() -> None:
    """Test the pypinball.physics.utils.remove_all_balls() method."""
    physics = PymunkPhysics(event_pub=None, fps=50.0)
    physics.add_ball(ball=Ball(uid=0, position=(10, 10)))
    physics.add_ball(ball=Ball(uid=1, position=(15, 15)))

    assert physics.get_num_balls() == 2

    utils.remove_all_balls(physics=physics)

    assert physics.get_num_balls() == 0
