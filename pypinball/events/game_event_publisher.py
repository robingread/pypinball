from .event_publisher import EventPublisher
from .game_events import GameEvents


class GameEventPublisher(EventPublisher):
    """
    Class for publishing different game events (see the GameEvent enums).
    """

    def __init__(self) -> None:
        super().__init__(event_type=GameEvents)
