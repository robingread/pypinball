import unittest
import pypinball
import pypinball.audio
import pypinball.inputs
import pypinball.physics
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


class FakePhysicsInterface(pypinball.physics.PhysicsInterface):
    def __init__(self):
        self.actuation_commands = list()

    def actuate_flippers(self, actuate_button: pypinball.domain.Buttons) -> None:
        self.actuation_commands.append(actuate_button)


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


class TestActuateFlippers(unittest.TestCase):
    def setUp(self) -> None:
        self.physics = FakePhysicsInterface()

    def _get_input_state(
        self, center_button=False, left_button=False, right_button=False
    ) -> dict:
        return {
            pypinball.domain.Buttons.CENTER: center_button,
            pypinball.domain.Buttons.LEFT: left_button,
            pypinball.domain.Buttons.RIGHT: right_button,
        }

    def test_actuate_flipper_no_buttons(self):
        input_state = self._get_input_state(left_button=False, right_button=False)
        pypinball.utils.actuate_flippers(input_state, self.physics)

        res = self.physics.actuation_commands
        exp = list()

        self.assertListEqual(res, exp)

    def test_actuate_left_flipper(self):
        input_state = self._get_input_state(left_button=True, right_button=False)
        pypinball.utils.actuate_flippers(input_state, self.physics)

        res = self.physics.actuation_commands
        exp = [pypinball.domain.Buttons.LEFT]

        self.assertListEqual(res, exp)

    def test_actuate_right_flipper(self):
        input_state = self._get_input_state(left_button=False, right_button=True)
        pypinball.utils.actuate_flippers(input_state, self.physics)

        res = self.physics.actuation_commands
        exp = [pypinball.domain.Buttons.RIGHT]

        self.assertListEqual(res, exp)

    def test_actuate_both_flippers(self):
        input_state = self._get_input_state(left_button=True, right_button=True)
        pypinball.utils.actuate_flippers(input_state, self.physics)

        res = self.physics.actuation_commands
        exp = [pypinball.domain.Buttons.LEFT, pypinball.domain.Buttons.RIGHT]

        self.assertListEqual(res, exp)

    def test_actuate_with_center_button_pressed(self):
        input_state = self._get_input_state(center_button=True)
        pypinball.utils.actuate_flippers(input_state, self.physics)

        res = self.physics.actuation_commands
        exp = list()

        self.assertListEqual(res, exp)
