from . import resources
from .audio import AudioGameEventHandler, SimpleAudio
from .controller import Controller
from .display import PyGameDisplay
from .domain import Flipper, FlipperConfig, RectangleBumper, RoundBumper, Wall
from .events import GameEventPublisher, GameEvents
from .game_config import DisplayConfig, GameConfig
from .inputs import InputEventPublisher, InputEvents, KeyboardInput
from .physics import PymunkPhysics

DISPLAY_CONFIG = DisplayConfig(
    background_image_path=resources.get_image_resource_path("background.png"),
    ball_image_path=resources.get_image_resource_path("ball.png"),
    round_bumper_image_path=resources.get_image_resource_path("round_bumper.png"),
    rectangle_bumper_image_path=resources.get_image_resource_path(
        "rectangle_bumper.png"
    ),
    flipper_image_path=resources.get_image_resource_path("flipper.png"),
)

GAME_CONFIG = GameConfig(
    playing_area=(450, 650),
    bumpers=[
        RectangleBumper(uid=1000, position=(100, 100), size=(100, 25), angle=1),
        RectangleBumper(uid=1001, position=(350, 150), size=(100, 25), angle=-1),
        RoundBumper(uid=1002, position=(200, 100), radius=15),
        RoundBumper(uid=1003, position=(220, 250), radius=15),
    ],
    flippers=[
        Flipper(
            uid=1,
            config=FlipperConfig(
                position=(50, 600),
                angle=0.0,
                length=140,
                actuation_angle=-1.0,
                actuation_direction=1,
                actuation_input=InputEvents.LEFT_BUTTON_PRESSED,
            ),
        ),
        Flipper(
            uid=2,
            config=FlipperConfig(
                position=(400, 600),
                angle=3.141,
                length=140,
                actuation_angle=1.0,
                actuation_direction=-1,
                actuation_input=InputEvents.RIGHT_BUTTON_PRESSED,
            ),
        ),
    ],
    walls=[
        Wall(
            uid=10,
            points=[
                (30.0, 560.0),
                (0.0, 50.0),
                (75.0, 0.0),
                (375.0, 0.0),
                (450.0, 50.0),
                (420.0, 560.0),
            ],
        ),
    ],
    event_to_sounds={
        GameEvents.FLIPPER_ACTIVATED: resources.get_audio_resource_path(
            filename="flipper_actuated.wav"
        ),
        GameEvents.BALL_LAUNCHED: resources.get_audio_resource_path(
            filename="ball_launch.wav"
        ),
        GameEvents.BALL_LOST: resources.get_audio_resource_path(
            filename="ball_lost.wav"
        ),
        GameEvents.COLLISION_BALL_BALL: resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        GameEvents.COLLISION_BALL_BUMPER: resources.get_audio_resource_path(
            filename="redPowerup3.wav"
        ),
        GameEvents.COLLISION_BALL_FLIPPER: resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        GameEvents.COLLISION_BALL_WALL: resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
    },
)


def main() -> None:
    """Main entry point for the pypinball game"""

    input_pub = InputEventPublisher()
    events_pub = GameEventPublisher()

    audio_event_handler = AudioGameEventHandler(
        interface=SimpleAudio(),
        events_to_sound=GAME_CONFIG.event_to_sounds,
    )

    events_pub.subscribe(audio_event_handler.update)

    display_interface = PyGameDisplay(
        width=int(GAME_CONFIG.playing_area[0]),
        height=int(GAME_CONFIG.playing_area[1]),
        game_events=events_pub,
        config=DISPLAY_CONFIG,
    )

    input_interface = KeyboardInput(event_pub=input_pub)
    physics_interface = PymunkPhysics(event_pub=events_pub)
    # physics_interface.set_debug_display(screen=display_interface._screen)

    controller = Controller(
        config=GAME_CONFIG,
        display_interface=display_interface,
        physics_interface=physics_interface,
        event_publisher=events_pub,
    )

    controller.setup()

    input_pub.subscribe(callback=controller.handle_input_event)

    controller.run()

    display_interface.close()
