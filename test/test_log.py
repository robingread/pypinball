import logging
import os
import random
import shutil
import unittest

import pypinball


class TestGetLoggerInit(unittest.TestCase):
    """Test initialising a new logger."""

    def setUp(self) -> None:
        self.name = "test_logger"
        self.log_level = random.choice([logging.DEBUG, logging.INFO, logging.WARN])
        self.logger = pypinball.log.get_logger(name=self.name, level=self.log_level)

    def test_num_handlers(self) -> None:
        """Test that the logger has a single handler"""
        self.assertEqual(len(self.logger.handlers), 1)

    def test_logger_name(self) -> None:
        """Test that the logger has the expected name."""
        self.assertEqual(self.logger.name, self.name)

    def test_logger_level(self) -> None:
        """Test that the logger has the expeted level."""
        self.assertEqual(self.logger.level, self.log_level)


class TestLoggerInitWithFilePath(unittest.TestCase):
    """Test create a logger which also has a specified filename/path."""

    def setUp(self) -> None:
        self.name = "test_logger"
        self.logdir = "/tmp/pypinball/logging"
        self.filepath = os.path.join(self.logdir, "test.log")
        self.log_level = random.choice([logging.DEBUG, logging.INFO, logging.WARN])
        self.logger = pypinball.log.get_logger(
            name=self.name, filename=self.filepath, level=logging.INFO
        )
        self.logger.critical("Testing...")

    def tearDown(self) -> None:
        shutil.rmtree(self.logdir)

    def test_file_exists(self) -> None:
        """Test that the log file exists."""
        self.assertTrue(os.path.exists(self.filepath))

    def test_num_handlers(self) -> None:
        """Test that the logger has a two handler"""
        self.assertEqual(len(self.logger.handlers), 2)

    def test_logging_writes_to_file(self) -> None:
        """Test that writing a critial message also writes to the file."""
        with open(self.filepath, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 1)


class TestSetGlobalLogLevel(unittest.TestCase):
    """Test the set_global_log_level() method."""

    def setUp(self) -> None:
        self._logger_1 = pypinball.log.get_logger(
            name="logger1", level=pypinball.log.INFO
        )

        self._logger_2 = pypinball.log.get_logger(
            name="logger2", level=pypinball.log.INFO
        )

        pypinball.log.set_global_log_level(level=pypinball.log.DEBUG)

    def test_logger_1_log_level(self) -> None:
        """Test that the level of logger 1 has been set to DEBUG"""
        self.assertEqual(pypinball.log.DEBUG, self._logger_1.level)

    def test_logger_2_log_level(self) -> None:
        """Test that the level of logger 2 has been set to DEBUG"""
        self.assertEqual(pypinball.log.DEBUG, self._logger_2.level)
