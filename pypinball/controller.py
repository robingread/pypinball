import logging
import typing
from . import audio
from . import domain
from . import display
from . import events
from . import inputs
from . import physics
from . import utils
from .game_config import GameConfig


BUTTON_AUDIO_MAP = {
    domain.Buttons.CENTER: audio.Sounds.BALL_LAUNCH,
    domain.Buttons.LEFT: audio.Sounds.FLIPPER_ACTIVATE,
    domain.Buttons.RIGHT: audio.Sounds.FLIPPER_ACTIVATE,
}


COLLISION_TO_AUDIO_MAP = {
    domain.CollisionType.BALL_AND_BALL: audio.Sounds.COLLISION_BALL_BALL,
    domain.CollisionType.BALL_AND_BUMPER: audio.Sounds.COLLISION_BALL_BUMPER,
    domain.CollisionType.BALL_AND_FLIPPER: audio.Sounds.COLLISION_BALL_FLIPPER,
    domain.CollisionType.BALL_AND_WALL: audio.Sounds.COLLISION_BALL_WALL,
}


class ObjectIdGenerator:
    def __init__(self):
        self._count = -1

    def generate_id(self) -> int:
        self._count += 1
        return self._count


class Controller:
    def __init__(
        self,
        audio_interface: audio.AudioInterface,
        display_interface: display.DisplayInterface,
        config: GameConfig,
        input_interface: inputs.InputInterface,
        physics_interface: physics.PhysicsInterface,
        event_publisher: events.GameEventPublisher,
    ):
        self._audio = audio_interface
        self._display = display_interface
        self._config = config
        self._input = input_interface
        self._physics = physics_interface
        self._id_generator = ObjectIdGenerator()
        self._event_publisher = event_publisher

        self._should_quit = False

    def handle_input_event(self, event: inputs.InputEvents) -> None:
        if event in [
            inputs.InputEvents.LEFT_BUTTON_PRESSED,
            inputs.InputEvents.RIGHT_BUTTON_PRESSED,
        ]:
            # TODO: This should be a function that we can unit-test
            for flipper in self._config.flippers:
                if flipper.config.actuation_input != event:
                    continue
                self._physics.actuate_flipper(uid=flipper.uid)

        elif event == inputs.InputEvents.CENTER_BUTTON_PRESSED:
            # Launch a ball
            pass

    def setup(self) -> bool:
        """
        Setup the controller to prepare before running/ticking. This method
        will return ``False`` if there are any issues in the setup process.

        Returns:
            bool: Whether the setup was fully successful.
        """
        logging.debug("Setting up controller")

        self._should_quit = False
        ret = list()
        ret += [self._event_publisher.subscribe(callback=self._handle_game_events)]
        ret += [self._physics.add_flipper(f) for f in self._config.flippers]
        ret += [self._physics.add_wall(w) for w in self._config.walls]
        return all(ret)

    def stop(self) -> None:
        """
        Stop running the controller.

        Returns:
            None
        """
        logging.info("Stopping the controller main loop")
        self._should_quit = True

    def run(self) -> None:
        """
        Start running the controller main loop.

        Returns:
            None
        """
        logging.info("Starting main loop")
        while not self._should_quit:
            self.tick()

    def tick(self) -> None:
        logging.debug("Ticking controller")

        input_state = self._input.get_input_state()

        if input_state[domain.Buttons.CENTER]:
            uid = self._id_generator.generate_id()
            ball = domain.Ball(uid=uid, position=(400, 500))
            self._physics.add_ball(ball=ball)
            self._physics.launch_ball(uid=ball.uid)

        self._display.clear()
        self._physics.update()
        self._display.update()

        self._handle_lost_balls()

    def _handle_sounds(self, sounds: typing.List[audio.Sounds]) -> None:
        utils.play_sounds(
            sounds=sounds,
            sounds_to_files=self._config.sound_to_file_map,
            audio=self._audio,
        )

    def _handle_lost_balls(self) -> None:
        states = self._physics.get_ball_states()
        sounds = set()
        for state in states:
            ball_in_area = utils.check_ball_is_within_area(
                ball_position=state.position,
                width=self._config.playing_area[0],
                height=self._config.playing_area[1],
            )

            if ball_in_area:
                continue

            sounds.add(audio.Sounds.BALL_LOST)
            self._physics.remove_ball(uid=state.uid)

        self._handle_sounds(sounds=list(sounds))

    def _handle_game_events(self, event: events.GameEvents) -> None:
        if event in [events.GameEvents.QUIT]:
            self.stop()
