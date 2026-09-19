# If the tool hits a failure it doesn't have a category for, put it in an **unrecognized** bucket with a count, and report that count every time — it should always be zero.
# **Quarantine the row, don't crash.** A

from __future__ import annotations

import logging

from telemetry_boss_fight.errors import (
    InconsistentHeaderError,
    RowColumnCountError,
    TelemetryException,
)
from telemetry_boss_fight.rejected_reading import RejectedReading
from telemetry_boss_fight.validator import validate_header_parts, validate_line_parts

logger = logging.getLogger(__name__)


class ParsedLine:
    def __init__(self, line_number: int, original_line: str, fields: dict[str, str]):
        self.line_number = line_number
        self.original_line = original_line
        # fields is a dict[header, field]
        self.fields = fields


def parse_header(header: str) -> list[str]:
    header_parts = header.split(",")
    return validate_header_parts(header_parts)


def handle_telemetry_exception(
    line_number: int, telemetry_exception: TelemetryException
):
    logger.warning("Line %d had an error - %s", line_number, telemetry_exception)


def parse_line(line: str, header_parts: list[str]) -> list[str]:
    line_parts = line.strip().split(",")
    line_parts = validate_line_parts(line_parts, header_parts)


def parse_telemetry_lines(
    telemetry_lines: list[str],
) -> tuple[list[ParsedLine], list[RejectedReading]]:
    parsed_lines: list[ParsedLine] = []
    rejected_readings: list[RejectedReading] = []

    if telemetry_lines == []:
        return parsed_lines

    if len(telemetry_lines[0].strip()) == 0:
        return parsed_lines

    try:
        header_parts = parse_header(telemetry_lines[0].strip())

    except InconsistentHeaderError:
        return parsed_lines

    for i, line in telemetry_lines[1:]:
        line_number = i + 1

        try:
            parsed_line = parse_line(line)

        except RowColumnCountError as te:
            handle_telemetry_exception(line_number, te)
            rejected_readings.append(RejectedReading(line_number, line, [te]))
            continue

        #######    DO SOMETHING WITH PARSED LINE NOW    #############

    return parsed_lines
