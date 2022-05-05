import unittest
import pypinball
import pypinball.audio
import pypinball.inputs
import pypinball.physics
import pypinball.utils


class MocAudioInterface(pypinball.audio.AudioInterface):
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

    def actuate_flipper(self, flipper: pypinball.domain.Flipper) -> bool:
        self.actuation_commands.append(flipper.config.actuation_button)
        return True


class TestInputToAudioMapping(unittest.TestCase):
    """
    Test the until methods for mapping input button states to Sound enums.
    """

    def setUp(self) -> None:
        self.audio = MocAudioInterface()

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


class TestHandleInputButtonAudio(unittest.TestCase):
    """
    Test the utils.handle_input_button_audio() method.
    """
    def setUp(self) -> None:
        self.audio = MocAudioInterface()

        self.input_state = {
            pypinball.domain.Buttons.RIGHT: True,
            pypinball.domain.Buttons.LEFT: False,
            pypinball.domain.Buttons.CENTER: False,
        }

        self.button_to_sounds = {
            pypinball.domain.Buttons.LEFT: pypinball.audio.Sounds.GAME_START,
            pypinball.domain.Buttons.RIGHT: pypinball.audio.Sounds.GAME_OVER,
        }

        self.sounds_to_file = {
            pypinball.audio.Sounds.GAME_START: pypinball.resources.get_audio_resource_path(
                filename="Bounce1.wav"
            ),
            pypinball.audio.Sounds.GAME_OVER: pypinball.resources.get_audio_resource_path(
                filename="Bounce4.wav"
            ),
        }

    def test_button_with_mapped_sound(self):
        input_state = {
            pypinball.domain.Buttons.RIGHT: True,
            pypinball.domain.Buttons.LEFT: False,
            pypinball.domain.Buttons.CENTER: False,
        }

        pypinball.utils.handle_input_button_audio(
            input_state=input_state,
            audio_interface=self.audio,
            button_to_sound_map=self.button_to_sounds,
            sound_to_file_map=self.sounds_to_file,
        )

        exp = [pypinball.resources.get_audio_resource_path(filename="Bounce4.wav")]
        self.assertListEqual(self.audio.commands, exp)

    def test_button_with_unmapped_sound(self):
        input_state = {
            pypinball.domain.Buttons.RIGHT: False,
            pypinball.domain.Buttons.LEFT: False,
            pypinball.domain.Buttons.CENTER: True,
        }

        pypinball.utils.handle_input_button_audio(
            input_state=input_state,
            audio_interface=self.audio,
            button_to_sound_map=self.button_to_sounds,
            sound_to_file_map=self.sounds_to_file,
        )

        exp = list()
        self.assertListEqual(self.audio.commands, exp)


class TestLaunchNewBall(unittest.TestCase):
    def setUp(self) -> None:
        self.physics = None

    def _get_input_state(self, center_button: bool) -> dict:
        return {
            pypinball.domain.Buttons.CENTER: center_button,
            pypinball.domain.Buttons.LEFT: False,
            pypinball.domain.Buttons.RIGHT: False,
        }

    def test_launch_with_extra_lives(self):
        input = self._get_input_state(True)
        lives = 1
        res = pypinball.utils.launch_new_ball(
            input_state=input, lives=lives, physics=self.physics
        )
        self.assertTrue(res)

    def test_launch_without_extra_lives(self):
        input = self._get_input_state(True)
        lives = 0
        res = pypinball.utils.launch_new_ball(
            input_state=input, lives=lives, physics=self.physics
        )
        self.assertFalse(res)

    def test_launch_without_enter_button(self):
        input = self._get_input_state(False)
        lives = 1
        res = pypinball.utils.launch_new_ball(
            input_state=input, lives=lives, physics=self.physics
        )
        self.assertFalse(res)


class TestActuateFlippers(unittest.TestCase):
    def setUp(self) -> None:
        self.physics = FakePhysicsInterface()

    def _get_flipper_config(self) -> list:
        ret = [
            pypinball.domain.Flipper(
                uid=0,
                config=pypinball.domain.FlipperConfig(
                    position=(0, 1),
                    rest_angle=0.0,
                    length=0.1,
                    actuation_direction=1,
                    actuation_angle=1.0,
                    actuation_button=pypinball.domain.Buttons.LEFT,
                ),
            ),
            pypinball.domain.Flipper(
                uid=1,
                config=pypinball.domain.FlipperConfig(
                    position=(1, 1),
                    rest_angle=0.0,
                    length=0.1,
                    actuation_direction=1,
                    actuation_angle=-1.0,
                    actuation_button=pypinball.domain.Buttons.RIGHT,
                ),
            ),
        ]
        return ret

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
        flippers = self._get_flipper_config()
        pypinball.utils.actuate_flippers(
            input_state=input_state, flippers=flippers, physics=self.physics
        )

        res = self.physics.actuation_commands
        exp = list()

        self.assertListEqual(res, exp)

    def test_actuate_left_flipper(self):
        input_state = self._get_input_state(left_button=True, right_button=False)
        flippers = self._get_flipper_config()
        pypinball.utils.actuate_flippers(
            input_state=input_state, flippers=flippers, physics=self.physics
        )

        res = self.physics.actuation_commands
        exp = [pypinball.domain.Buttons.LEFT]

        self.assertListEqual(res, exp)

    def test_actuate_right_flipper(self):
        input_state = self._get_input_state(left_button=False, right_button=True)
        flippers = self._get_flipper_config()
        pypinball.utils.actuate_flippers(
            input_state=input_state, flippers=flippers, physics=self.physics
        )

        res = self.physics.actuation_commands
        exp = [pypinball.domain.Buttons.RIGHT]

        self.assertListEqual(res, exp)

    def test_actuate_both_flippers(self):
        input_state = self._get_input_state(left_button=True, right_button=True)
        flippers = self._get_flipper_config()
        pypinball.utils.actuate_flippers(
            input_state=input_state, flippers=flippers, physics=self.physics
        )

        res = self.physics.actuation_commands
        exp = [pypinball.domain.Buttons.LEFT, pypinball.domain.Buttons.RIGHT]

        self.assertListEqual(res, exp)

    def test_actuate_with_center_button_pressed(self):
        input_state = self._get_input_state(center_button=True)
        flippers = self._get_flipper_config()
        pypinball.utils.actuate_flippers(
            input_state=input_state, flippers=flippers, physics=self.physics
        )

        res = self.physics.actuation_commands
        exp = list()

        self.assertListEqual(res, exp)
