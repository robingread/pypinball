import dataclasses


@dataclasses.dataclass(frozen=True)
class FlipperConfig:
    position: tuple
    length: float
    min_angle: float
    max_angle: float


class Flipper:
    def __init__(self, uid: int, config: FlipperConfig):
        self._uid = uid
        self._angle = config.min_angle
        self._config = config

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def uid(self) -> int:
        return self._uid
