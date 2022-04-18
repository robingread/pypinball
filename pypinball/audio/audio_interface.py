import typing


class AudioInterface(typing.Protocol):
    """
    Audio Interface protocol definition. This is an interface class and does not implement any actual behaviour.
    Concrete implementations of audio interfaces should either inherit from this class or implement the same
    methods.
    """

    def play_sound_file(self, file_path: str) -> bool:
        """
        Play a sound file.
        Args:
            file_path (str): Full system path to the audio file.

        Returns:
            bool: Whether the sound was played successfully.
        """
        ...
