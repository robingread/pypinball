import pypinball
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


class TestMocInput(unittest.TestCase):
    """
    Test the MocInputInterface class.
    """

    def test_default_init(self):
        """
        Test the state of the buttons after the default init method is called.
        """
        inputs = moc_interfaces.MocInputInterface()
        exp = {
            pypinball.Buttons.CENTER: False,
            pypinball.Buttons.LEFT: False,
            pypinball.Buttons.RIGHT: False,
        }
        res = inputs.get_input_state()
        self.assertDictEqual(exp, res)

    def test_set_buttons_state_via_init_method(self):
        """
        Test that the button state can be set via the init method.
        """
        inputs = moc_interfaces.MocInputInterface(
            center_button=True, left_button=False, right_button=False
        )
        exp = {
            pypinball.Buttons.CENTER: True,
            pypinball.Buttons.LEFT: False,
            pypinball.Buttons.RIGHT: False,
        }
        res = inputs.get_input_state()
        self.assertDictEqual(exp, res)

    def test_set_input_state(self):
        """
        Test that the set_input_state() method set the button states as
        expected.
        """
        inputs = moc_interfaces.MocInputInterface()
        inputs.set_input_state(center=True, left=True, right=True)
        exp = {
            pypinball.Buttons.CENTER: True,
            pypinball.Buttons.LEFT: True,
            pypinball.Buttons.RIGHT: True,
        }
        res = inputs.get_input_state()
        self.assertDictEqual(exp, res)
