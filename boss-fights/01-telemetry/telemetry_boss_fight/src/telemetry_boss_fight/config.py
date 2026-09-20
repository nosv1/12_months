# these are the known header values, not the known header order

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass(frozen=True)
class Header:
    header: str
    type: type
    range: None | tuple[float, float]


class EXPECTED_HEADERS(Enum):
    TIMESTAMP = Header(header="timestamp", type=datetime, range=None)  # ISO 8601, UTC
    ROBOT_ID = Header(header="robot_id", type=str, range=None)  # `amr-01`
    VELOCITY = Header(header="velocity", type=float, range=(-2.0, 2.0))  # m/s
    BATTERY = Header(header="battery", type=float, range=(0.0, 100.0))  # percent
    TEMPERATURE = Header(header="temperature", type=float, range=(-40.0, 150.0))  # °C

    @staticmethod
    def as_str_set() -> set[str]:
        return {member.value.header for member in EXPECTED_HEADERS}
