import dataclasses
import logging
import typing
import pymunk
from .physics_interface import PhysicsInterface
from .. import domain


@dataclasses.dataclass
class PymunkEntity:
    id: int
    body: pymunk.Body
    shape: pymunk.Shape

    @property
    def position(self) -> typing.Tuple[float, float]:
        return self.body.position


@dataclasses.dataclass
class PymunkFlipper:
    id: int
    actuation_direction: int
    flipper_body: pymunk.Body
    flipper_shape: pymunk.Poly
    joint_body: pymunk.Body
    joint: pymunk.PinJoint
    joint_limit: pymunk.RotaryLimitJoint
    spring: pymunk.DampedRotarySpring

    @property
    def angle(self) -> float:
        return self.flipper_body.angle

    @property
    def position(self) -> typing.Tuple[float, float]:
        return self.flipper_body.position

    def add_to_space(self, space) -> None:
        space.add(
            self.flipper_body,
            self.flipper_shape,
            self.joint_body,
            self.joint,
            self.joint_limit,
            self.spring,
        )

    def actuate(self) -> None:
        actuation_force = 10000
        self.flipper_body.apply_impulse_at_local_point(
            impulse=pymunk.Vec2d.unit()
            * actuation_force
            * self.actuation_direction
            * -1.0,
            point=(80, 0),
        )


def create_pymunk_ball(ball: domain.Ball) -> PymunkEntity:
    mass = 0.1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = ball.position
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    return PymunkEntity(id=0, body=body, shape=shape)


def create_pymunk_flipper(flipper: domain.Flipper) -> PymunkFlipper:
    fp = [(-20, -20), (-20, 20), (120, 10), (120, -10)]
    mass = 10
    moment = pymunk.moment_for_poly(mass, fp)

    flipper_body = pymunk.Body(mass, moment)
    flipper_body.position = flipper.config.position
    flipper_shape = pymunk.Poly(flipper_body, fp)

    flipper_body.angle = flipper.config.angle

    joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    joint_body.position = flipper.config.position
    joint_body.angle = flipper.config.angle
    joint = pymunk.PivotJoint(flipper_body, joint_body, (0, 0), (0, 0))

    flipper_shape.group = 1
    flipper_shape.elasticity = 0.5

    spring = pymunk.DampedRotarySpring(
        a=flipper_body,
        b=joint_body,
        rest_angle=0.0,
        stiffness=2000000,
        damping=1000,
    )

    joint_limit = pymunk.RotaryLimitJoint(
        a=joint_body,
        b=flipper_body,
        min=min(0.0, flipper.config.actuation_angle),
        max=max(0.0, flipper.config.actuation_angle),
    )

    return PymunkFlipper(
        id=flipper.uid,
        actuation_direction=flipper.config.actuation_direction,
        flipper_body=flipper_body,
        flipper_shape=flipper_shape,
        joint_body=joint_body,
        joint_limit=joint_limit,
        joint=joint,
        spring=spring,
    )


class PymunkPhysics(PhysicsInterface):
    def __init__(self):
        self._balls = dict()
        self._bumpers = list()
        self._flippers = dict()

        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

    def actuate_flipper(self, flipper: domain.Flipper) -> bool:
        try:
            self._flippers[flipper.uid].actuate()
            return True
        except KeyError:
            return False

    def add_ball(self, ball: domain.Ball) -> bool:
        if ball.uid in self._balls.keys():
            logging.warning(f"Unable to add ball. ID is already registered: {ball.uid}")
            return False
        entity = create_pymunk_ball(ball=ball)
        self._space.add(entity.body, entity.shape)
        self._balls[entity.id] = entity
        return True

    def add_flipper(self, flipper: domain.Flipper) -> bool:
        if flipper.uid in self._flippers.keys():
            logging.warning(
                f"Unable to add flipper. ID is already registered: {flipper.uid}"
            )
            return False
        entity = create_pymunk_flipper(flipper=flipper)
        entity.add_to_space(space=self._space)
        self._flippers[flipper.uid] = entity
        return True

    def get_ball_state(self, uid: int) -> domain.BallState:
        if uid not in self._balls.keys():
            raise KeyError(f"Unknown ball id: {uid}")
        return domain.BallState(uid=uid, position=self._balls[uid].position)

    def get_flipper_state(self, uid: int) -> domain.FlipperState:
        if uid not in self._flippers.keys():
            raise KeyError(f"Unknown flipper id: {uid}")
        return domain.FlipperState(
            angle=self._flippers[uid].angle, position=self._flippers[uid].position
        )

    def update(self) -> None:
        dt = 1.0 / 60.0 / 5.0
        for x in range(5):
            self._space.step(dt)
