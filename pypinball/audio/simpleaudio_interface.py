import os
import simpleaudio
from .audio_interface import AudioInterface
from .. import log

logger = log.get_logger(name=__name__)


class SimpleAudio(AudioInterface):
    def __init__(self, blocking=False):
        self._blocking = blocking

    def play_sound_file(self, file_path: str) -> bool:
        logger.debug(f"Playing sound file: {file_path}")

        if not os.path.isfile(file_path):
            logger.warning(f"Unknown find sound file: {file_path}")
            return False

        wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()

        if self._blocking:
            play_obj.wait_done()

        return True
