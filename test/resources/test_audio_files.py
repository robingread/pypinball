"""Test that the audio files that are part of this repo have been downloaded correctly
using Git LFS. This is done by attempting to load the WAV files using simple_audio."""

import pytest
import simpleaudio

import pypinball


def load_audio(path: str) -> None:
    """Attempt to load an WAV audio file using simple_audio"""
    try:
        simpleaudio.WaveObject.from_wave_file(path)
    except Exception as exc:
        assert False, f"Failed to load audio file: {path}, raised an exception {exc}"


def test_load_audio() -> None:
    """Test that the load_audio() method throws an AssertionError when nonsense is
    passed to it."""
    with pytest.raises(AssertionError):
        load_audio("haha.txt")


files = [
    "ball_launch.wav",
    "ball_lost.wav",
    "Bounce1.wav",
    "Bounce4.wav",
    "flipper_actuated.wav",
    "redPowerup3.wav",
]


@pytest.mark.parametrize("file", files)
def test_load_ball_launched_sound(file: str) -> None:
    """Test that simple audio can load the ball_launch.wav file."""
    path = pypinball.resources.get_audio_resource_path(file)
    load_audio(path)
