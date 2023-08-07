import math
import typing

import pygame

from .. import events, game_config, log
from .display_interface import DisplayInterface
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
        self._height = height
        self._game_events = game_events
        pygame.init()
        pygame.font.init()
        self._screen = pygame.display.set_mode(size=(width, height))
        self._clock = pygame.time.Clock()

        self._background_img = pygame.image.load(
            config.background_image_path
        ).convert_alpha()
        self._ball_img = pygame.image.load(config.ball_image_path).convert_alpha()
        self._round_bumper_img = pygame.image.load(
            config.round_bumper_image_path
        ).convert_alpha()
        self._rectable_bumper_img = pygame.image.load(
            config.rectangle_bumper_image_path
        ).convert_alpha()
        self._flipper_img = pygame.image.load(config.flipper_image_path).convert_alpha()

    def clear(self) -> None:
        self._screen.fill(pygame.Color("white"))

    def close(self) -> None:
        pygame.quit()

    def draw_background(self) -> None:
        width = self._screen.get_width()
        height = self._screen.get_height()
        img = pygame.transform.scale(self._background_img, size=(width, height))
        self._screen.blit(img, (0, 0))

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

        img = pygame.transform.scale(self._rectable_bumper_img, size=(width, height))
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
        my_font = pygame.font.SysFont("Comic Sans MS", 35)
        text_surface = my_font.render("*" * lives, False, (255, 255, 255))
        self._screen.blit(
            text_surface, (self._width - text_surface.get_rect().width, 0)
        )

    def draw_score(self, score: str) -> None:
        my_font = pygame.font.SysFont("Comic Sans MS", 35)
        text_surface = my_font.render(score, False, (255, 255, 255))
        self._screen.blit(text_surface, (0, 0))

    def update(self) -> None:
        pygame.display.flip()
        self._clock.tick(50)
        pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Closing display window")
                self._game_events.emit(event=events.GameEvents.QUIT)
                break
