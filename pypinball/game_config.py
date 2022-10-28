import dataclasses
import typing

from . import domain, events


@dataclasses.dataclass
class GameConfig:
    """
    The GameConfig class is used to hold the configuration of a single instance of the game.

    - playing_area: The size of hte play area in pixels (width, height).
    - flippers: Specification of all flippers to create in the ``PhysicsInterface``.
    - walls: Specification of all walls to create in the ``PhysicsInterface``.
    - events_to_sounds: Mapping from ``GameEvents`` types to file paths for audio files.
    """

    playing_area: typing.Tuple[float, float]

    flippers: typing.List[domain.Flipper] = dataclasses.field(default_factory=list)

    walls: typing.List[domain.Wall] = dataclasses.field(default_factory=list)

    event_to_sounds: typing.Dict[events.GameEvents, str] = dataclasses.field(
        default_factory=dict
    )
