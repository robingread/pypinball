import logging
import typing
from .audio_interface import AudioInterface
from .. import events


class AudioGameEventHandler:
    """
    The AudioGameEventHandler class is responsible for ensuring that the correct
    audio is played when game events are received. This is done by having a
    dictionary mapping between GameEvent enums and audio file paths and using an
    AudioInterface instance to play these files.
    """

    def __init__(
        self,
        interface: AudioInterface,
        events_to_sound: typing.Dict[events.GameEvents, str],
    ):
        self._interface = interface
        self._events_to_sounds = events_to_sound

    @property
    def events_to_sounds(self) -> typing.Dict[events.GameEvents, str]:
        """
        Get the dictionary mapping game events to audio file paths.

        Returns:
            dict: Mapping dictionary
        """
        return self._events_to_sounds

    @property
    def interface(self) -> AudioInterface:
        """
        Get the AudioInterface instance.

        Returns:
            AudioInterface: Interface.
        """
        return self._interface

    def update(self, event: events.GameEvents) -> None:
        """
        Update the handler with a given event.

        Args:
            event: Event type.

        Returns:
            None
        """
        try:
            self._interface.play_sound_file(file_path=self._events_to_sounds[event])
        except KeyError:
            logging.warning(
                f"Unmapped GameEvent enum: {event.name}. No audio will be played!"
            )
