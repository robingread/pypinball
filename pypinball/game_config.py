import dataclasses
import typing

from . import domain, events


@dataclasses.dataclass
class GameConfig:
    playing_area: typing.Tuple[float, float]

    flippers: typing.List[domain.Flipper] = dataclasses.field(default_factory=list)

    walls: typing.List[domain.Wall] = dataclasses.field(default_factory=list)

    event_to_sounds: typing.Dict[events.GameEvents, str] = dataclasses.field(
        default_factory=dict
    )
