import pypinball
import unittest


class EventTester:
    """
    Helper class to be used when testing the Event class. The single member
    ``callback`` is used to check whether the callback() method has
    actually been called.
    """

    def __init__(self):
        self.called = False

    def callback(self):
        self.called = True


class TestEvent(unittest.TestCase):
    """Test the Event class"""

    def setUp(self) -> None:
        self.event = pypinball.Event()
        self.handler = EventTester()

    def test_init_to_zero_handlers(self):
        """Test that there are no handlers upon initialisation."""
        self.assertEqual(self.event.num_handlers, 0)

    def test_add_handler(self):
        """Test adding a handler using the += syntax."""
        self.event += self.handler.callback
        self.assertEqual(self.event.num_handlers, 1)

    def test_add_second_handler(self):
        """Test adding a second handler method."""
        second_handler = EventTester()
        self.event += self.handler.callback
        self.event += second_handler.callback
        self.assertEqual(self.event.num_handlers, 2)

    def test_sub_handler(self):
        """Test removing a handler using the -= syntax."""
        self.event += self.handler.callback
        self.event -= self.handler.callback
        self.assertEqual(self.event.num_handlers, 0)

    def test_register_handler(self):
        """Test the register_handler() method."""
        self.event.register_handler(func=self.handler.callback)
        self.assertEqual(self.event.num_handlers, 1)

    def test_unregister_handler(self):
        """Test the unregister_handler() method."""
        self.event.register_handler(func=self.handler.callback)
        self.event.unregister_handler(func=self.handler.callback)
        self.assertEqual(self.event.num_handlers, 0)

    def test_emit_event(self):
        """Test emitting the event using the emit() method."""
        self.event.register_handler(self.handler.callback)
        self.event.emit()
        self.assertTrue(self.handler.called)

    def test_event_call(self):
        """Test emitting the event using the __call__() magic method."""
        self.event.register_handler(self.handler.callback)
        self.event()
        self.assertTrue(self.handler.called)

    def test_clear(self):
        """Test the event clear() method"""
        self.event.register_handler(func=self.handler.callback)
        self.event.clear()
        self.assertEqual(self.event.num_handlers, 0)
