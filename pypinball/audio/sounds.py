import enum


class Sounds(enum.Enum):
    """
    Define the different types of sound that are defined within the Game.
    """

    FLIPPER_ACTIVATE = enum.auto()
    FLIPPER_BALL_BOUNCE = enum.auto()
    GAME_START = enum.auto()
    GAME_OVER = enum.auto()
