from os import path

import pytest

import pypinball


def test_load_from_unknwon_prefix() -> None:
    """
    Test that loading a resource from an non-existing package throws an exception.
    """
    prefix = "some.random.prefix"
    resource = "ball.png"
    with pytest.raises(ModuleNotFoundError):
        pypinball.resources.get_python_pkg_resource_path(
            prefix=prefix, resource=resource
        )


def test_load_from_unknown_resource() -> None:
    """
    Test that loading a non-existing resource from an existing package throws an exception.
    """
    prefix = "pypinball.resources.audio"
    resource = "foo.wav"
    with pytest.raises(FileNotFoundError):
        pypinball.resources.get_python_pkg_resource_path(
            prefix=prefix, resource=resource
        )


def test_get_audio_resource_path_bad_path() -> None:
    """
    Test that loading an audio which does't exist throws an exception.
    """
    filename = "foo.wav"
    with pytest.raises(FileNotFoundError):
        pypinball.resources.get_audio_resource_path(filename=filename)


def test_get_audio_resource_path_good_path() -> None:
    """
    Test that loading an existing audio file works.
    """
    filename = "Bounce1.wav"
    filepath = pypinball.resources.get_audio_resource_path(filename=filename)
    assert path.exists(filepath)


def test_get_image_resource_path_bad_path() -> None:
    """
    Test that loading an image which does't exist throws an exception.
    """
    filename = "foo.png"
    with pytest.raises(FileNotFoundError):
        pypinball.resources.get_image_resource_path(filename=filename)


def test_get_image_resource_path_good_path() -> None:
    """
    Test that loading an existing image file works.
    """
    filename = "ball.png"
    filepath = pypinball.resources.get_image_resource_path(filename=filename)
    assert path.exists(filepath)
