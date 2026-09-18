import pytest

from telemetry.exceptions import (
    BatteryNotANumberError,
    BatteryOutOfRangeError,
    ColumnCountError,
    TemperatureOutOfRangeError,
    TimestampFormatError,
    TimestampIdenticalError,
    TimestampOutOfOrderError,
    VelocityNotANumberError,
    VelocityOutOfRangeError,
    VelocityWasNaNError,
)
from telemetry.pipeline import analyze_telemetry
from telemetry.reading import BadReading
from telemetry.robot import Robot
from telemetry.telemetry_warning import TelemetryWarning


@pytest.fixture
def sample_known_bad_readings() -> set[tuple[int, str]]:
    known_bad_readings: set[tuple[int, str]] = {
        (2, TimestampFormatError.__name__),
        (39, VelocityWasNaNError.__name__),
        (97, BatteryNotANumberError.__name__),
        (142, BatteryOutOfRangeError.__name__),
        (203, TemperatureOutOfRangeError.__name__),
        (238, TimestampOutOfOrderError.__name__),
        (262, TimestampIdenticalError.__name__),
        (302, ColumnCountError.__name__),
        (324, VelocityNotANumberError.__name__),
        (363, VelocityOutOfRangeError.__name__),
    }
    return known_bad_readings


def test_all_defects_caught(
    sample_telemetry_lines: list[str],
    sample_defined_warnings: list[TelemetryWarning],
    sample_known_bad_readings: set[tuple[int, str]],
) -> None:

    sample_analysis = analyze_telemetry(sample_telemetry_lines, sample_defined_warnings)
    found_bad_readings: set[tuple[int, str]] = set()

    for ra in sample_analysis.robot_analyses.values():
        for br in ra.bad_readings:
            found_bad_readings.add((br.line_number, br.exception.__class__.__name__))
    for br in sample_analysis.bad_readings:
        found_bad_readings.add((br.line_number, br.exception.__class__.__name__))

    assert found_bad_readings == sample_known_bad_readings


def test_all_valid_lines_found(
    sample_known_bad_readings: set[tuple[int, str]],
    sample_validated_robots: dict[str, Robot],
) -> None:
    known_bad_line_numbers = {br[0] for br in sample_known_bad_readings}
    for validated_robot in sample_validated_robots.values():
        for reading in validated_robot.readings:
            assert reading.line_number not in known_bad_line_numbers


def test_all_line_numbers_accounted_for(
    sample_telemetry_lines: list[str],
    sample_validated_robots: dict[str, Robot],
    sample_bad_readings: list[BadReading],
) -> None:
    # each file will have 1 header line, so our range of line numbers is 2:len(lines)
    line_numbers = {ln + 1 for ln in range(1, len(sample_telemetry_lines))}
    assert len(line_numbers) == len(sample_telemetry_lines) - 1
    assert 2 in line_numbers and len(sample_telemetry_lines) in line_numbers

    for validated_robot in sample_validated_robots.values():
        for reading in validated_robot.readings:
            line_numbers.remove(reading.line_number)

        for bad_reading in validated_robot.bad_readings:
            line_numbers.remove(bad_reading.line_number)

    for bad_reading in sample_bad_readings:
        line_numbers.remove(bad_reading.line_number)

    assert line_numbers == set()
