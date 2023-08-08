import unittest
import unittest.mock

import pypinball


class TestEventPublisherInit(unittest.TestCase):
    def setUp(self) -> None:
        self.callback = unittest.mock.MagicMock()
        self.publisher = pypinball.events.EventPublisher(
            event_type=pypinball.events.GameEvents
        )

    def test_num_subscribers(self):
        self.assertEqual(self.publisher.num_subscribers, 0)

    def test_emit_incorrect_type(self):
        with self.assertRaises(TypeError):
            self.publisher.emit(event="hello")

    def test_emit_event(self):
        self.assertEqual(
            self.publisher.emit(pypinball.events.GameEvents.GAME_STARTED), None
        )

    def test_subscribe_once(self):
        self.assertTrue(self.publisher.subscribe(self.callback))
        self.assertEqual(self.publisher.num_subscribers, 1)

    def test_subscribe_same_handler_twice(self):
        self.assertTrue(self.publisher.subscribe(self.callback))
        self.assertFalse(self.publisher.subscribe(self.callback))
        self.assertEqual(self.publisher.num_subscribers, 1)

    def test_unsubscribe(self):
        self.assertFalse(self.publisher.unsubscribe(self.callback))

    def test_unsubcribe_after_subscribe(self):
        self.publisher.subscribe(self.callback)
        self.assertTrue(self.publisher.unsubscribe(self.callback))
        self.assertEqual(self.publisher.num_subscribers, 0)

    def test_emit_event_after_subscription(self):
        event = pypinball.events.GameEvents.GAME_STARTED
        self.publisher.subscribe(self.callback)
        self.publisher.emit(event=event)
        self.callback.assert_called_once_with(event)
