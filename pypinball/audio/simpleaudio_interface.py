import os

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

    def play_sound_file(self, file_path: str) -> bool:
        logger.debug(f"Playing sound file: {file_path}")

        if not os.path.isfile(file_path):
            logger.error(
                f"Unknown find sound file: {file_path}, skipping playing audio"
            )
            return False

        wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)

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
