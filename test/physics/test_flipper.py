import math
import unittest

import pypinball


class AngleTracker:
    def __init__(self, reference: float):
        self._reference = reference
        self._max_angle_diff = 0.0
        self._absolute_angle = 0.0

    @property
    def absolute_angle(self) -> float:
        return self._absolute_angle

    def update(self, angle: float) -> None:
        diff = angle - self._reference
        if math.fabs(diff) > self._max_angle_diff:
            self._absolute_angle = angle
            self._max_angle_diff = math.fabs(diff)


class TestAngleTracker(unittest.TestCase):
    def test_tracker_positive_angles(self):
        tracker = AngleTracker(reference=0.0)
        tracker.update(angle=0.0)
        tracker.update(angle=1.0)
        tracker.update(angle=0.5)
        self.assertEqual(tracker.absolute_angle, 1.0)

    def test_tracker_negative_angles(self):
        tracker = AngleTracker(reference=0.0)
        tracker.update(angle=0.0)
        tracker.update(angle=-1.0)
        tracker.update(angle=-0.5)
        self.assertEqual(tracker.absolute_angle, -1.0)

    def test_pi_reference(self):
        tracker = AngleTracker(reference=3.0)
        tracker.update(angle=3.1)
        tracker.update(angle=2.1)
        tracker.update(angle=0.0)
        self.assertEqual(tracker.absolute_angle, 0.0)


class TestPymunkFlipper(unittest.TestCase):
    def setUp(self):
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(event_pub=self.event_pub)

        self.left_flipper = pypinball.domain.Flipper(
            uid=0,
            config=pypinball.domain.FlipperConfig(
                position=(50, 400),
                angle=0,
                length=150,
                actuation_angle=-1.0,
                actuation_direction=1,
                actuation_input=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
            ),
        )

        self.right_flipper = pypinball.domain.Flipper(
            uid=1,
            config=pypinball.domain.FlipperConfig(
                position=(350, 400),
                angle=math.pi,
                length=50,
                actuation_angle=1.0,
                actuation_direction=-1,
                actuation_input=pypinball.inputs.InputEvents.RIGHT_BUTTON_PRESSED,
            ),
        )

    def test_add_flipper(self):
        """
        Test that adding a flipper works and the add_flipper() method returns ``True``.
        """
        ret = self.physics.add_flipper(flipper=self.left_flipper)
        self.assertTrue(ret)

    def test_add_flipper_twice(self):
        """
        Test that adding a flipper with the same ID twice does not work.
        """
        ret = self.physics.add_flipper(flipper=self.left_flipper)
        self.assertTrue(ret)

        ret = self.physics.add_flipper(flipper=self.left_flipper)
        self.assertFalse(ret)

    def test_get_flipper_state_after_adding(self):
        self.physics.add_flipper(flipper=self.left_flipper)
        state = self.physics.get_flipper_state(uid=self.left_flipper.uid)

        self.assertIsInstance(state, pypinball.domain.FlipperState)
        self.assertEqual(self.left_flipper.config.angle, state.angle)
        self.assertEqual(self.left_flipper.config.position, state.position)

    def test_get_state_of_flipper_with_unknown_id(self):
        with self.assertRaises(KeyError):
            self.physics.get_flipper_state(uid=100)

    def test_actuate_left_flipper(self):
        """
        Test that actuating a flipper changes the angle in the desired direction.
        """
        self.physics.add_flipper(flipper=self.left_flipper)
        self.physics.actuate_flipper(uid=self.left_flipper.uid)

        tracker = AngleTracker(reference=self.left_flipper.config.angle)
        for _ in range(100):
            self.physics.update()
            state = self.physics.get_flipper_state(uid=self.left_flipper.uid)
            tracker.update(angle=state.angle)

        target_angle = (
            self.left_flipper.config.angle + self.left_flipper.config.actuation_angle
        )
        self.assertAlmostEqual(
            tracker.absolute_angle,
            target_angle,
            delta=0.1,
            msg="Actual angle of left flipper is not equal to target configuation angle",
        )

    def test_actuate_right_flipper(self):
        """
        Test that actuating a flipper changes the angle in the desired direction.
        """
        self.physics.add_flipper(flipper=self.right_flipper)
        self.physics.actuate_flipper(uid=self.right_flipper.uid)

        tracker = AngleTracker(reference=self.right_flipper.config.angle)
        for _ in range(100):
            self.physics.update()
            state = self.physics.get_flipper_state(uid=self.right_flipper.uid)
            tracker.update(angle=state.angle)

        target_angle = (
            self.right_flipper.config.angle + self.right_flipper.config.actuation_angle
        )
        self.assertAlmostEqual(tracker.absolute_angle, target_angle, delta=0.1)

    def test_actuate_unregistered_flipper(self):
        """
        Test that actuating a flipper that hasn't been added to the Physics
        environment doesn't do anything.
        """
        ret = self.physics.actuate_flipper(uid=self.right_flipper.uid)
        self.assertFalse(ret)

    def test_actuate_flipper_emits_event(self):
        """
        Test that the actuate_flipper() method also emits a FLIPPER_ACTIVATED
        event via he GameEventPublisher.
        """
        event_handler = pypinball.events.MockEventHandler()
        self.event_pub.subscribe(callback=event_handler.handle_event)

        self.physics.add_flipper(flipper=self.right_flipper)
        self.physics.actuate_flipper(uid=self.right_flipper.uid)

        for _ in range(100):
            self.physics.update()

        self.assertListEqual(
            event_handler.events, [pypinball.events.GameEvents.FLIPPER_ACTIVATED]
        )

    def test_actuate_unregistered_flipper_does_not_emit_event(self):
        """
        Test that actuating a flipper that doesn't exist also doesn't emit a
        FLIPPER_ACTIVATED game event.
        """
        event_handler = pypinball.events.MockEventHandler()
        self.event_pub.subscribe(callback=event_handler.handle_event)

        self.physics.actuate_flipper(uid=self.right_flipper.uid)
        self.assertListEqual(event_handler.events, [])
