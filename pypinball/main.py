import argparse

from .audio import AudioGameEventHandler, SimpleAudio
from .config import DEFAULT_DISPLAY_CONFIG, DEFAULT_GAME_CONFIG
from .controller import Controller
from .display import PyGameDisplay
from .events import GameEventPublisher
from .inputs import InputEventPublisher, KeyboardInput
from .log import DEBUG, set_global_log_level
from .physics import PymunkPhysics


def define_arguments(args=None) -> argparse.Namespace:
    """Define the top-level argument parser.

    Returns:
        argparse.Namespace: Populated argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    args = parser.parse_args(args)
    return args


def main(args=None) -> None:
    """Main entry point for the pypinball game"""

    args = define_arguments(args)

    if args.debug:
        set_global_log_level(level=DEBUG)

    audio_event_handler = AudioGameEventHandler(
        interface=SimpleAudio(),
        events_to_sound=DEFAULT_GAME_CONFIG.event_to_sounds,
    )

    events_pub = GameEventPublisher()
    events_pub.subscribe(audio_event_handler.update)

    display_interface = PyGameDisplay(
        width=int(DEFAULT_GAME_CONFIG.playing_area[0]),
        height=int(DEFAULT_GAME_CONFIG.playing_area[1]),
        game_events=events_pub,
        config=DEFAULT_DISPLAY_CONFIG,
        fps=DEFAULT_GAME_CONFIG.fames_per_second,
    )

    physics_interface = PymunkPhysics(
        event_pub=events_pub,
        fps=DEFAULT_GAME_CONFIG.fames_per_second,
    )
    # physics_interface.set_debug_display(screen=display_interface._screen)

    controller = Controller(
        config=DEFAULT_GAME_CONFIG,
        display_interface=display_interface,
        physics_interface=physics_interface,
        event_publisher=events_pub,
    )

    controller.setup()

    input_pub = InputEventPublisher()
    input_pub.subscribe(callback=controller.handle_input_event)
    input_interface = KeyboardInput(event_pub=input_pub)

    controller.run()

    display_interface.close()
