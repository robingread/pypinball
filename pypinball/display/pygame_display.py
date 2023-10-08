import math
import typing

import pygame

from .. import events, game_config, log
from .display_interface import DisplayInterface
from .pygame_lives import LivesCache
from .pygame_score import ScoringCache
from .utils import calculate_rectangle_bounding_box_image_coordinates

logger = log.get_logger(name=__name__)


class PyGameDisplay(DisplayInterface):
    """Implementation of a DisplayInterface class that uses PyGame as the underling Graphics engine/manager."""

    def __init__(
        self,
        width: int,
        height: int,
        game_events: events.GameEventPublisher,
        config: game_config.DisplayConfig,
    ) -> None:
        self._width = width
        self._game_events = game_events
        pygame.init()
        pygame.font.init()
        self._screen = pygame.display.set_mode(size=(width, height))
        self._clock = pygame.time.Clock()

        self._background_surface = pygame.Surface(size=(width, height))
        self._background_surface.blit(
            source=pygame.image.load(config.background_image_path).convert_alpha(),
            dest=(0, 0),
        )

        self._ball_img = pygame.image.load(config.ball_image_path).convert_alpha()
        self._round_bumper_img = pygame.image.load(
            config.round_bumper_image_path
        ).convert_alpha()
        self._rectangle_bumper_img = pygame.image.load(
            config.rectangle_bumper_image_path
        ).convert_alpha()
        self._flipper_img = pygame.image.load(config.flipper_image_path).convert_alpha()

        self._lives_cache = LivesCache(
            max_lives=5,
            icon_path=config.life_icon_path,
            icon_width=25,
            icon_spacing=3,
        )
        self._score_cache = ScoringCache(max_score=500)

    def clear(self) -> None:
        # self._screen.fill(pygame.Color("white"))
        pass

    def close(self) -> None:
        pygame.quit()

    def draw_background(self) -> None:
        self._screen.blit(self._background_surface, (0, 0))

    def draw_ball(
        self, pos: typing.Tuple[float, float], diameter: float, alpha: float
    ) -> None:
        x, y = calculate_rectangle_bounding_box_image_coordinates(
            pos=pos, size=(diameter, diameter), angle=0.0
        )
        img = pygame.transform.scale(self._ball_img, size=(diameter, diameter))
        img = pygame.transform.rotate(img, angle=math.degrees(0.0))
        img.set_alpha(int(alpha * 255))
        self._screen.blit(img, (x, y))

    def draw_round_bumper(
        self, pos: typing.Tuple[float, float], diameter: float, alpha: float
    ) -> None:
        x, y = calculate_rectangle_bounding_box_image_coordinates(
            pos=pos, size=(diameter, diameter), angle=0.0
        )
        img = pygame.transform.scale(self._round_bumper_img, size=(diameter, diameter))
        img = pygame.transform.rotate(img, angle=math.degrees(0.0))
        img.set_alpha(int(alpha * 255))
        self._screen.blit(img, (x, y))

    def draw_rectangle_bumper(
        self,
        pos: typing.Tuple[float, float],
        size: typing.Tuple[float, float],
        angle: float,
        alpha: float,
    ) -> None:
        padding = 10
        width = size[0] + padding
        height = size[1] + padding

        x, y = calculate_rectangle_bounding_box_image_coordinates(
            pos=pos, size=(width, height), angle=angle
        )

        img = pygame.transform.scale(self._rectangle_bumper_img, size=(width, height))
        img = pygame.transform.rotate(img, angle=math.degrees(-angle))
        img.set_alpha(int(alpha * 255))
        self._screen.blit(img, (x, y))

    def draw_flipper(
        self,
        pos: typing.Tuple[float, float],
        angle: float,
        size: typing.Tuple[float, float],
        alpha: float,
    ) -> None:
        width = size[0]
        height = size[1]

        x, y = calculate_rectangle_bounding_box_image_coordinates(
            pos=pos, size=(width, height), angle=angle
        )

        img = pygame.transform.scale(self._flipper_img, size=(width, height))
        img = pygame.transform.rotate(img, angle=math.degrees(-angle))
        img.set_alpha(int(alpha * 255))
        self._screen.blit(img, (x, y))

    def draw_lives(self, lives: int) -> None:
        surface = self._lives_cache[lives]
        self._screen.blit(surface, (self._width - surface.get_rect().width, 0))

    def draw_score(self, score: str) -> None:
        self._screen.blit(self._score_cache[int(score)], (0, 0))

    def update(self) -> None:
        pygame.display.flip()
        self._clock.tick(50)
        pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Closing display window")
                self._game_events.emit(event=events.GameEvents.QUIT)
                break
