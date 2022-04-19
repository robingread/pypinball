import unittest
import pypinball
import pypinball.audio
import pypinball.inputs
import pypinball.utils


class FakeAudioInterface(pypinball.audio.AudioInterface):
    """
    Define a Fake Audio Interface for testing purposes.
    """

    def __init__(self):
        self.commands = list()

    def play_sound_file(self, file_path: str) -> bool:
        self.commands.append(file_path)
        return True


class TestInputToAudioMapping(unittest.TestCase):
    """
    Test the until methods for mapping input button states to Sound enums.
    """

    def setUp(self) -> None:
        self.audio = FakeAudioInterface()

    def test_fake_audio_interface_play_audio_file(self):
        """
        Test the FakeAudioInterface.
        """
        path = "/test/path.wav"
        self.audio.play_sound_file(file_path=path)
        self.assertListEqual(self.audio.commands, [path])

    def test_single_input_audio_mapping(self):
        """
        Test that a single input button pressed maps to one audio Sound type to be played.
        """
        input_state = {
            pypinball.domain.Buttons.LEFT: True,
            pypinball.domain.Buttons.RIGHT: False,
        }

        button_sound_map = {
            pypinball.domain.Buttons.LEFT: pypinball.audio.Sounds.FLIPPER_ACTIVATE,
            pypinball.domain.Buttons.RIGHT: pypinball.audio.Sounds.FLIPPER_ACTIVATE,
        }

        exp = [pypinball.audio.Sounds.FLIPPER_ACTIVATE]
        ret = pypinball.utils.map_button_state_to_sound_type(
            input_state=input_state, sound_map=button_sound_map
        )
        self.assertListEqual(ret, exp)

    def test_double_input_audio_mapping(self):
        """
        Test that two input buttons pressed maps to two audio Sound types to be played.
        """
        input_state = {
            pypinball.domain.Buttons.LEFT: True,
            pypinball.domain.Buttons.RIGHT: True,
        }

        button_sound_map = {
            pypinball.domain.Buttons.LEFT: pypinball.audio.Sounds.FLIPPER_ACTIVATE,
            pypinball.domain.Buttons.RIGHT: pypinball.audio.Sounds.FLIPPER_ACTIVATE,
        }

        exp = [pypinball.audio.Sounds.FLIPPER_ACTIVATE] * 2
        ret = pypinball.utils.map_button_state_to_sound_type(
            input_state=input_state, sound_map=button_sound_map
        )
        self.assertListEqual(ret, exp)
