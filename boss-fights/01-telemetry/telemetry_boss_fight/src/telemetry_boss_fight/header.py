from dataclasses import dataclass


@dataclass(frozen=True)
class Header:
    header: str
    type: type
    range: None | tuple[float, float]
