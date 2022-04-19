import typing


class DisplayInterface(typing.Protocol):
    def clear(self) -> None:
        ...

    def display_image(self, path: str) -> None:
        ...

    def draw_ball(self, pos: list, radius: int) -> None:
        ...

    def draw_flipper(self) -> None:
        ...

    def update(self) -> None:
        ...
