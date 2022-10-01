import logging
import os
import pypinball
import random
import unittest


class TestGetLoggerInit(unittest.TestCase):
    def setUp(self) -> None:
        self.name = "test_logger"
        self.log_level = random.choice([logging.DEBUG, logging.INFO, logging.WARN])
        self.logger = pypinball.log.get_logger(name=self.name, level=self.log_level)

    def test_num_handlers(self):
        self.assertEqual(len(self.logger.handlers), 1)

    def test_logger_name(self):
        self.assertEqual(self.logger.name, self.name)

    def test_logger_level(self):
        self.assertEqual(self.logger.level, self.log_level)


class TestLoggerInitWithFilePath(unittest.TestCase):
    def setUp(self) -> None:
        self.name = "test_logger"
        self.filepath = "/tmp/pypinball/test.log"
        self.log_level = random.choice([logging.DEBUG, logging.INFO, logging.WARN])
        self.logger = pypinball.log.get_logger(
            name=self.name, filename=self.filepath, level=logging.INFO
        )
        self.logger.info("Testing")

    def tearDown(self) -> None:
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.filepath))
