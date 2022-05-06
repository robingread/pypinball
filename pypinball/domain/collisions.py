import dataclasses
import enum


class CollisionType(enum.Enum):

    BALL_AND_BALL = enum.auto()
    BALL_AND_BUMPER = enum.auto()
    BALL_AND_FLIPPER = enum.auto()
    BALL_AND_WALL = enum.auto()


@dataclasses.dataclass
class Collision:
    type: CollisionType
    ball_id: int
    other_id: int
