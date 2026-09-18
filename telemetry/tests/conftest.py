from pathlib import Path

import pytest

from telemetry.parser import ParsedLine
from telemetry.pipeline import get_parsed_lines_and_bad_readings, get_validated_robots
from telemetry.reader import read_file
from telemetry.reading import BadReading
from telemetry.robot import Robot
from telemetry.telemetry_warning import (
    BatteryWarning,
    TelemetryWarning,
    TemperatureWarning,
)


@pytest.fixture
def sample_defined_warnings() -> list[TelemetryWarning]:
    defined_warnings = [
        BatteryWarning(min_battery=20),
        TemperatureWarning(max_temperature=60),
    ]

    return defined_warnings


@pytest.fixture
def sample_telemetry_lines() -> list[str]:
    file_dir = Path(__file__).resolve().parent
    data_dir = file_dir / ".." / "data"
    telemetry_file_path = data_dir / "sample_telemetry.csv"
    telemetry_lines = read_file(telemetry_file_path)
    return telemetry_lines


@pytest.fixture
def sample_parsed_lines(sample_telemetry_lines: list[str]) -> list[ParsedLine]:
    parsed_lines, bad_readings = get_parsed_lines_and_bad_readings(
        sample_telemetry_lines
    )
    return parsed_lines


@pytest.fixture
def sample_bad_readings(sample_telemetry_lines: list[str]) -> list[BadReading]:
    parsed_lines, bad_readings = get_parsed_lines_and_bad_readings(
        sample_telemetry_lines
    )
    return bad_readings


@pytest.fixture
def sample_validated_robots(sample_parsed_lines: list[ParsedLine]) -> dict[str, Robot]:
    validated_robots = get_validated_robots(sample_parsed_lines)
    return validated_robots
