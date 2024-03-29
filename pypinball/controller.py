from . import display, events, inputs, log, physics, utils
from .config import GameConfig
from .lives import Lives
from .scoring import Scoring

logger = log.get_logger(__name__)


class Controller:
    """Controller class"""

    def __init__(
        self,
        display_interface: display.DisplayInterface,
        config: GameConfig,
        physics_interface: physics.PhysicsInterface,
        event_publisher: events.GameEventPublisher,
    ) -> None:
        self._display = display_interface
        self._config = config
        self._physics = physics_interface
        self._id_generator = utils.ObjectIdGenerator()
        self._event_publisher = event_publisher

        self._scoring = Scoring()
        self._lives = Lives(lives=5, event_pub=self._event_publisher)

        self._should_quit = False

    ##################
    # Public Methods #
    ##################
    def handle_input_event(self, event: inputs.InputEvents) -> None:
        """
        Input device event handler class. This method is used to react to input
        events and should be registered as a callback with a ``InputEventPublisher`` instance.

        Args:
            event (InputEvents): Input device event.
        """
        logger.debug(f"Handling input event: {event}")

        if event in [
            inputs.InputEvents.LEFT_BUTTON_PRESSED,
            inputs.InputEvents.RIGHT_BUTTON_PRESSED,
        ]:
            # TODO: This should be a function that we can unit-test
            for flipper in self._config.flippers:
                if flipper.config.actuation_input != event:
                    continue
                self._physics.actuate_flipper(uid=flipper.uid)

        elif event == inputs.InputEvents.CENTER_BUTTON_PRESSED:
            utils.handle_center_button_press(
                physics=self._physics,
                config=self._config,
                id_gen=self._id_generator,
            )

    def setup(self) -> bool:
        """
        Setup the controller to prepare before running/ticking. This method
        will return ``False`` if there are any issues in the setup process.

        Returns:
            bool: Whether the setup was fully successful.
        """
        logger.debug("Setting up controller")

        self._should_quit = False
        ret = list()
        ret += [self._event_publisher.subscribe(callback=self._handle_game_events)]
        ret += [self._physics.add_bumper(f) for f in self._config.bumpers]
        ret += [self._physics.add_flipper(f) for f in self._config.flippers]
        ret += [self._physics.add_wall(w) for w in self._config.walls]

        self._event_publisher.subscribe(callback=self._scoring.event_callback)
        self._event_publisher.subscribe(callback=self._lives.event_callback)
        return all(ret)

    def stop(self) -> None:
        """
        Stop running the controller.
        """
        logger.info("Stopping the controller main loop")
        self._should_quit = True

    def run(self) -> None:
        """
        Start running the controller main loop. This calls the ``tick()`` method in the background.
        """
        logger.info("Starting main loop")
        while not self._should_quit:
            self.tick()

    def tick(self) -> None:
        """
        Tick the controller one iteration. This will update the ``PhysicsInterface`` as well as the ``DisplayInterface``
        implementations based upon the input values received.
        """
        self._display.clear()
        self._physics.update()
        utils.render_physics_state(physics=self._physics, display=self._display)
        utils.render_score_and_lives(
            scoring=self._scoring, lives=self._lives, display=self._display
        )
        self._display.update()

        self._handle_lost_balls()

    ###################
    # Private Methods #
    ###################
    def _handle_lost_balls(self) -> None:
        states = self._physics.get_ball_states()
        for state in states:
            ball_in_area = utils.check_ball_is_within_area(
                ball_position=state.position,
                width=self._config.playing_area[0],
                height=self._config.playing_area[1],
            )

            if ball_in_area:
                continue

            logger.info("Ball lost")
            self._physics.remove_ball(uid=state.uid)
            self._event_publisher.emit(event=events.GameEvents.BALL_LOST)

    def _handle_game_events(self, event: events.GameEvents) -> None:
        if event in [events.GameEvents.QUIT, events.GameEvents.GAME_OVER]:
            self.stop()
