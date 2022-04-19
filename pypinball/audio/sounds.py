import enum


class Sounds(enum.Enum):
    """
    Define the different types of sound that are defined within the Game.
    """

    BALL_LAUNCH = enum.auto()
    FLIPPER_ACTIVATE = enum.auto()
    FLIPPER_BALL_BOUNCE = enum.auto()
    GAME_START = enum.auto()
    GAME_OVER = enum.auto()
