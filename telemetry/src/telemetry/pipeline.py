from collections.abc import Iterable

from telemetry.analysis import Analysis, analyze_robots
from telemetry.grouper import group_robots_as_parsed_lines
from telemetry.parser import ParsedLine, parse_lines
from telemetry.reading import BadReading
from telemetry.telemetry_warning import TelemetryWarning
from telemetry.validator import validate_parsed_robots


def get_parsed_lines_and_bad_readings(
    telemetry_lines: Iterable[str],
) -> tuple[list[ParsedLine], list[BadReading]]:
    parsed_lines, bad_readings = parse_lines(telemetry_lines)
    return parsed_lines, bad_readings


def get_validated_robots(parsed_lines: list[ParsedLine]):
    parsed_robots = group_robots_as_parsed_lines(parsed_lines)
    validated_robots = validate_parsed_robots(parsed_robots)
    return validated_robots


def analyze_telemetry(
    telemetry_lines: Iterable[str], defined_warnings: list[TelemetryWarning]
) -> Analysis:
    parsed_lines, bad_readings = get_parsed_lines_and_bad_readings(telemetry_lines)
    validated_robots = get_validated_robots(parsed_lines)
    robot_analyses = analyze_robots(validated_robots, defined_warnings)
    analysis = Analysis(robot_analyses=robot_analyses, bad_readings=bad_readings)

    return analysis
