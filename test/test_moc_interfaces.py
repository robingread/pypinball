import unittest
from . import moc_interfaces


class TestMocAudio(unittest.TestCase):
    """
    Test the MocAudio class.
    """

    def test_get_sounds(self):
        """
        Test the sounds property in the ``MocAudio`` class.
        """
        audio = moc_interfaces.MocAudio()
        audio.play_sound_file(file_path="/path1")
        audio.play_sound_file(file_path="/path2")

        exp = {"/path1", "/path2"}
        self.assertSetEqual(exp, audio.sounds)
