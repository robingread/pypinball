import logging
import pypinball

GAME_CONFIG = pypinball.GameConfig(
    playing_area=(600, 650),
    flippers=[
        pypinball.domain.Flipper(
            uid=1,
            config=pypinball.domain.FlipperConfig(
                position=(50, 600),
                angle=0.0,
                length=25,
                actuation_angle=-1.0,
                actuation_button=pypinball.Buttons.LEFT,
                actuation_direction=1,
            ),
        ),
        pypinball.domain.Flipper(
            uid=2,
            config=pypinball.domain.FlipperConfig(
                position=(400, 600),
                angle=3.141,
                length=25,
                actuation_angle=1.0,
                actuation_button=pypinball.Buttons.RIGHT,
                actuation_direction=-1,
            ),
        ),
        pypinball.domain.Flipper(
            uid=3,
            config=pypinball.domain.FlipperConfig(
                position=(400, 400),
                angle=3.141,
                length=25,
                actuation_angle=1.0,
                actuation_button=pypinball.Buttons.RIGHT,
                actuation_direction=-1,
            ),
        ),
    ],
    walls=[
        pypinball.domain.Wall(
            uid=0,
            points=[(0.0, 0.0), (450.0, 0.0), (450.0, 650.0), (0.0, 650.0), (0.0, 0.0)],
        )
    ],
    sound_to_file_map={
        pypinball.Sounds.COLLISION_BALL_BALL: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.Sounds.COLLISION_BALL_FLIPPER: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.Sounds.COLLISION_BALL_WALL: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.Sounds.FLIPPER_ACTIVATE: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.Sounds.BALL_LAUNCH: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
    },
)

logger = logging.getLogger(name="pypinball")
logger.setLevel(level=logging.DEBUG)
logger.info("Starting game")

audio_interface = pypinball.audio.SimpleAudio()
display_interface = pypinball.display.PyGameDisplay(width=450, height=650)
input_interface = pypinball.inputs.KeyboardInput()

physics_interface = pypinball.physics.PymunkPhysics()
physics_interface.set_debug_display(screen=display_interface._screen)

controller = pypinball.Controller(
    audio_interface=audio_interface,
    config=GAME_CONFIG,
    display_interface=display_interface,
    input_interface=input_interface,
    physics_interface=physics_interface,
)

controller.setup()

logging.info("Starting main loop")
for _ in range(10000):
    controller.tick()
