import dataclasses
import enum
import random
import threading
import typing

import pymunk
import pymunk.pygame_util

from .. import domain, events, log
from .physics_interface import PhysicsInterface

logger = log.get_logger(name=__name__)


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
    """Data class to bring together all the Pymunk specific data and objects for a ball."""

    id: int
    body: pymunk.Body
    shape: pymunk.Circle

    @property
    def position(self) -> typing.Tuple[float, float]:
        """Get the position of the ball.

        Returns:
            typing.Tuple[float, float]: Position in the format (x, y).
        """
        return self.body.position

    @property
    def radius(self) -> float:
        """Get the radius of the ball.

        Returns:
            float: Ball radius.
        """
        return self.shape.radius

    def add_to_space(self, space: pymunk.Space) -> None:
        """Add the pymunk objects/data to the space.

        Args:
            space (pymunk.Space): Pymunk space.
        """
        space.add(self.body, self.shape)

    def apply_impulse(self, direction: typing.Tuple[float, float]) -> None:
        """Apply an impluse force to the ball in a given (unit vector) direction.

        Args:
            direction (typing.Tuple[float, float]): Direction unit vector.
        """
        force = random.randint(75_000, 120_000)
        force_vec = pymunk.Vec2d(x=direction[0], y=direction[1]) * force
        position = self.body.position
        self.body.apply_force_at_world_point(force=force_vec, point=position)

    def remove_from_space(self, space: pymunk.Space) -> None:
        """Remove the pymunk data/objects from a space.

        Args:
            space (pymunk.Space): Space to remove the objects from.
        """
        space.remove(self.body, self.shape)


@dataclasses.dataclass
class PymunkBumper:
    """Data class to bring together all the Pymunk specific data and objects for
    a (rectangle or round) bumper.
    """

    uid: int
    body: pymunk.Body
    shape: pymunk.Shape
    type: domain.BumperType
    config: typing.Union[domain.RoundBumper, domain.RectangleBumper]

    def add_to_space(self, space: pymunk.Space) -> None:
        """Add the pymunk objects/data to the space.

        Args:
            space (pymunk.Space): Pymunk space.
        """
        space.add(self.body, self.shape)

    def remove_from_space(self, space: pymunk.Space) -> None:
        """Remove the pymunk data/objects from a space.

        Args:
            space (pymunk.Space): Space to remove the objects from.
        """
        space.remove(self.body, self.shape)


@dataclasses.dataclass
class PymunkFlipper:
    """Data class to bring together all the Pymunk specific data and objects for
    a flipper.
    """

    id: int
    actuation_direction: int
    flipper_body: pymunk.Body
    flipper_shape: pymunk.Poly
    joint_body: pymunk.Body
    joint: pymunk.PivotJoint
    joint_limit: pymunk.RotaryLimitJoint
    spring: pymunk.DampedRotarySpring
    config: domain.FlipperConfig

    @property
    def angle(self) -> float:
        """Get the current rotation angle of the flipper.

        Returns:
            float: Angle in radians.
        """
        return self.flipper_body.angle

    @property
    def position(self) -> typing.Tuple[float, float]:
        """Get the position of the flipper.

        Returns:
            typing.Tuple[float, float]: Position in the format (x, y).
        """
        return self.flipper_body.position

    def add_to_space(self, space: pymunk.Space) -> None:
        """Add the pymunk objects/data to the space.

        Args:
            space (pymunk.Space): Pymunk space.
        """
        space.add(
            self.flipper_body,
            self.flipper_shape,
            self.joint_body,
            self.joint,
            self.joint_limit,
            self.spring,
        )

    def actuate(self) -> None:
        """Actuate the flipper."""
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
    """Data class to bring together all the Pymunk specific data and objects for
    a list of wall segments.
    """

    id: int
    segment_bodies: typing.List[pymunk.Segment]

    def add_to_space(self, space: pymunk.Space) -> None:
        """Add the pymunk objects/data to the space.

        Args:
            space (pymunk.Space): Pymunk space.
        """
        for segment in self.segment_bodies:
            space.add(segment)


