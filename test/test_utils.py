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

    def actuate_flipper(self, uid: int) -> bool:
        self.actuation_commands.append(uid)
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


class TestBallWithinAreaFunction(unittest.TestCase):
    """
    Test the utils.check_ball_is_within_area() method.
    """

    def setUp(self) -> None:
        self.width = 100
        self.height = 100

    def test_ball_within_area(self):
        """
        Test the condition where the ball is within the area.
        """
        position = (10, 10)
        self.assertTrue(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_above(self):
        """
        Test the condition where the ball is outside the area where the ball is
        above the playable area.
        """
        position = (10, -10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_below(self):
        """
        Test the condition where the ball is outside the area where the ball is
        below the playable area.
        """
        position = (10, self.height + 10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_left(self):
        """
        Test the condition where the ball is outside the area where the ball is
        to the left of the playable area.
        """
        position = (-10, 10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )

    def test_ball_outside_area_right(self):
        """
        Test the condition where the ball is outside the area where the ball is
        to the right of the playable area.
        """
        position = (self.width + 10, 10)
        self.assertFalse(
            pypinball.utils.check_ball_is_within_area(
                ball_position=position, width=self.width, height=self.height
            )
        )


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
                    angle=0.0,
                    length=0.1,
                    actuation_direction=1,
                    actuation_angle=1.0,
                    actuation_button=pypinball.domain.Buttons.LEFT,
                    actuation_input=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
                ),
            ),
            pypinball.domain.Flipper(
                uid=1,
                config=pypinball.domain.FlipperConfig(
                    position=(1, 1),
                    angle=0.0,
                    length=0.1,
                    actuation_direction=1,
                    actuation_angle=-1.0,
                    actuation_button=pypinball.domain.Buttons.RIGHT,
                    actuation_input=pypinball.inputs.InputEvents.RIGHT_BUTTON_PRESSED,
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
        exp = [flippers[0].uid]

        self.assertListEqual(res, exp)

    def test_actuate_right_flipper(self):
        input_state = self._get_input_state(left_button=False, right_button=True)
        flippers = self._get_flipper_config()
        pypinball.utils.actuate_flippers(
            input_state=input_state, flippers=flippers, physics=self.physics
        )

        res = self.physics.actuation_commands
        exp = [flippers[1].uid]

        self.assertListEqual(res, exp)

    def test_actuate_both_flippers(self):
        input_state = self._get_input_state(left_button=True, right_button=True)
        flippers = self._get_flipper_config()
        pypinball.utils.actuate_flippers(
            input_state=input_state, flippers=flippers, physics=self.physics
        )

        res = self.physics.actuation_commands
        exp = [flippers[0].uid, flippers[1].uid]

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
