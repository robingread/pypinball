from .. import resources
from ..domain import Flipper, FlipperConfig, RectangleBumper, RoundBumper, Wall
from ..events import GameEvents
from ..inputs import InputEvents
from .game_config import DisplayConfig, GameConfig

DEFAULT_DISPLAY_CONFIG = DisplayConfig(
    background_image_path=resources.get_image_resource_path("background.png"),
    ball_image_path=resources.get_image_resource_path("ball.png"),
    round_bumper_image_path=resources.get_image_resource_path("round_bumper.png"),
    rectangle_bumper_image_path=resources.get_image_resource_path(
        "rectangle_bumper.png"
    ),
    flipper_image_path=resources.get_image_resource_path("flipper.png"),
    life_icon_path=resources.get_image_resource_path("heart_icon.png"),
)

DEFAULT_GAME_CONFIG = GameConfig(
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
