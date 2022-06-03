import logging
from . import audio
from . import domain
from . import display
from . import inputs
from . import physics
from . import utils
from .game_config import GameConfig


BUTTON_AUDIO_MAP = {
    domain.Buttons.CENTER: audio.Sounds.GAME_START,
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
    ):
        self._audio = audio_interface
        self._display = display_interface
        self._config = config
        self._input = input_interface
        self._physics = physics_interface
        self._id_generator = ObjectIdGenerator()

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
            utils.play_sounds(
                sounds=[audio.Sounds.BALL_LAUNCH],
                sounds_to_files=self._config.sound_to_file_map,
                audio=self._audio,
            )

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
        utils.play_sounds(
            sounds=sounds,
            sounds_to_files=self._config.sound_to_file_map,
            audio=self._audio,
        )
