from .audio import AudioGameEventHandler, SimpleAudio
from .config import DEFAULT_DISPLAY_CONFIG, DEFAULT_GAME_CONFIG
from .controller import Controller
from .display import PyGameDisplay
from .events import GameEventPublisher
from .inputs import InputEventPublisher, KeyboardInput
from .physics import PymunkPhysics


def main() -> None:
    """Main entry point for the pypinball game"""

    input_pub = InputEventPublisher()
    events_pub = GameEventPublisher()

    audio_event_handler = AudioGameEventHandler(
        interface=SimpleAudio(),
        events_to_sound=DEFAULT_GAME_CONFIG.event_to_sounds,
    )

    events_pub.subscribe(audio_event_handler.update)

    display_interface = PyGameDisplay(
        width=int(DEFAULT_GAME_CONFIG.playing_area[0]),
        height=int(DEFAULT_GAME_CONFIG.playing_area[1]),
        game_events=events_pub,
        config=DEFAULT_DISPLAY_CONFIG,
        fps=60.0,
    )

    input_interface = KeyboardInput(event_pub=input_pub)
    physics_interface = PymunkPhysics(event_pub=events_pub, fps=60.0)
    # physics_interface.set_debug_display(screen=display_interface._screen)

    controller = Controller(
        config=DEFAULT_GAME_CONFIG,
        display_interface=display_interface,
        physics_interface=physics_interface,
        event_publisher=events_pub,
    )

    controller.setup()

    input_pub.subscribe(callback=controller.handle_input_event)

    controller.run()

    display_interface.close()
