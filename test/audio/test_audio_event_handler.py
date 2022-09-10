import pypinball
import pytest


EVENTS_TO_SOUND_PATHS = {
    pypinball.events.GameEvents.GAME_STARTED: "game_started_sound",
    pypinball.events.GameEvents.GAME_OVER: "game_over_sound",
}


class MockAudioInterface(pypinball.audio.AudioInterface):
    def __init__(self):
        self.commands = list()

    def play_sound_file(self, file_path: str) -> bool:
        self.commands.append(file_path)
        return True


@pytest.fixture
def audio_handler():
    handler = pypinball.audio.AudioGameEventHandler(
        interface=MockAudioInterface(), events_to_sound=EVENTS_TO_SOUND_PATHS
    )
    return handler


def test_handler_plays_registered_sound(audio_handler):
    """
    Test that when the audio event handler receives an event update that has a
    mapping to a sound file, the audio player plays that sound.
    """
    event = pypinball.events.GameEvents.GAME_STARTED
    audio_handler.update(event=event)
    exp_file = audio_handler.events_to_sounds[event]
    assert audio_handler.interface.commands == [exp_file]


def test_handler_doesnt_play_unregistered_sound(audio_handler):
    """
    Test that when the audio event handler receives an event update that has a
    mapping to a sound file, the audio player plays DOES NOT that sound.
    """
    event = pypinball.events.GameEvents.BALL_LOST
    audio_handler.update(event=event)
    assert audio_handler.interface.commands == list()
