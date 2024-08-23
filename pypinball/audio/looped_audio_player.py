"""Module that provides functionality for playing audio on a loop in the background."""

import threading
import time
import typing

import simpleaudio
from pydub import AudioSegment

from .. import log

LOGGER = log.get_logger(name="Looped Audio Player")


class LoopedAudioPlayer:
    """The LoopedAudioPlayer class is used to play audio on a loop. This is useful for
    playing background music in the game.

    The playing of the audio itself is done in a separate thread, and starting/stopping
    the class is thread safe.
    """

    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._is_playing = False
        self._thread: typing.Optional[threading.Thread] = None
        self._thread_lock = threading.Lock()
        self._audio = AudioSegment.from_mp3(file=filename)
        self._obj: simpleaudio.PlayObject = None

    ##################
    # Public Methods #
    ##################
    def get_filename(self) -> str:
        """Get the filename / path of the audio file being played.

        Returns:
            str: Full path of the file.
        """
        return self._filename

    def is_playing(self) -> bool:
        """Check whether this player is running/playing audio.

        Returns:
            bool: ``True`` if audio is playing, else ``False``.
        """
        return self._is_playing

    def play(self) -> bool:
        """Play the audio file on loop.

        Returns:
            bool: ``True`` if not audio is played, else ``False``.
        """
        LOGGER.debug(f"Playing audio file: {self.get_filename()}")
        with self._thread_lock:
            if self._is_playing:
                return False

        self._is_playing = True
        self._thread = threading.Thread(target=self._play_method, daemon=True)
        self._thread.start()
        return True

    def stop(self) -> bool:
        """Stop playing the loop

        Returns:
            bool: ``True`` if audio was playing, else ``False``.
        """
        LOGGER.debug(f"Stopping audio file: {self.get_filename()}")
        with self._thread_lock:
            if not self.is_playing():
                return False

            self._is_playing = False
            self._obj.stop()

            if self._thread is not None:
                self._thread.join()
                self._thread = None

            return True

    ###################
    # Private Methods #
    ###################
    def _play_method(self) -> None:
        """This method running the playback and looping and is the target method which
        is run in a separate thread."""
        while True:
            if not self.is_playing():
                return

            self._obj = simpleaudio.play_buffer(
                self._audio.raw_data,
                num_channels=self._audio.channels,
                bytes_per_sample=self._audio.sample_width,
                sample_rate=self._audio.frame_rate,
            )

            while self._obj.is_playing():
                time.sleep(0.05)