# TODO: Unit-test this method.
def create_pymunk_ball(ball: domain.Ball) -> PymunkEntity:
    """Create a ball data structure from a domain specified ball.

    Args:
        ball (domain.Ball): Domain model of a Ball.

    Returns:
        PymunkEntity: Populated data structure.
    """
    mass = 0.1
    radius = ball.radius
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = ball.position
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    shape.collision_type = CollisionEntity.BALL
    return PymunkEntity(id=ball.uid, body=body, shape=shape)


def create_round_bumper(bumper: domain.RoundBumper) -> PymunkBumper:
    """Create a PymunkBumper data structure containing all the Pymunk specific objects
    for a bumper.

    Args:
        bumper (domain.RoundBumper): Bumper configuration from the domain model.

    Returns:
        PymunkBumper: Pymunk specific data/objects.
    """
    mass = 0.1
    radius = bumper.radius
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass=mass, moment=inertia, body_type=pymunk.Body.STATIC)
    body.position = bumper.position
    shape = pymunk.Circle(body=body, radius=radius)
    shape.elasticity = 1.2
    shape.collision_type = CollisionEntity.BUMPER
    return PymunkBumper(
        uid=bumper.uid,
        body=body,
        shape=shape,
        type=domain.BumperType.ROUND,
        config=bumper,
    )


def create_rectangle_bumper(bumper: domain.RectangleBumper) -> PymunkBumper:
    """Create a PymunkBumper data structure for a rectangular bumper.

    Args:
        bumper (domain.RectangleBumper): Bumper configuration from the domain model.

    Returns:
        PymunkBumper: Pymunk specific data/objects.
    """
    width, height = bumper.size
    mass = 0.1
    inertia = pymunk.moment_for_box(mass=mass, size=bumper.size)
    body = pymunk.Body(mass=mass, moment=inertia, body_type=pymunk.Body.STATIC)
    body.position = bumper.position
    body.angle = bumper.angle
    shape = pymunk.Poly(
        body=body,
        vertices=[
            (-width / 2, -height / 2),
            (width / 2, -height / 2),
            (width / 2, height / 2),
            (-width / 2, height / 2),
        ],
    )
    shape.elasticity = 1.2
    shape.collision_type = CollisionEntity.BUMPER
    return PymunkBumper(
        uid=bumper.uid,
        body=body,
        shape=shape,
        type=domain.BumperType.RECTANGLE,
        config=bumper,
    )


def create_pymunk_flipper(flipper: domain.Flipper) -> PymunkFlipper:
    """Create a PymunkBumper data structure for a flipper given a domain model configuration.

    Args:
        flipper (domain.Flipper): Flipper configuration from the domain model.

    Returns:
        PymunkFlipper: Pymunk specific data/objects.
    """
    vertices = [
        (-20, -20),
        (-20, 20),
        (flipper.config.length, 10),
        (flipper.config.length, -10),
    ]
    # TODO: This seems to be a very carefully coded value! It can easily break tests!
    mass = 8
    moment = pymunk.moment_for_poly(mass, vertices=vertices)

    flipper_body = pymunk.Body(mass, moment)
    flipper_body.position = flipper.config.position
    flipper_shape = pymunk.Poly(flipper_body, vertices=vertices)

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
        config=flipper.config,
        actuation_direction=flipper.config.actuation_direction,
        flipper_body=flipper_body,
        flipper_shape=flipper_shape,
        joint_body=joint_body,
        joint_limit=joint_limit,
        joint=joint,
        spring=spring,
    )


