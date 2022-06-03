import pypinball
import unittest
from . import moc_interfaces


MOC_SOUND_FILE_MAP = pypinball.GameConfig(
    playing_area=(450, 650),
    sound_to_file_map={
        pypinball.Sounds.BALL_LOST: "ball_lost",
        pypinball.Sounds.COLLISION_BALL_FLIPPER: "ball_flipper_collision",
    },
)


class TestBallDropInEmptyScene(unittest.TestCase):
    """
    Test the condition where a ball is free-falling within an empty scene.
    """

    def setUp(self) -> None:
        self.audio = moc_interfaces.MocAudio()
        self.config = MOC_SOUND_FILE_MAP
        self.physics = pypinball.physics.PymunkPhysics()

        self.ball = pypinball.domain.Ball(uid=0, position=(20.0, 0.0))
        self.physics.add_ball(ball=self.ball)

        self.controller = pypinball.Controller(
            audio_interface=self.audio,
            config=self.config,
            display_interface=moc_interfaces.MocDisplayInterface(),
            input_interface=moc_interfaces.MocInputInterface(),
            physics_interface=self.physics,
        )

    def test_no_audio_played(self):
        """
        Test that a ball free-falling over a short distance produces no sound
        events.
        """
        for _ in range(5):
            self.controller.tick()

        exp = set()
        self.assertSetEqual(exp, self.audio.sounds)

    def test_ball_lost_sounds_played(self):
        """
        Test that the BALL_LOST sound is played once a ball falls beyond the
        playable area under gravity. The BALL_LOST sound should be the ONLY
        sound that is played.
        """
        for _ in range(500):
            self.controller.tick()

        exp = {"ball_lost"}
        self.assertSetEqual(exp, self.audio.sounds)

    def test_lost_ball_is_removed_from_physics(self):
        """
        Test that the ball is removed from the PhysicsInterface once it falls
        outside the playing area.
        """
        for _ in range(500):
            self.controller.tick()

        res = self.physics.get_ball_states()
        self.assertListEqual([], res)


class TestDropBallOnFlipper(unittest.TestCase):
    """
    Test the condition when a ball is dropped onto a flipper with no other
    objects within the scene.
    """

    def setUp(self) -> None:
        self.audio = moc_interfaces.MocAudio()
        self.config = MOC_SOUND_FILE_MAP
        self.physics = pypinball.physics.PymunkPhysics()

        self.ball = pypinball.domain.Ball(uid=0, position=(20.0, 0.0))
        self.flipper = pypinball.domain.Flipper(
            uid=1,
            config=pypinball.domain.FlipperConfig(
                position=(0.0, 100.0),
                angle=1.0,
                length=50.0,
                actuation_button=pypinball.domain.Buttons.LEFT,
                actuation_direction=1,
                actuation_angle=1.0,
            ),
        )

        self.physics.add_ball(ball=self.ball)
        self.physics.add_flipper(flipper=self.flipper)

        self.controller = pypinball.Controller(
            audio_interface=self.audio,
            config=self.config,
            display_interface=moc_interfaces.MocDisplayInterface(),
            input_interface=moc_interfaces.MocInputInterface(),
            physics_interface=self.physics,
        )

    def test_audio_played_with_collision(self):
        """
        Test that no audio is played when a ball simply drops in the scene.
        """
        for _ in range(100):
            self.controller.tick()
        self.assertTrue("ball_flipper_collision" in self.audio.sounds)


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

        self.audio = moc_interfaces.MocAudio()
        self.config = pypinball.GameConfig(
            playing_area=(10, 10),
            sound_to_file_map=dict(),
            walls=[pypinball.domain.Wall(uid=0, points=[(0.0, 0.0), (10, 10)])],
        )
        self.display = moc_interfaces.MocDisplayInterface()
        self.input = moc_interfaces.MocInputInterface()
        self.physics = MocPhysics()

        self.controller = pypinball.Controller(
            audio_interface=self.audio,
            display_interface=self.display,
            config=self.config,
            input_interface=self.input,
            physics_interface=self.physics,
        )

    def test_setup_fails_when_adding_wall_and_flipper_fails(self):
        """
        Test that if the Physics Interface isn't able to create a wall or flipper
        then the Controller.setup() method returns ``False```.
        """
        res = self.controller.setup()
        self.assertFalse(res)
