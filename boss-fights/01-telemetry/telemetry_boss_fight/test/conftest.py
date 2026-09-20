from pathlib import Path

import pytest

from telemetry_boss_fight.grouper import group_parsed_lines_by_robot
from telemetry_boss_fight.parser import (
    ParsedLine,
    parse_header,
    parse_line,
    parse_telemetry_lines,
)
from telemetry_boss_fight.reader import read_telemetry_file
from telemetry_boss_fight.rejected_reading import RejectedReading


@pytest.fixture
def sample_telemetry_path() -> Path:
    cur_dir = Path(__file__).resolve().parent
    data_dir = cur_dir / ".." / "data"
    sample_telemetry_path = data_dir / "sample_telemetry.csv"
    return sample_telemetry_path


@pytest.fixture
def sample_telemetry_lines(sample_telemetry_path: Path) -> list[str]:
    return read_telemetry_file(sample_telemetry_path)


@pytest.fixture
def sample_header() -> str:
    return "timestamp,robot_id,velocity,battery,temperature"


@pytest.fixture
def sample_header_parts(sample_header) -> list[str]:
    return parse_header(sample_header)


@pytest.fixture
def sample_expected_header_values() -> set[str]:
    # these are the known header values, not the known header order
    return {
        "timestamp",
        "robot_id",
        "velocity",
        "battery",
        "temperature",
    }


@pytest.fixture
def sample_line() -> str:
    return "2026-09-03T14:00:00.026Z,amr-02,1.366,57.7,34.1"


@pytest.fixture
def sample_line_out_of_range_temperature() -> str:
    return "2026-09-03T14:00:00.026Z,amr-02,1.366,57.7,1234.1"


@pytest.fixture
def sample_parsed_line(sample_line: str, sample_header_parts: list[str]) -> ParsedLine:
    return ParsedLine(
        line_number=0,
        original_line=sample_line,
        line_parts=parse_line(sample_line, sample_header_parts),
        header_parts=sample_header_parts,
    )


@pytest.fixture
def sample_parsed_line_out_of_range_temperature(
    sample_line_out_of_range_temperature: str, sample_header_parts: list[str]
) -> ParsedLine:
    return ParsedLine(
        line_number=0,
        original_line=sample_line_out_of_range_temperature,
        line_parts=parse_line(
            sample_line_out_of_range_temperature, sample_header_parts
        ),
        header_parts=sample_header_parts,
    )


@pytest.fixture
def sample_parsed_lines(
    sample_telemetry_lines: list[str],
) -> list[ParsedLine]:
    parsed_lines, _rejected_readings = parse_telemetry_lines(sample_telemetry_lines)
    return parsed_lines


@pytest.fixture
def sample_rejected_reading(sample_parsed_line: ParsedLine) -> RejectedReading:
    return RejectedReading(
        line_number=sample_parsed_line.line_number,
        original_line=sample_parsed_line.original_line,
        errors=[],
    )


@pytest.fixture
def sample_rejected_readings(
    sample_telemetry_lines: list[str],
) -> list[RejectedReading]:
    _parsed_lines, rejected_readings = parse_telemetry_lines(sample_telemetry_lines)
    return rejected_readings


@pytest.fixture
def sample_known_robot_ids() -> set[str]:
    return {"amr-01", "amr-02", "amr-03"}


@pytest.fixture
def sample_grouped_parsed_robots(
    sample_parsed_lines: list[ParsedLine],
) -> dict[str, list[ParsedLine]]:
    return group_parsed_lines_by_robot(sample_parsed_lines)
