import logging
import os
import sys

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")


def get_console_handler() -> logging.Handler:
    """
    Get a logging Handler for directing logs to the console.

    Returns:
        logging.Handler: Log handler.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(FORMATTER)
    return handler


def get_file_handler(filename: str) -> logging.Handler:
    """
    Get a logging Handler for directing logs to a file.

    Args:
        filename (str): Full path to file (e.g. /tmp/logs/some.log).

    Returns:
        logging.Handler: Log handler.
    """
    handler = logging.FileHandler(filename=filename)
    handler.setFormatter(FORMATTER)
    return handler


def make_log_file_path(filename: str) -> None:
    """
    Make a path for a log file.

    Args:
        filename (str): Path to log file (e.g. /tmp/logs/some.log).

    Returns:
        None
    """
    p = os.path.abspath(filename)
    p = os.path.splitext(p)[0]
    if not os.path.exists(p):
        os.makedirs(name=p)


def get_logger(
    name: str, filename: str = None, level: int = logging.INFO
) -> logging.Logger:
    """
    Get a logging.Logger instance.

    Args:
        name (str): Name for the logger.
        filename (str): Path to a file that logs will be written to. If set to ``None`` no file will be written.
        level (int): The ``logging`` level (e.g. DEBUG, INFO, etc).

    Returns:
        logging.Logger: Logger instance.
    """
    logger = logging.getLogger(name=name)
    logger.handlers.clear()
    logger.setLevel(level=level)
    logger.addHandler(get_console_handler())

    if filename is not None:
        make_log_file_path(filename=filename)
        logger.addHandler(get_file_handler(filename=filename))

    logger.propagate = False
    return logger
