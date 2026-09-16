from pathlib import Path

import pytest

from telemetry.analysis import Analysis
from telemetry.exceptions import (
    BatteryNotANumberError,
    BatteryOutOfRangeError,
    ColumnCountError,
    TemperatureOutOfRangeError,
    TimestampIdenticalError,
    TimestampOutOfOrderError,
    VelocityNotANumberError,
    VelocityOutOfRangeError,
    VelocityWasNaNError,
)
from telemetry.pipeline import analyze_telemetry
from telemetry.reader import read_file
from telemetry.telemetry_warning import BatteryWarning, TemperatureWarning

### ANALYSIS


@pytest.fixture
def sample_analysis() -> Analysis:
    file_dir = Path(__file__).resolve().parent
    data_dir = file_dir / "../data"
    telemetry_file_path = data_dir / "sample_telemetry.csv"
    telemetry_lines = read_file(telemetry_file_path)

    defined_warnings = [
        BatteryWarning(min_battery=20),
        TemperatureWarning(max_temperature=60),
    ]

    analysis = analyze_telemetry(telemetry_lines, defined_warnings)
    return analysis


def test_all_defects_caught(sample_analysis: Analysis) -> None:
    known_bad_readings: set[tuple[int, str]] = {
        # no timestamp format error?
        (39, VelocityWasNaNError.__name__),
        (97, BatteryNotANumberError.__name__),
        (142, BatteryOutOfRangeError.__name__),
        (203, TemperatureOutOfRangeError.__name__),
        (238, TimestampOutOfOrderError.__name__),
        (261, TimestampIdenticalError.__name__),
        (302, ColumnCountError.__name__),
        (324, VelocityNotANumberError.__name__),
        (363, VelocityOutOfRangeError.__name__),
    }
    found_bad_readings: set[tuple[int, str]] = set()

    for ra in sample_analysis.robot_analyses.values():
        for br in ra.bad_readings:
            found_bad_readings.add((br.line_number, br.exception.__class__.__name__))
    for br in sample_analysis.bad_readings:
        found_bad_readings.add((br.line_number, br.exception.__class__.__name__))

    assert found_bad_readings == known_bad_readings


def test_all_valid_lines_found(sample_analysis: Analysis) -> None:
    pass
