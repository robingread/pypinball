import dataclasses
import pymunk
from .physics_interface import PhysicsInterface
from .. import domain


@dataclasses.dataclass
class PymunkEntity:
    id: int
    body: pymunk.Body
    shape: pymunk.Shape


def create_pymunk_ball(ball: domain.Ball) -> PymunkEntity:
    mass = 1
    radius = 25
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = ball.position
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    return PymunkEntity(id=0, body=body, shape=shape)


class PymunkPhysics(PhysicsInterface):
    def __init__(self):
        self._balls = list()
        self._bumpers = list()
        self._flippers = list()

        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

    def add_ball(self, ball: domain.Ball) -> None:
        entity = create_pymunk_ball(ball=ball)
        self._space.add(entity.body, entity.shape)
        self._balls.append(entity)

    def update(self) -> None:
        dt = 1.0 / 60.0 / 5.0
        for x in range(5):
            self._space.step(dt)
