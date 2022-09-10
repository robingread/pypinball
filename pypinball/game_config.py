import dataclasses
import typing
from . import audio
from . import domain
from . import events


@dataclasses.dataclass
class GameConfig:
    playing_area: typing.Tuple[float, float]

    flippers: typing.List[domain.Flipper] = dataclasses.field(default_factory=list)

    walls: typing.List[domain.Wall] = dataclasses.field(default_factory=list)

    sound_to_file_map: typing.Dict[audio.Sounds, str] = dataclasses.field(
        default_factory=dict
    )

    event_to_sounds: typing.Dict[events.GameEvents, str] = dataclasses.field(
        default_factory=dict
    )
