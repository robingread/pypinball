"""Test module for the LoopedAudioPlayer class"""

import time
import unittest

import pypinball

TEST_AUDIO_FILE = pypinball.resources.get_audio_resource_path("ball_launch.wav")


class TestLoopedAudioPlayerInit(unittest.TestCase):
    """Test initialisation of the LoopedAudioPlayer class."""

    def setUp(self) -> None:
        self.filename = TEST_AUDIO_FILE
        self.audio = pypinball.audio.LoopedAudioPlayer(filename=self.filename)

    def test_get_filename(self) -> None:
        """Test that the get_filename() method returns a string that matches the string
        passed at initialisation"""
        self.assertEqual(
            self.filename, self.audio.get_filename(), msg="File names do not match"
        )

    def test_is_playing(self) -> None:
        """Test that the is_playing() method returns False at initialisation"""
        self.assertFalse(
            self.audio.is_playing(), msg="Audio reports playing as True at init"
        )


class TestEmptyFilenameAtInit(unittest.TestCase):
    """Test the initialisation of the LoopedAudioPlayer() class with some bad filename values"""

    def test_init_with_empty_string(self) -> None:
        """Test that initialisation with an empty string throws an FileNotFound exception"""
        with self.assertRaises(FileNotFoundError):
            pypinball.audio.LoopedAudioPlayer(filename="")

    def test_init_with_random_string(self) -> None:
        """Tets that initialisation with a random string (or file name) throws an FileNotFound exception"""
        with self.assertRaises(FileNotFoundError):
            pypinball.audio.LoopedAudioPlayer(filename="foobar")


class TestLoopedAudioPlaying(unittest.TestCase):
    """Test the play() and stop() methods for the LoopedAudioPlayer class."""

    def setUp(self) -> None:
        self.filename = TEST_AUDIO_FILE
        self.audio = pypinball.audio.LoopedAudioPlayer(filename=self.filename)

    def tearDown(self) -> None:
        time.sleep(0.2)
        self.audio.stop()

    def test_play(self) -> None:
        """Test that calling the play() method returns True"""
        self.assertTrue(self.audio.play(), msg="Played returned False")

    def test_play_twice(self) -> None:
        """Test that calling the play() method when audio is already playing returns ``False``"""
        self.audio.play()
        time.sleep(0.2)
        self.assertFalse(self.audio.play(), msg="Play method returned True")

    def test_stop(self) -> None:
        """Test that calling the stop() method while something is playing returns True"""
        self.audio.play()
        time.sleep(2.0)
        self.assertTrue(self.audio.stop(), msg="Calling stop() method returned False")

    def test_stop_without_play(self) -> None:
        """Test that calling the stop() method without calling play() returns False"""
        self.assertFalse(self.audio.stop(), msg="Stop method returned True")
