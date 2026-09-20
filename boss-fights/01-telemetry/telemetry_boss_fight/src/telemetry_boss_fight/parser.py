from __future__ import annotations

import logging

from telemetry_boss_fight.accepted_reading import AcceptedReading
from telemetry_boss_fight.errors import (
    InconsistentHeaderError,
    RowColumnCountError,
    TelemetryException,
)
from telemetry_boss_fight.rejected_reading import RejectedReading
from telemetry_boss_fight.robot import Robot
from telemetry_boss_fight.validator import (
    validate_header_parts,
    validate_line_parts_count,
    validate_parsed_line,
)

logger = logging.getLogger(__name__)


class ParsedLine:
    def __init__(
        self,
        line_number: int,
        original_line: str,
        line_parts: list[str],
        header_parts: list[str],
    ) -> None:
        self.line_number = line_number
        self.original_line = original_line
        # fields is a dict[header, field_value]
        self.fields: dict[str, str] = {
            header_parts[i]: v for i, v in enumerate(line_parts)
        }


def parse_header(header: str) -> list[str]:
    header_parts = header.split(",")
    return validate_header_parts(header_parts)


def handle_telemetry_exception(
    line_number: int, telemetry_exception: TelemetryException
):
    logger.warning("Line %d had an error - %s", line_number, telemetry_exception)


def parse_line(line: str, header_parts: list[str]) -> list[str]:
    line_parts = line.strip().split(",")
    return validate_line_parts_count(line_parts, header_parts)


def parse_telemetry_lines(
    telemetry_lines: list[str],
) -> tuple[list[ParsedLine], list[RejectedReading]]:
    parsed_lines: list[ParsedLine] = []
    rejected_readings: list[RejectedReading] = []

    if telemetry_lines == []:
        return parsed_lines, rejected_readings

    if len(telemetry_lines[0].strip()) == 0:
        return parsed_lines, rejected_readings

    try:
        header_parts = parse_header(telemetry_lines[0].strip())

    except InconsistentHeaderError:
        return parsed_lines, rejected_readings

    for i, line in enumerate(telemetry_lines[1:]):
        line_number = i + 2

        try:
            parsed_lines.append(
                ParsedLine(
                    line_number=line_number,
                    original_line=line,
                    line_parts=parse_line(line, header_parts),
                    header_parts=header_parts,
                )
            )

        except RowColumnCountError as te:
            handle_telemetry_exception(line_number, te)
            rejected_readings.append(RejectedReading(line_number, line, [te]))
            continue

    return parsed_lines, rejected_readings


def validate_parsed_robots(
    parsed_robots: dict[str, list[ParsedLine]],
) -> dict[str, Robot]:
    robots: dict[str, Robot] = {}

    for robot_id, parsed_lines in parsed_robots.items():
        robots[robot_id] = Robot(robot_id, [], [])

        for parsed_line in parsed_lines:
            accepted_or_rejected_reading = validate_parsed_line(
                parsed_line.fields,
                RejectedReading(
                    line_number=parsed_line.line_number,
                    original_line=parsed_line.original_line,
                    errors=[],
                ),
            )

            if isinstance(accepted_or_rejected_reading, AcceptedReading):
                robots[robot_id].accepted_readings.append(accepted_or_rejected_reading)

            else:
                for err in accepted_or_rejected_reading.errors:
                    handle_telemetry_exception(parsed_line.line_number, err)
                robots[robot_id].rejected_readings.append(accepted_or_rejected_reading)
                continue

            # validate timestamp order

    return robots
