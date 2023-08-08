import unittest.mock

import pytest

import pypinball

EVENTS_TO_SOUND_PATHS = {
    pypinball.events.GameEvents.GAME_STARTED: "game_started_sound",
    pypinball.events.GameEvents.GAME_OVER: "game_over_sound",
}


@pytest.fixture
def audio_handler():
    handler = pypinball.audio.AudioGameEventHandler(
        interface=unittest.mock.MagicMock(spec=pypinball.AudioInterface),
        events_to_sound=EVENTS_TO_SOUND_PATHS,
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
    audio_handler.interface.play_sound_file.assert_called_once_with(file_path=exp_file)


def test_handler_doesnt_play_unregistered_sound(audio_handler):
    """
    Test that when the audio event handler receives an event update that has a
    mapping to a sound file, the audio player plays DOES NOT that sound.
    """
    event = pypinball.events.GameEvents.BALL_LOST
    audio_handler.update(event=event)
    audio_handler.interface.play_sound_file.assert_not_called()
