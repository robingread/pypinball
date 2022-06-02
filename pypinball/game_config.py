import dataclasses
import typing
from . import audio


@dataclasses.dataclass
class GameConfig:
    sound_to_file_map: typing.Dict[audio.Sounds, str]
