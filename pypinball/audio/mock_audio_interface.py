import typing
from .audio_interface import AudioInterface


# TODO: Unit test the MockAudioInterface class
# TODO: Write doc-stings or the MockAudioInterface class
class MockAudioInterface(AudioInterface):
    def __init__(self):
        self._sounds = list()

    @property
    def sounds(self) -> typing.List[str]:
        return self._sounds

    def clear(self) -> None:
        self._sounds.clear()

    def play_sound_file(self, file_path: str) -> bool:
        self._sounds.append(file_path)
        return True
