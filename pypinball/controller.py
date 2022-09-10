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
        self._should_quit = True

    def run(self) -> None:
        logging.info("Starting main loop")
        while not self._should_quit:
            self.tick()

    def tick(self) -> None:
        logging.debug("Ticking controller")

        input_state = self._input.get_input_state()

        # Handle inputs to update Physics
        utils.actuate_flippers(
            input_state=input_state,
            flippers=self._config.flippers,
            physics=self._physics,
        )

        if input_state[domain.Buttons.CENTER]:
            uid = self._id_generator.generate_id()
            ball = domain.Ball(uid=uid, position=(400, 500))
            self._physics.add_ball(ball=ball)
            self._physics.launch_ball(uid=ball.uid)
            self._event_publisher.emit(event=events.GameEvents.BALL_LAUNCHED)

        self._display.clear()
        self._physics.update()
        self._display.update()

        # Handle audio
        sounds = list()
        sounds += utils.map_button_state_to_sound_type(
            input_state=input_state, sound_map=BUTTON_AUDIO_MAP
        )
        sounds += utils.map_collision_type_to_sound_type(
            collisions=self._physics.get_collisions(), sound_map=COLLISION_TO_AUDIO_MAP
        )
        self._handle_sounds(sounds=sounds)
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
