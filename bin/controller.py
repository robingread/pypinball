#!/usr/bin/env python

import pypinball

DISPLAY_CONFIG = pypinball.game_config.DisplayConfig(
    background_image_path=pypinball.resources.get_image_resource_path("background.png"),
    ball_image_path=pypinball.resources.get_image_resource_path("ball.png"),
    round_bumper_image_path=pypinball.resources.get_image_resource_path(
        "round_bumper.png"
    ),
    rectangle_bumper_image_path=pypinball.resources.get_image_resource_path(
        "rectangle_bumper.png"
    ),
    flipper_image_path=pypinball.resources.get_image_resource_path("flipper.png"),
)

GAME_CONFIG = pypinball.GameConfig(
    playing_area=(450, 650),
    bumpers=[
        pypinball.domain.RectangleBumper(
            uid=1000, position=(100, 100), size=(100, 25), angle=1
        ),
        pypinball.domain.RectangleBumper(
            uid=1001, position=(350, 150), size=(100, 25), angle=-1
        ),
        pypinball.domain.RoundBumper(uid=1002, position=(200, 100), radius=15),
        pypinball.domain.RoundBumper(uid=1003, position=(220, 250), radius=15),
    ],
    flippers=[
        pypinball.domain.Flipper(
            uid=1,
            config=pypinball.domain.FlipperConfig(
                position=(50, 600),
                angle=0.0,
                length=140,
                actuation_angle=-1.0,
                actuation_direction=1,
                actuation_input=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
            ),
        ),
        pypinball.domain.Flipper(
            uid=2,
            config=pypinball.domain.FlipperConfig(
                position=(400, 600),
                angle=3.141,
                length=140,
                actuation_angle=1.0,
                actuation_direction=-1,
                actuation_input=pypinball.inputs.InputEvents.RIGHT_BUTTON_PRESSED,
            ),
        ),
    ],
    walls=[
        pypinball.domain.Wall(
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
        pypinball.events.GameEvents.FLIPPER_ACTIVATED: pypinball.resources.get_audio_resource_path(
            filename="flipper_actuated.wav"
        ),
        pypinball.events.GameEvents.BALL_LAUNCHED: pypinball.resources.get_audio_resource_path(
            filename="ball_launch.wav"
        ),
        pypinball.events.GameEvents.BALL_LOST: pypinball.resources.get_audio_resource_path(
            filename="ball_lost.wav"
        ),
        pypinball.events.GameEvents.COLLISION_BALL_BALL: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.events.GameEvents.COLLISION_BALL_BUMPER: pypinball.resources.get_audio_resource_path(
            filename="redPowerup3.wav"
        ),
        pypinball.events.GameEvents.COLLISION_BALL_FLIPPER: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.events.GameEvents.COLLISION_BALL_WALL: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
    },
)

input_pub = pypinball.inputs.InputEventPublisher()
events_pub = pypinball.events.GameEventPublisher()

audio_event_handler = pypinball.audio.AudioGameEventHandler(
    interface=pypinball.audio.SimpleAudio(),
    events_to_sound=GAME_CONFIG.event_to_sounds,
)

events_pub.subscribe(audio_event_handler.update)

display_interface = pypinball.display.PyGameDisplay(
    width=int(GAME_CONFIG.playing_area[0]),
    height=int(GAME_CONFIG.playing_area[1]),
    game_events=events_pub,
    config=DISPLAY_CONFIG,
)

input_interface = pypinball.inputs.KeyboardInput(event_pub=input_pub)
physics_interface = pypinball.physics.PymunkPhysics(event_pub=events_pub)
physics_interface.set_debug_display(screen=display_interface._screen)

controller = pypinball.Controller(
    config=GAME_CONFIG,
    display_interface=display_interface,
    physics_interface=physics_interface,
    event_publisher=events_pub,
)

controller.setup()

input_pub.subscribe(callback=controller.handle_input_event)

controller.run()

display_interface.close()
