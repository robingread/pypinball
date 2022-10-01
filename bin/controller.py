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
                actuation_direction=1,
                actuation_input=pypinball.inputs.InputEvents.LEFT_BUTTON_PRESSED,
            ),
        ),
        pypinball.domain.Flipper(
            uid=2,
            config=pypinball.domain.FlipperConfig(
                position=(400, 600),
                angle=3.141,
                length=25,
                actuation_angle=1.0,
                actuation_direction=-1,
                actuation_input=pypinball.inputs.InputEvents.RIGHT_BUTTON_PRESSED,
            ),
        ),
    ],
    walls=[
        pypinball.domain.Wall(
            uid=10,
            points=[(0.0, 650.0), (0.0, 0.0), (450.0, 0.0), (450.0, 650.0)],
        ),
    ],
    event_to_sounds={
        pypinball.events.GameEvents.FLIPPER_ACTIVATED: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.events.GameEvents.BALL_LAUNCHED: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.events.GameEvents.COLLISION_BALL_BALL: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
        ),
        pypinball.events.GameEvents.COLLISION_BALL_BUMPER: pypinball.resources.get_audio_resource_path(
            filename="Bounce4.wav"
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

audio_interface = pypinball.audio.SimpleAudio()
audio_event_handler = pypinball.audio.AudioGameEventHandler(
    interface=audio_interface, events_to_sound=GAME_CONFIG.event_to_sounds
)
events_pub.subscribe(audio_event_handler.update)

display_interface = pypinball.display.PyGameDisplay(
    width=450, height=650, game_events=events_pub
)
input_interface = pypinball.inputs.KeyboardInput(event_pub=input_pub)

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
    config=GAME_CONFIG,
    display_interface=display_interface,
    physics_interface=physics_interface,
    event_publisher=events_pub,
)
controller.setup()

input_pub.subscribe(callback=controller.handle_input_event)

controller.run()

display_interface.close()
