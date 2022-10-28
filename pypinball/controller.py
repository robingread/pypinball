from . import display, domain, events, inputs, log, physics, utils
from .game_config import GameConfig

logger = log.get_logger(__name__)


class ObjectIdGenerator:
    """
    The object ID generator is used to create unique ID for objects
    as needed throughout a game.
    """

    def __init__(self):
        self._count = -1

    def generate_id(self) -> int:
        """
        Generate a new ID from the internal counter.
        """
        self._count += 1
        return self._count

    def reset(self) -> None:
        """
        Reset the internal counter.
        """
        self._count = -1


class Controller:
    def __init__(
        self,
        display_interface: display.DisplayInterface,
        config: GameConfig,
        physics_interface: physics.PhysicsInterface,
        event_publisher: events.GameEventPublisher,
    ):
        self._display = display_interface
        self._config = config
        self._physics = physics_interface
        self._id_generator = ObjectIdGenerator()
        self._event_publisher = event_publisher

        self._should_quit = False

    ##################
    # Public Methods #
    ##################
    def handle_input_event(self, event: inputs.InputEvents) -> None:
        """
        Input device event handler class. This method is used to react to input
        events and should be registred as a callback with a ``InputEventPublisher`` instance.

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
            # TODO: Make this a unit-testable function
            uid = self._id_generator.generate_id()
            ball = domain.Ball(uid=uid, position=(400, 500))
            self._physics.add_ball(ball=ball)
            self._physics.launch_ball(uid=ball.uid)

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
        ret += [self._physics.add_flipper(f) for f in self._config.flippers]
        ret += [self._physics.add_wall(w) for w in self._config.walls]
        return all(ret)

    def stop(self) -> None:
        """
        Stop running the controller.
        """
        logger.info("Stopping the controller main loop")
        self._should_quit = True

    def run(self) -> None:
        """
        Start running the controller main loop.
        """
        logger.info("Starting main loop")
        while not self._should_quit:
            self.tick()

    def tick(self) -> None:
        """
        Tick the controller. This will update the PhysicsInterface as well as the DisplayInterface
        implementations.
        """
        self._display.clear()
        self._physics.update()
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
        if event in [events.GameEvents.QUIT]:
            self.stop()
