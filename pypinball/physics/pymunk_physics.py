import dataclasses
import enum
import logging
import typing
import pymunk
import pymunk.pygame_util
import random
from .physics_interface import PhysicsInterface
from .. import domain
from .. import events


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
        force = random.randint(75_000, 120_000)
        force_vec = pymunk.Vec2d(x=direction[0], y=direction[1]) * force
        position = self.body.position
        self.body.apply_force_at_world_point(force=force_vec, point=position)

    def remove_from_space(self, space: pymunk.Space) -> None:
        space.remove(self.body, self.shape)


@dataclasses.dataclass
class PymunkBumper:
    uid: int
    body: pymunk.Body
    shape: pymunk.Shape

    def add_to_space(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)

    def remove_from_space(self, space: pymunk.Space) -> None:
        space.remove(self.body, self.shape)


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


def create_round_bumper(bumper: domain.RoundBumper) -> PymunkBumper:
    mass = 0.1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass=mass, moment=inertia, body_type=pymunk.Body.STATIC)
    body.position = bumper.position
    shape = pymunk.Circle(body=body, radius=20)
    shape.elasticity = 1.2
    shape.collision_type = CollisionEntity.BUMPER
    return PymunkBumper(uid=bumper.uid, body=body, shape=shape)


def create_rectangle_bumper(bumper: domain.RectangleBumper) -> PymunkBumper:
    w, h = bumper.size
    mass = 0.1
    inertia = pymunk.moment_for_box(mass=mass, size=bumper.size)
    body = pymunk.Body(mass=mass, moment=inertia, body_type=pymunk.Body.STATIC)
    body.position = bumper.position
    body.angle = bumper.angle
    shape = pymunk.Poly(
        body=body,
        vertices=[(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)],
    )
    shape.elasticity = 1.2
    shape.collision_type = CollisionEntity.BUMPER
    return PymunkBumper(uid=bumper.uid, body=body, shape=shape)


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


class CollisionHandler:
    def __init__(
        self,
        event_pub: events.GameEventPublisher,
        space: pymunk.Space,
        balls: typing.Dict[int, PymunkEntity],
        bumpers: typing.Dict[int, PymunkBumper],
        flippers: typing.Dict[int, PymunkFlipper],
        walls: typing.Dict[int, PymunkWall],
    ):
        self._balls = balls
        self._bumpers = bumpers
        self._flippers = flippers
        self._walls = walls

        self._event_pub = event_pub
        self._space = space

        handler = self._space.add_wildcard_collision_handler(
            collision_type_a=CollisionEntity.BALL
        )
        handler.begin = self.handle_collision

    def handle_collision(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict
    ) -> bool:
        other_shape = arbiter.shapes[1]

        if other_shape.collision_type == CollisionEntity.WALL:
            for uid, wall in self._walls.items():
                for segment in wall.segment_bodies:
                    if segment == other_shape:
                        self._event_pub.emit(
                            event=events.GameEvents.COLLISION_BALL_WALL
                        )
                        return True

        elif other_shape.collision_type == CollisionEntity.BALL:
            for uid, ball in self._balls.items():
                if other_shape != ball.shape:
                    continue
                self._event_pub.emit(event=events.GameEvents.COLLISION_BALL_BALL)
                return True

        elif other_shape.collision_type == CollisionEntity.FLIPPER:
            for uid, flipper in self._flippers.items():
                if other_shape != flipper.flipper_shape:
                    continue
                self._event_pub.emit(event=events.GameEvents.COLLISION_BALL_FLIPPER)
                return True

        elif other_shape.collision_type == CollisionEntity.BUMPER:
            for uid, bumper in self._bumpers.items():
                if other_shape != bumper.shape:
                    continue
                self._event_pub.emit(event=events.GameEvents.COLLISION_BALL_BUMPER)
                return True

        return True


class PymunkPhysics(PhysicsInterface):
    def __init__(self, event_pub: events.GameEventPublisher):
        self._balls = dict()
        self._bumpers = dict()
        self._flippers = dict()
        self._walls = dict()
        self._event_pub = event_pub

        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        self._draw_options = None

        self._collision_handler = CollisionHandler(
            event_pub=event_pub,
            space=self._space,
            balls=self._balls,
            bumpers=self._bumpers,
            flippers=self._flippers,
            walls=self._walls,
        )

    def actuate_flipper(self, uid: int) -> bool:
        try:
            self._flippers[uid].actuate()
            self._event_pub.emit(event=events.GameEvents.FLIPPER_ACTIVATED)
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

    def add_bumper(self, bumper: domain.Bumper) -> bool:
        if bumper.uid in self._bumpers.keys():
            return False
        if isinstance(bumper, domain.RoundBumper):
            entity = create_round_bumper(bumper=bumper)
        else:
            entity = create_rectangle_bumper(bumper=bumper)
        entity.add_to_space(space=self._space)
        self._bumpers[bumper.uid] = entity
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

    def get_ball_state(self, uid: int) -> domain.BallState:
        if uid not in self._balls.keys():
            raise KeyError(f"Unknown ball id: {uid}")
        return domain.BallState(uid=uid, position=self._balls[uid].position)

    def get_ball_states(self) -> typing.List[domain.BallState]:
        return [self.get_ball_state(uid=uid) for uid in self._balls.keys()]

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
        self._event_pub.emit(event=events.GameEvents.BALL_LAUNCHED)
        return True

    def remove_ball(self, uid: int) -> bool:
        if uid not in self._balls.keys():
            return False
        self._balls[uid].remove_from_space(space=self._space)
        del self._balls[uid]
        return True

    def remove_bumper(self, uid) -> bool:
        if uid not in self._bumpers.keys():
            return False
        self._bumpers[uid].remove_from_space(space=self._space)
        del self._bumpers[uid]
        return True

    def set_debug_display(self, screen) -> None:
        self._draw_options = pymunk.pygame_util.DrawOptions(screen)

    def update(self) -> None:
        logging.debug("Updating Pymunk Physics")

        if self._draw_options is not None:
            self._space.debug_draw(options=self._draw_options)

        dt = 1.0 / 60.0 / 5.0
        for x in range(5):
            self._space.step(dt)
