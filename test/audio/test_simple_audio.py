"""Test the SimpleAudio class in the simple_audio.py module."""

import unittest

import simpleaudio

import pypinball


class TestSimpleAudioInit(unittest.TestCase):
    """Test the state of the SimpleAudio class at init."""

    def setUp(self) -> None:
        self.audio = pypinball.audio.SimpleAudio(blocking=True)

    def test_no_cached_files(self) -> None:
        """Test that init there are no cached files."""
        exp = set()
        res = self.audio.cached_files()
        self.assertSetEqual(exp, res)


class TestLoadGetFromInternalCache(unittest.TestCase):
    """Test loading, caching and getting cached WAVE files."""

    def setUp(self) -> None:
        self.file = pypinball.resources.get_audio_resource_path("ball_lost.wav")
        self.audio = pypinball.audio.SimpleAudio(blocking=True)
        self.result = self.audio.get_wav_sound(file_path=self.file)

    def test_get_wav_sound_return_value(self) -> None:
        """Test that the return of the get_wav_sound() method is an instance
        of a simpleaudio.WaveObject"""
        self.assertIsInstance(self.result, simpleaudio.WaveObject)

    def test_get_wav_file(self) -> None:
        """Test that getting a wave file for the first time adds it to the cache"""
        exp = set([self.file])
        res = self.audio.cached_files()
        self.assertSetEqual(exp, res)

    def test_get_cached_wav_file_matches_original(self) -> None:
        """Test that getting the cached file returns the same object as the first get
        call."""
        result = self.audio.get_wav_sound(file_path=self.file)
        self.assertEqual(result, self.result)
