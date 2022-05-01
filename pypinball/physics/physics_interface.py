import typing
from .. import domain


class PhysicsInterface(typing.Protocol):
    def actuate_flipper(self, flipper: domain.Flipper) -> bool:
        ...

    def actuate_flippers(self, actuate_button: domain.Buttons) -> None:
        ...

    def add_ball(self, ball: domain.Ball) -> None:
        ...

    def add_flipper(self, flipper: domain.Flipper) -> bool:
        ...

    def update(self) -> None:
        ...
