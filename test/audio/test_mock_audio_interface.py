import pypinball
import pytest


@pytest.fixture()
def audio():
    return pypinball.audio.MockAudioInterface()


def test_audio_init(audio):
    assert len(audio.sounds) == 0


def test_audio_play_file(audio):
    audio.play_sound_file(file_path="test")
    assert len(audio.sounds) == 1
    assert audio.sounds == ["test"]


def test_audio_play_same_file(audio):
    n = 10
    for _ in range(n):
        audio.play_sound_file(file_path="test")
    assert len(audio.sounds) == n
    assert audio.sounds == ["test" for _ in range(n)]


def test_audio_clear(audio):
    audio.play_sound_file(file_path="test")
    audio.clear()
    assert len(audio.sounds) == 0
