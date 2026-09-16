from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass

from telemetry.reading import BadReading

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

    line_number: int
    original_line: str

    timestamp_str: str
    robot_id: str
    velocity_str: str
    battery_str: str
    temperature_str: str


def parse_line(line: str, line_number: int) -> ParsedLine:
    parts = line.split(",")
    if len(parts) != ParsedLine.NUM_COLUMNS:
        raise MissingDataError("line is missing data")

    return ParsedLine(
        line_number=line_number,
        original_line=line,
        timestamp_str=parts[ParsedLine.TIMESTAMP_IDX],
        robot_id=parts[ParsedLine.ROBOT_ID_IDX],
        velocity_str=parts[ParsedLine.VELOCITY_IDX],
        battery_str=parts[ParsedLine.BATTERY_IDX],
        temperature_str=parts[ParsedLine.TEMPERATURE_IDX],
    )


def parse_lines(
    lines: Iterable[str], headers_count: int = 0
) -> tuple[list[ParsedLine], list[BadReading]]:
    parsed_lines: list[ParsedLine] = []
    bad_readings: list[BadReading] = []
    for i, line in enumerate(lines):
        if i < headers_count:
            continue
        line_number = i + 1
        try:
            parsed_lines.append(parse_line(line, line_number))

        except MissingDataError as err:
            logger.warning("Line %d was missing data.", line_number)
            bad_readings.append(BadReading(line_number, line, err))
            continue

    return parsed_lines, bad_readings
