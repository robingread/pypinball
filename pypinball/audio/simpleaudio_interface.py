import os
import typing

import simpleaudio

from .. import log
from .audio_interface import AudioInterface

logger = log.get_logger(name=__name__)


class SimpleAudio(AudioInterface):  # pylint: disable=too-few-public-methods
    """
    Implementation of the ``AudioInterface`` protocol that uses the ``simpleaudio``
    package to handle playing audio under the hood.
    """

    def __init__(self, blocking=False) -> None:
        self._blocking = blocking
        self._cache: typing.Dict[str, simpleaudio.WaveObject] = dict()

    def cached_files(self) -> typing.Set[str]:
        """Get a set of the cached files paths.

        Returns:
            set[str]: List of file paths.
        """
        return set(list(self._cache.keys()))

    def play_sound_file(self, file_path: str) -> bool:
        logger.debug(f"Playing sound file: {file_path}")

        if not os.path.isfile(file_path):
            logger.error(
                f"Unknown find sound file: {file_path}, skipping playing audio"
            )
            return False

        wave_obj = self.get_wav_sound(file_path=file_path)

        try:
            play_obj = wave_obj.play()
        except (
            simpleaudio._simpleaudio.SimpleaudioError  # pylint: disable=protected-access, c-extension-no-member
        ) as exep:
            logger.error(f"Failed to play audio file: {file_path}, exception: {exep}")
            return False

        if self._blocking:
            play_obj.wait_done()

        return True

    def get_wav_sound(self, file_path: str) -> simpleaudio.WaveObject:
        """Load a WAV object either from file or from an internal cache.

        Args:
            file_path (str): Path to WAV object.

        Returns:
            simpleaudio.WaveObject: WAV object to play.
        """
        try:
            ret = self._cache[file_path]
            logger.debug(f"Loaded audio file from cache: {file_path}")
            return ret

        except KeyError:
            wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)
            self._cache[file_path] = wave_obj
            logger.debug(f"Added audio file to cache: {file_path}")
            return wave_obj
