import typing

from .audio_interface import AudioInterface


class MockAudioInterface(AudioInterface):
    """
    The ``MockAudioInterface`` is an implementation of the ``AudioInterface``
    that is intended for testing purposes. It does not play any audio, but simply
    keeps an internal list of the sound files that have been requested via the
    ``play_sound_file()`` method.
    """

    def __init__(self):
        self._sounds = list()

    @property
    def sounds(self) -> typing.List[str]:
        """
        Get the list of sound files that have been played.

        Returns:
            list: List of strings.
        """
        return self._sounds

    def clear(self) -> None:
        """
        Clear the list of played sound files.

        Returns:
            None
        """
        self._sounds.clear()

    def play_sound_file(self, file_path: str) -> bool:
        self._sounds.append(file_path)
        return True
