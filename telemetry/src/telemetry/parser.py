from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class MissingDataError(Exception):
    pass


@dataclass
class ParsedLine:
    TIMESTAMP_IDX = 0
    ROBOT_ID_IDX = 1
    VELOCITY_IDX = 2
    BATTERY_IDX = 3
    TEMPERATURE_IDX = 4
    NUM_COLUMNS = 5

    timestamp_str: str
    robot_id: str
    velocity_str: str
    battery_str: str
    temperature_str: str

    @staticmethod
    def parse_line(line: str) -> ParsedLine:
        parts = line.split(",")
        if len(parts) != ParsedLine.NUM_COLUMNS:
            raise MissingDataError("line is missing data")

        return ParsedLine(
            timestamp_str=parts[ParsedLine.TIMESTAMP_IDX],
            robot_id=parts[ParsedLine.ROBOT_ID_IDX],
            velocity_str=parts[ParsedLine.VELOCITY_IDX],
            battery_str=parts[ParsedLine.BATTERY_IDX],
            temperature_str=parts[ParsedLine.TEMPERATURE_IDX],
        )
