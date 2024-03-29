import copy
import unittest
import unittest.mock

import pypinball

MOC_SOUND_FILE_MAP = pypinball.GameConfig(
    ball_radius=15,
    playing_area=(450, 650),
    event_to_sounds={
        pypinball.events.GameEvents.BALL_LOST: "ball_lost",
        pypinball.events.GameEvents.COLLISION_BALL_BALL: "ball_ball_collision",
        pypinball.events.GameEvents.COLLISION_BALL_BUMPER: "ball_bumper_collision",
        pypinball.events.GameEvents.COLLISION_BALL_FLIPPER: "ball_flipper_collision",
        pypinball.events.GameEvents.COLLISION_BALL_WALL: "ball_wall_collision",
        pypinball.events.GameEvents.FLIPPER_ACTIVATED: "flipper_activate",
    },
)


class TestBallDropInEmptyScene(unittest.TestCase):
    """
    Test the condition where a ball is free-falling within an empty scene.
    """

    def setUp(self) -> None:
        self.audio = unittest.mock.MagicMock(spec=pypinball.AudioInterface)
        self.config = MOC_SOUND_FILE_MAP
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(
            event_pub=self.event_pub, fps=60.0
        )

        audio_event_handler = pypinball.audio.AudioGameEventHandler(
            interface=self.audio, events_to_sound=MOC_SOUND_FILE_MAP.event_to_sounds
        )
        self.event_pub.subscribe(callback=audio_event_handler.update)

        self.ball = pypinball.domain.Ball(uid=0, position=(20.0, 0.0))
        self.physics.add_ball(ball=self.ball)

        self.controller = pypinball.Controller(
            config=self.config,
            display_interface=unittest.mock.MagicMock(spec=pypinball.DisplayInterface),
            physics_interface=self.physics,
            event_publisher=self.event_pub,
        )

    def test_no_audio_played(self) -> None:
        """
        Test that a ball free-falling over a short distance produces no sound
        events.
        """
        for _ in range(5):
            self.controller.tick()
        self.audio.play_sound_file.assert_not_called()

    def test_ball_lost_sounds_played(self) -> None:
        """
        Test that the BALL_LOST sound is played once a ball falls beyond the
        playable area under gravity. The BALL_LOST sound should be the ONLY
        sound that is played.
        """
        for _ in range(500):
            self.controller.tick()
        self.audio.play_sound_file.assert_called_once()

    def test_lost_ball_is_removed_from_physics(self) -> None:
        """
        Test that the ball is removed from the PhysicsInterface once it falls
        outside the playing area.
        """
        for _ in range(500):
            self.controller.tick()

        res = self.physics.get_ball_states()
        self.assertListEqual([], res)

    def test_launch_ball_into_second_ball_plays_audio(self) -> None:
        """
        Test that a ball-ball collision sound is played when a second ball is
        added to the scene and launched at the first one.
        """
        ball = pypinball.domain.Ball(uid=10, position=(20.0, 250.0))
        self.physics.add_ball(ball=ball)
        self.physics.launch_ball(uid=ball.uid)

        for _ in range(10):
            self.controller.tick()

        self.audio.play_sound_file.assert_called()


class TestDropBallOnFlipper(unittest.TestCase):
    """
    Test the condition when a ball is dropped onto a flipper with no other
    objects within the scene.
    """

    def setUp(self) -> None:
        self.audio = unittest.mock.MagicMock(spec=pypinball.AudioInterface)
        self.config = MOC_SOUND_FILE_MAP
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(
            event_pub=self.event_pub, fps=60.0
        )

        audio_event_handler = pypinball.audio.AudioGameEventHandler(
            interface=self.audio, events_to_sound=MOC_SOUND_FILE_MAP.event_to_sounds
        )
        self.event_pub.subscribe(callback=audio_event_handler.update)

        self.ball = pypinball.domain.Ball(uid=0, position=(20.0, 0.0))
        self.flipper = pypinball.domain.Flipper(
            uid=1,
            config=pypinball.domain.FlipperConfig(
                position=(0.0, 100.0),
                angle=1.0,
                length=50.0,
                actuation_direction=1,
                actuation_angle=1.0,
                actuation_input=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
            ),
        )

        self.physics.add_ball(ball=self.ball)
        self.physics.add_flipper(flipper=self.flipper)

        self.controller = pypinball.Controller(
            config=self.config,
            display_interface=unittest.mock.MagicMock(spec=pypinball.DisplayInterface),
            physics_interface=self.physics,
            event_publisher=self.event_pub,
        )

    def test_audio_played_with_collision(self) -> None:
        """
        Test that no audio is played when a ball simply drops in the scene.
        """
        for _ in range(100):
            self.controller.tick()
        self.audio.play_sound_file.assert_called()


class TestDropBallOnWall(unittest.TestCase):
    """
    Test dropping the ball onto a Wall element.
    """

    def setUp(self) -> None:
        self.audio = unittest.mock.MagicMock(spec=pypinball.AudioInterface)
        self.config = MOC_SOUND_FILE_MAP
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(
            event_pub=self.event_pub, fps=60.0
        )

        audio_event_handler = pypinball.audio.AudioGameEventHandler(
            interface=self.audio, events_to_sound=MOC_SOUND_FILE_MAP.event_to_sounds
        )
        self.event_pub.subscribe(callback=audio_event_handler.update)

        self.ball = pypinball.domain.Ball(uid=0, position=(50, 50))
        self.physics.add_ball(ball=self.ball)
        self.physics.add_wall(
            wall=pypinball.domain.Wall(uid=1, points=[(25.0, 100.0), (75.0, 150.0)])
        )

        self.controller = pypinball.Controller(
            config=self.config,
            display_interface=unittest.mock.MagicMock(spec=pypinball.DisplayInterface),
            physics_interface=self.physics,
            event_publisher=self.event_pub,
        )

        self.controller.setup()

    def test_sound_on_collision(self) -> None:
        """
        Test that a sound is played when the ball is dropped onto the wall element.
        """
        for _ in range(100):
            self.controller.tick()
        self.audio.play_sound_file.assert_called()


