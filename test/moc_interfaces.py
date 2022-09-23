import pypinball
import typing


# TODO: Remove the need/use of the MocAudio class.
class MocAudio(pypinball.AudioInterface):
    """
    Moc AudioInterface that stores the sounds which have been requested without
    actually playing any audio.
    """

    def __init__(self):
        self._sounds = list()

    @property
    def sounds(self) -> set:
        return set(self._sounds)

    def play_sound_file(self, file_path: str) -> bool:
        self._sounds.append(file_path)
        return True


class MocDisplayInterface(pypinball.DisplayInterface):
    def clear(self) -> None:
        pass

    def display_image(self, path: str) -> None:
        pass

    def update(self) -> None:
        pass


# TODO: Remove the need for the MocInputInterface class.
class MocInputInterface(pypinball.InputInterface):
    """
    Moc input interface which allows users to specify the input state that
    should be returned.
    """

    def __init__(self, center_button=False, left_button=False, right_button=False):
        self._center = center_button
        self._left = left_button
        self._right = right_button

    def get_input_state(self) -> typing.Dict[pypinball.domain.Buttons, bool]:
        return {
            pypinball.domain.Buttons.CENTER: self._center,
            pypinball.domain.Buttons.LEFT: self._left,
            pypinball.domain.Buttons.RIGHT: self._right,
        }

    def set_input_state(self, center=False, left=False, right=False) -> None:
        self._center = center
        self._left = left
        self._right = right
