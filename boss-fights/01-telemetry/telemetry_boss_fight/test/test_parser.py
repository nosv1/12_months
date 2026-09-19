import pytest

from telemetry_boss_fight.errors import (
    InconsistentHeaderError,
    RowColumnCountError,
    TelemetryException,
)
from telemetry_boss_fight.parser import parse_header, parse_line

##########           HEADER           ##########


def test_header_accepts(sample_header: str) -> None:
    parse_header(sample_header)


@pytest.mark.parametrize(
    ("value, expected_error"),
    [
        (
            "timestamp,robot_id,velocity,battery,temperature,angle",
            InconsistentHeaderError,
        ),
        ("timestamp,robot_id,velocity,battery", InconsistentHeaderError),
    ],
)
def test_header_rejects(value: str, expected_error: TelemetryException) -> None:
    with pytest.raises(expected_error):
        parse_header(value)


def test_parsed_line_accepts(sample_line: str, sample_header_parts: list[str]) -> None:
    parse_line(sample_line, sample_header_parts)


@pytest.mark.parametrize(
    ("value, expected_error"),
    [
        ("2026-09-03T14:00:00.026Z,amr-02,1.366,57.7", RowColumnCountError),
        ("2026-09-03T14:00:00.026Z,amr-02,1.366,57.7,34.1,0", RowColumnCountError),
    ],
)
def test_parsed_line_rejects(
    value: str, expected_error: TelemetryException, sample_header_parts: list[str]
) -> None:
    with pytest.raises(expected_error):
        parse_line(value, sample_header_parts)


##########           ...           ##########
