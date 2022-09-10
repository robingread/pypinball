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
        pypinball.Sounds.COLLISION_BALL_BUMPER: pypinball.resources.get_audio_resource_path(
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
    event_to_sounds={
        pypinball.events.GameEvents.BALL_LAUNCHED: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
    },
)

logger = logging.getLogger(name="pypinball")
logger.setLevel(level=logging.DEBUG)
logger.info("Starting game")

events_pub = pypinball.events.GameEventPublisher()

audio_interface = pypinball.audio.SimpleAudio()
audio_event_handler = pypinball.audio.AudioGameEventHandler(
    interface=audio_interface, events_to_sound=GAME_CONFIG.event_to_sounds
)
events_pub.subscribe(audio_event_handler.update)

display_interface = pypinball.display.PyGameDisplay(
    width=450, height=650, game_events=events_pub
)
input_interface = pypinball.inputs.KeyboardInput()

physics_interface = pypinball.physics.PymunkPhysics(event_pub=events_pub)
physics_interface.set_debug_display(screen=display_interface._screen)
physics_interface.add_bumper(
    bumper=pypinball.domain.RectangleBumper(
        uid=1000, position=(100, 100), size=(100, 25), angle=1
    )
)
physics_interface.add_bumper(
    bumper=pypinball.domain.RoundBumper(uid=1001, position=(200, 100), radius=15)
)
physics_interface.add_bumper(
    bumper=pypinball.domain.RoundBumper(uid=1002, position=(250, 250), radius=15)
)

controller = pypinball.Controller(
    audio_interface=audio_interface,
    config=GAME_CONFIG,
    display_interface=display_interface,
    input_interface=input_interface,
    physics_interface=physics_interface,
    event_publisher=events_pub,
)
controller.setup()
controller.run()

display_interface.close()
