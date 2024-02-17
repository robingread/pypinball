from .physics_interface import PhysicsInterface


def remove_all_balls(physics: PhysicsInterface) -> None:
    """Remove all the balls from a PhysicsInstance instance/implementation.

    Args:
        physics (PhysicsInterface): Physics state to remove balls from.
    """
    states = physics.get_ball_states()
    for s in states:
        physics.remove_ball(uid=s.uid)
