import enum


class GameEvents(enum.Enum):
    """
    Game related event types. These should all be self explanatory.
    """

    BALL_LAUNCHED = enum.auto()
    BALL_LOST = enum.auto()
    COLLISION_BALL_BALL = enum.auto()
    COLLISION_BALL_BUMPER = enum.auto()
    COLLISION_BALL_FLIPPER = enum.auto()
    COLLISION_BALL_WALL = enum.auto()
    FLIPPER_ACTIVATED = enum.auto()
    GAME_OVER = enum.auto()
    GAME_STARTED = enum.auto()
    LIFE_LOST = enum.auto()
    QUIT = enum.auto()