def create_pymunk_wall(wall: domain.Wall, space: pymunk.Space) -> PymunkWall:
    """Create a PymunkBumper data structure for a wall segment.

    Args:
        wall (domain.Wall): Wall segment configuration from the domain model.
        space (pymunk.Space): Pymunk space to use as a static body.

    Returns:
        PymunkWall: Pymunk specific data/objects.
    """
    num_points = len(wall.points) - 1
    segment_radius = 1
    segments = list()
    for i in range(num_points):
        j = i + 1
        segment = pymunk.Segment(
            body=space.static_body,
            a=wall.points[i],
            b=wall.points[j],
            radius=segment_radius,
        )
        segment.collision_type = CollisionEntity.WALL
        segment.elasticity = 0.75
        segments.append(segment)
    return PymunkWall(id=wall.uid, segment_bodies=segments)


class CollisionHandler:  # pylint: disable=too-few-public-methods
    """Collision handler class for interactions between balls, bumpers, flippers and walls."""

    def __init__(
        self,
        event_pub: events.GameEventPublisher,
        space: pymunk.Space,
        balls: typing.Dict[int, PymunkEntity],
        bumpers: typing.Dict[int, PymunkBumper],
        flippers: typing.Dict[int, PymunkFlipper],
        walls: typing.Dict[int, PymunkWall],
    ) -> None:
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
        self,
        arbiter: pymunk.Arbiter,
        space: pymunk.Space,  # pylint: disable=unused-argument
        data: dict,  # pylint: disable=unused-argument
    ) -> bool:
        """Handle Pymunk physics collisions.

        Args:
            arbiter (pymunk.Arbiter): Pymunk arbiter.
            space (pymunk.Space): Pymink space the collision bodies are in.
            data (dict): Data dictionary that can be populated optionally.

        Returns:
            bool: If the collision was handled.
        """
        other_shape = arbiter.shapes[1]

        if other_shape.collision_type == CollisionEntity.WALL:
            for _, wall in self._walls.items():
                for segment in wall.segment_bodies:
                    if segment == other_shape:
                        self._event_pub.emit(
                            event=events.GameEvents.COLLISION_BALL_WALL
                        )
                        return True

        elif other_shape.collision_type == CollisionEntity.BALL:
            for _, ball in self._balls.items():
                if other_shape != ball.shape:
                    continue
                self._event_pub.emit(event=events.GameEvents.COLLISION_BALL_BALL)
                return True

        elif other_shape.collision_type == CollisionEntity.FLIPPER:
            for _, flipper in self._flippers.items():
                if other_shape != flipper.flipper_shape:
                    continue
                self._event_pub.emit(event=events.GameEvents.COLLISION_BALL_FLIPPER)
                return True

        elif other_shape.collision_type == CollisionEntity.BUMPER:
            for _, bumper in self._bumpers.items():
                if other_shape != bumper.shape:
                    continue
                self._event_pub.emit(event=events.GameEvents.COLLISION_BALL_BUMPER)
                return True

        return True


