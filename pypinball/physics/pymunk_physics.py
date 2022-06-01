import dataclasses
import enum
import logging
import typing
import pymunk
import random
from .physics_interface import PhysicsInterface
from .. import domain


class CollisionEntity(enum.IntEnum):
    """
    Enum for storing the different type of object in an enum which is used to
    identify the type of object (and ultimately collision) that has taken place.
    """

    BALL = enum.auto()
    BUMPER = enum.auto()
    FLIPPER = enum.auto()
    WALL = enum.auto()


@dataclasses.dataclass
class PymunkEntity:
    id: int
    body: pymunk.Body
    shape: pymunk.Shape

    @property
    def position(self) -> typing.Tuple[float, float]:
        return self.body.position

    def add_to_space(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)

    def apply_impulse(self, direction: typing.Tuple[float, float]) -> None:
        print("Applying impulse on ball")
        force = random.randint(75_000, 120_000)
        force_vec = pymunk.Vec2d(x=direction[0], y=direction[1]) * force
        position = self.body.position
        self.body.apply_force_at_world_point(force=force_vec, point=position)


@dataclasses.dataclass
class PymunkFlipper:
    id: int
    actuation_direction: int
    flipper_body: pymunk.Body
    flipper_shape: pymunk.Poly
    joint_body: pymunk.Body
    joint: pymunk.PivotJoint
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


@dataclasses.dataclass
class PymunkWall:
    id: int
    segment_bodies: typing.List[pymunk.Segment]

    def add_to_space(self, space: pymunk.Space) -> None:
        for segment in self.segment_bodies:
            space.add(segment)


def create_pymunk_ball(ball: domain.Ball) -> PymunkEntity:
    mass = 0.1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = ball.position
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    shape.collision_type = CollisionEntity.BALL
    return PymunkEntity(id=ball.uid, body=body, shape=shape)


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
    flipper_shape.collision_type = CollisionEntity.FLIPPER

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


def create_pymunk_wall(wall: domain.Wall, space: pymunk.Space) -> PymunkWall:
    n = len(wall.points) - 1
    segment_radius = 1
    segments = list()
    for i in range(n):
        j = i + 1
        segment = pymunk.Segment(
            body=space.static_body,
            a=wall.points[i],
            b=wall.points[j],
            radius=segment_radius,
        )
        segment.collision_type = CollisionEntity.WALL
        segment.elasticity = 0.9
        segments.append(segment)
    return PymunkWall(id=wall.uid, segment_bodies=segments)


class CollisionsHandler:
    def __init__(self):
        self._collisions = list()

    @property
    def collisions(self) -> typing.List[typing.Tuple[pymunk.Shape, pymunk.Shape]]:
        return self._collisions

    def clear(self) -> None:
        self._collisions.clear()

    def handle_collision(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict
    ) -> bool:
        self._collisions.append(arbiter.shapes)
        return True


class PymunkPhysics(PhysicsInterface):
    def __init__(self):
        self._balls = dict()
        self._bumpers = list()
        self._flippers = dict()
        self._walls = dict()

        self._collision_handler = CollisionsHandler()

        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)
        handler = self._space.add_wildcard_collision_handler(
            collision_type_a=CollisionEntity.BALL
        )
        handler.begin = self._collision_handler.handle_collision

    def actuate_flipper(self, uid: int) -> bool:
        try:
            self._flippers[uid].actuate()
            return True
        except KeyError:
            return False

    def add_ball(self, ball: domain.Ball) -> bool:
        if ball.uid in self._balls.keys():
            logging.warning(f"Unable to add ball. ID is already registered: {ball.uid}")
            return False
        entity = create_pymunk_ball(ball=ball)
        entity.add_to_space(space=self._space)
        self._balls[ball.uid] = entity
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

    def add_wall(self, wall: domain.Wall) -> bool:
        if wall.uid in self._walls.keys():
            logging.warning(f"Unable to add wall. ID is already registered: {wall.uid}")
            return False
        entity = create_pymunk_wall(wall=wall, space=self._space)
        entity.add_to_space(space=self._space)
        self._walls[wall.uid] = entity
        return True

    def get_collisions(self) -> typing.List[domain.Collision]:
        ret = list()

        for collision in self._collision_handler.collisions:
            ball_shape = collision[0]
            other_shape = collision[1]
            collision_type = -1

            ball_id = -1
            other_id = -1

            for uid, ball in self._balls.items():
                if ball_shape == ball.shape:
                    ball_id = uid

            if collision[1].collision_type == CollisionEntity.WALL:
                for uid, wall in self._walls.items():
                    for segment in wall.segment_bodies:
                        if segment == other_shape:
                            other_id = uid
                            collision_type = domain.CollisionType.BALL_AND_WALL

            ret.append(
                domain.Collision(
                    type=collision_type,
                    ball_id=ball_id,
                    other_id=other_id,
                )
            )

        return ret

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

    def launch_ball(self, uid: int) -> bool:
        if uid not in self._balls.keys():
            msg = f"Failed to launch ball with UID {uid}. This ID is not registred in the Physics implementaion."
            logging.warning(msg)
            return False
        self._balls[uid].apply_impulse(direction=(0.0, -1.0))
        return True

    def update(self) -> None:
        logging.debug("Updating Pymunk Physics")
        self._collision_handler.clear()

        dt = 1.0 / 60.0 / 5.0
        for x in range(5):
            self._space.step(dt)
