import dataclasses
import typing


@dataclasses.dataclass
class Wall:
    """
    The Wall class specifies wall elements to be modelled in the Physics engine
    and provide the general boundaries for the Pinball game.
    """

    uid: int
    points: typing.List[typing.Tuple[float, float]]
