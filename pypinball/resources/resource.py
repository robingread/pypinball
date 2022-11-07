import importlib.resources

from .. import log

logger = log.get_logger(name=__name__)


def get_python_pkg_resource_path(prefix: str, resource: str) -> str:
    """
    Get the full system path of a resource file within a python package. For
    example, loading a resource at ``some.pkg.module.audio.wav``.

    Args:
        prefix (str): Python module path in dot format (e.g. some.pkg.module).
        resource (str): Name of the resource within the Python module path (e.g. audio.wav).

    Returns:
        str: Full system path of a resource.

    Raises:
        ModuleNotFoundError: If the prefix does not exist.
        FileNotFoundError: If the resource file does not exist.
    """
    logger.debug(f"Loading resource path, prefix: {prefix}, resource: {resource}")
    with importlib.resources.path(package=prefix, resource=resource) as path:
        return str(path)


def get_audio_resource_path(filename: str) -> str:
    """
    Get the full system path for an audio resource stored within the pypinball
    package under the ``pypinball.resources.audio`` module.

    Args:
        filename (str): Name of the resource in the resources.audio module.

    Returns:
        str: Full system path of the resource.

    Raises:
        FileNotFoundError: If the resource filename doesn't exist.
    """
    prefix = "pypinball.resources.audio"
    return get_python_pkg_resource_path(prefix=prefix, resource=filename)