class TestDropBallOnBumper(unittest.TestCase):
    """
    Test dropping the ball onto a Bumper.
    """

    def setUp(self) -> None:
        self.audio = unittest.mock.MagicMock(spec=pypinball.AudioInterface)
        self.config = MOC_SOUND_FILE_MAP
        self.event_pub = pypinball.events.GameEventPublisher()
        self.physics = pypinball.physics.PymunkPhysics(
            event_pub=self.event_pub, fps=60.0
        )

        audio_event_handler = pypinball.audio.AudioGameEventHandler(
            interface=self.audio, events_to_sound=MOC_SOUND_FILE_MAP.event_to_sounds
        )
        self.event_pub.subscribe(callback=audio_event_handler.update)

        self.ball = pypinball.domain.Ball(uid=0, position=(50, 50))
        self.physics.add_ball(ball=self.ball)
        self.physics.add_bumper(
            bumper=pypinball.domain.RoundBumper(uid=1, position=(60, 150), radius=10)
        )

        self.controller = pypinball.Controller(
            config=self.config,
            display_interface=unittest.mock.MagicMock(spec=pypinball.DisplayInterface),
            physics_interface=self.physics,
            event_publisher=self.event_pub,
        )

        self.controller.setup()

    def test_sound_on_collision(self) -> None:
        """
        Test that a sound is played when the ball is dropped onto the wall element.
        """
        for _ in range(100):
            self.controller.tick()
        self.audio.play_sound_file.assert_called()


class TestControllerSetup(unittest.TestCase):
    """
    Test the Controller.setup() method.
    """

    def setUp(self) -> None:
        class MocPhysics(pypinball.PhysicsInterface):
            def add_flipper(self, *args, **kwargs) -> bool:
                return False

            def add_wall(self, *args, **kwargs) -> bool:
                return False

        self.audio = unittest.mock.MagicMock(spec=pypinball.AudioInterface)
        self.config = pypinball.GameConfig(
            playing_area=(10, 10),
            walls=[pypinball.domain.Wall(uid=0, points=[(0.0, 0.0), (10, 10)])],
        )
        self.display = unittest.mock.MagicMock(spec=pypinball.DisplayInterface)
        self.physics = MocPhysics()
        self.events = pypinball.events.GameEventPublisher()

        self.controller = pypinball.Controller(
            display_interface=self.display,
            config=self.config,
            physics_interface=self.physics,
            event_publisher=self.events,
        )

    def test_setup_fails_when_adding_wall_and_flipper_fails(self) -> None:
        """
        Test that if the Physics Interface isn't able to create a wall or flipper
        then the Controller.setup() method returns ``False```.
        """
        res = self.controller.setup()
        self.assertFalse(res)


class TestLeftButtonPressed(unittest.TestCase):
    """
    Test the case where the left input button is pressed in a physics scene
    with only a flipper.
    """

    def setUp(self) -> None:
        flipper = pypinball.domain.Flipper(
            uid=1,
            config=pypinball.domain.FlipperConfig(
                position=(0.0, 100.0),
                angle=1.0,
                length=50.0,
                actuation_direction=1,
                actuation_angle=1.0,
                actuation_input=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
            ),
        )

        self.config = copy.deepcopy(MOC_SOUND_FILE_MAP)
        self.config.flippers.append(flipper)

        self.input_pub = pypinball.inputs.InputEventPublisher()
        self.event_pub = unittest.mock.MagicMock(
            wraps=pypinball.events.GameEventPublisher()
        )

        self.audio_interface = unittest.mock.MagicMock(spec=pypinball.AudioInterface)
        self.audio_event_handler = pypinball.audio.AudioGameEventHandler(
            interface=self.audio_interface, events_to_sound=self.config.event_to_sounds
        )

        self.event_pub.subscribe(callback=self.audio_event_handler.update)

        self.physics = pypinball.physics.PymunkPhysics(
            event_pub=self.event_pub, fps=60.0
        )

        self.controller = pypinball.Controller(
            config=self.config,
            display_interface=unittest.mock.MagicMock(spec=pypinball.DisplayInterface),
            event_publisher=self.event_pub,
            physics_interface=self.physics,
        )
        self.controller.setup()
        self.input_pub.subscribe(callback=self.controller.handle_input_event)
        self.input_pub.emit(event=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED)

        for _ in range(10):
            self.controller.tick()

    def test_audio_played_for_left_button(self) -> None:
        """Test that playing audio has been attempted."""
        self.audio_interface.play_sound_file.assert_called_once()

    def test_event_emitted(self) -> None:
        """Test that a GameEvent has been emitted"""
        self.event_pub.emit.assert_called_once()

    def test_flipper_actuated_event_emitted(self) -> None:
        """Test that the FLIPPER_ACTIVATED event has been emitted via the mock event handler."""
        self.event_pub.emit.assert_any_call(
            event=pypinball.events.GameEvents.FLIPPER_ACTIVATED
        )