class PymunkPhysics(PhysicsInterface):
    """Implementation of the PhysicsInterface class that uses Pymunk as the underlying
    physics modelling solution.
    """

    def __init__(self, event_pub: events.GameEventPublisher, fps: float) -> None:
        self._balls: typing.Dict[int, PymunkEntity] = dict()
        self._bumpers: typing.Dict[int, PymunkBumper] = dict()
        self._flippers: typing.Dict[int, PymunkFlipper] = dict()
        self._walls: typing.Dict[int, PymunkWall] = dict()
        self._event_pub = event_pub
        self._threading_lock = threading.Lock()
        self._fps = fps

        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        self._draw_options: typing.Optional[pymunk.pygame_util.DrawOptions] = None

        self._collision_handler = CollisionHandler(
            event_pub=event_pub,
            space=self._space,
            balls=self._balls,
            bumpers=self._bumpers,
            flippers=self._flippers,
            walls=self._walls,
        )

    def actuate_flipper(self, uid: int) -> bool:
        with self._threading_lock:
            try:
                self._flippers[uid].actuate()
                self._event_pub.emit(event=events.GameEvents.FLIPPER_ACTIVATED)
                return True
            except KeyError:
                return False

    def add_ball(self, ball: domain.Ball) -> bool:
        with self._threading_lock:
            if ball.uid in self._balls.keys():
                logger.warning(
                    f"Unable to add ball. ID is already registered: {ball.uid}"
                )
                return False
            entity = create_pymunk_ball(ball=ball)
            entity.add_to_space(space=self._space)
            self._balls[ball.uid] = entity
            return True

    def add_bumper(self, bumper: domain.Bumper) -> bool:
        with self._threading_lock:
            if bumper.uid in self._bumpers.keys():
                logger.warning(
                    f"Unable to add bumper. ID is already registered: {bumper.uid}"
                )
                return False

            if isinstance(bumper, domain.RoundBumper):
                entity = create_round_bumper(bumper=bumper)
            elif isinstance(bumper, domain.RectangleBumper):
                entity = create_rectangle_bumper(bumper=bumper)
            else:
                raise ValueError()

            entity.add_to_space(space=self._space)
            self._bumpers[bumper.uid] = entity
            return True

    def add_flipper(self, flipper: domain.Flipper) -> bool:
        with self._threading_lock:
            if flipper.uid in self._flippers.keys():
                logger.warning(
                    f"Unable to add flipper. ID is already registered: {flipper.uid}"
                )
                return False
            entity = create_pymunk_flipper(flipper=flipper)
            entity.add_to_space(space=self._space)
            self._flippers[flipper.uid] = entity
            return True

    def add_wall(self, wall: domain.Wall) -> bool:
        with self._threading_lock:
            if wall.uid in self._walls.keys():
                logger.warning(
                    f"Unable to add wall. ID is already registered: {wall.uid}"
                )
                return False
            entity = create_pymunk_wall(wall=wall, space=self._space)
            entity.add_to_space(space=self._space)
            self._walls[wall.uid] = entity
            return True

    def get_ball_state(self, uid: int) -> domain.BallState:
        if uid not in self._balls.keys():
            raise KeyError(f"Unknown ball id: {uid}")
        return domain.BallState(
            uid=uid, position=self._balls[uid].position, radius=self._balls[uid].radius
        )

    def get_ball_states(self) -> typing.List[domain.BallState]:
        return [self.get_ball_state(uid=uid) for uid in self._balls.keys()]

    def get_bumper_state(self, uid: int) -> domain.Bumper:
        if uid not in self._bumpers.keys():
            raise KeyError(f"Unknown bumper id: {uid}")
        return self._bumpers[uid].config

    def get_bumper_states(self) -> typing.List[domain.Bumper]:
        return [self.get_bumper_state(uid=uid) for uid in self._bumpers.keys()]

    def get_flipper_state(self, uid: int) -> domain.FlipperState:
        if uid not in self._flippers.keys():
            raise KeyError(f"Unknown flipper id: {uid}")
        return domain.FlipperState(
            uid=uid,
            angle=self._flippers[uid].angle,
            position=self._flippers[uid].position,
            length=self._flippers[uid].config.length,
        )

    def get_flipper_states(self) -> typing.List[domain.FlipperState]:
        return [self.get_flipper_state(uid=uid) for uid in self._flippers.keys()]

    def get_num_balls(self) -> int:
        return len(self._balls.keys())

    def launch_ball(self, uid: int) -> bool:
        with self._threading_lock:
            if uid not in self._balls.keys():
                msg = f"Failed to launch ball with UID {uid}. This ID is not registred in the Physics implementaion."
                logger.warning(msg)
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
        """Get a PyGame display surface for debugging.

        Args:
            screen (pygame.Surface): PyGame display surface.
        """
        self._draw_options = pymunk.pygame_util.DrawOptions(screen)

    def update(self) -> None:
        with self._threading_lock:
            logger.debug("Updating Pymunk Physics")

            sub_step = 5
            delta_time = 1.0 / self._fps / float(sub_step)
            for _ in range(sub_step):
                self._space.step(delta_time)

            if self._draw_options is not None:
                self._space.debug_draw(options=self._draw_options)
