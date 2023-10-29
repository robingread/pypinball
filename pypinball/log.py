import logging
import os
import sys
import typing

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


class CustomFormatter(logging.Formatter):
    """
    Custom logging.Formatter class that provides colouing to the different log levels.
    """

    GRAY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    FORMAT = (
        "[%(asctime)s][%(name)s][%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: GRAY + FORMAT + RESET,
        logging.INFO: GRAY + FORMAT + RESET,
        logging.WARNING: YELLOW + FORMAT + RESET,
        logging.ERROR: RED + FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


FORMATTER = CustomFormatter()


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
    """
    path = os.path.split(os.path.abspath(filename))[0]
    if not os.path.exists(path):
        os.makedirs(name=path)


def get_logger(
    name: str, filename: typing.Optional[str] = None, level: int = logging.INFO
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
