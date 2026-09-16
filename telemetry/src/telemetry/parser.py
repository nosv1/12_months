from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass

from telemetry.exceptions import ColumnCountError
from telemetry.reading import BadReading

logger = logging.getLogger(__name__)


@dataclass
class ParsedLine:
    TIMESTAMP_IDX = 0
    ROBOT_ID_IDX = 1
    VELOCITY_IDX = 2
    BATTERY_IDX = 3
    TEMPERATURE_IDX = 4

    line_number: int
    original_line: str

    timestamp_str: str
    robot_id: str
    velocity_str: str
    battery_str: str
    temperature_str: str


def parse_line(line: str, line_number: int, num_columns: int) -> ParsedLine:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != num_columns:
        raise ColumnCountError(num_columns, len(parts))

    return ParsedLine(
        line_number=line_number,
        original_line=line,
        timestamp_str=parts[ParsedLine.TIMESTAMP_IDX],
        robot_id=parts[ParsedLine.ROBOT_ID_IDX],
        velocity_str=parts[ParsedLine.VELOCITY_IDX],
        battery_str=parts[ParsedLine.BATTERY_IDX],
        temperature_str=parts[ParsedLine.TEMPERATURE_IDX],
    )


def parse_lines(lines: Iterable[str]) -> tuple[list[ParsedLine], list[BadReading]]:
    parsed_lines: list[ParsedLine] = []
    bad_readings: list[BadReading] = []
    if not lines:
        return parsed_lines, bad_readings

    header_parts = list(lines)[0].split(",")
    headers_count = len(header_parts)
    for i, line in enumerate(lines):
        if i < headers_count:
            continue
        line_number = i + 1
        try:
            parsed_lines.append(parse_line(line, line_number, len(header_parts)))

        except ColumnCountError as err:
            logger.warning(
                "Line %d has a different number of columns than expected - %s",
                line_number,
                str(err),
            )
            bad_readings.append(BadReading(line_number, line, err))
            continue

    return parsed_lines, bad_readings
