import enum


class Sounds(enum.Enum):
    """
    Define the different types of sound that are defined within the Game.
    """

    BALL_LAUNCH = enum.auto()
    BALL_LOST = enum.auto()
    FLIPPER_ACTIVATE = enum.auto()
    FLIPPER_BALL_BOUNCE = enum.auto()
    GAME_START = enum.auto()
    GAME_OVER = enum.auto()

    COLLISION_BALL_BALL = enum.auto()
    COLLISION_BALL_BUMPER = enum.auto()
    COLLISION_BALL_FLIPPER = enum.auto()
    COLLISION_BALL_WALL = enum.auto()
