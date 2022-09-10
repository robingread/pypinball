import pygame
from .display_interface import DisplayInterface
from ..event import Event
from .. import events


class PyGameDisplay(DisplayInterface):
    def __init__(self, width: int, height: int, game_events: events.GameEventPublisher):
        self._game_events = game_events
        pygame.init()
        self._screen = pygame.display.set_mode(size=(width, height))
        self._clock = pygame.time.Clock()
        self.window_close = Event()

    def clear(self) -> None:
        self._screen.fill(pygame.Color("white"))

    def close(self) -> None:
        pygame.quit()

    def draw_ball(self, pos: list, radius: int) -> None:
        colour = (0, 2, 128)
        pygame.draw.circle(
            surface=self._screen, center=pos, radius=radius, color=colour
        )

    def update(self) -> None:
        pygame.display.flip()
        self._clock.tick(50)
        pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self._game_events.emit(event=events.GameEvents.QUIT)
                break
