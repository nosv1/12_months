import pytest

from telemetry_boss_fight.errors import InconsistentHeaderError, RowColumnCountError
from telemetry_boss_fight.parser import ParsedLine, parse_header, parse_line

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
def test_header_rejects(value: str, expected_error) -> None:
    with pytest.raises(expected_error):
        parse_header(value)


def test_parsed_line_accepts(sample_line: str, sample_header_parts: list[str]) -> None:
    line_parts = parse_line(sample_line, sample_header_parts)
    parsed_line = ParsedLine(1, sample_line, line_parts, sample_header_parts)
    assert parsed_line.fields["timestamp"] == "2026-09-03T14:00:00.026Z"
    assert parsed_line.fields["robot_id"] == "amr-02"
    assert parsed_line.fields["velocity"] == "1.366"
    assert parsed_line.fields["battery"] == "57.7"
    assert parsed_line.fields["temperature"] == "34.1"


@pytest.mark.parametrize(
    ("value, expected_error"),
    [
        ("2026-09-03T14:00:00.026Z,amr-02,1.366,57.7", RowColumnCountError),
        ("2026-09-03T14:00:00.026Z,amr-02,1.366,57.7,34.1,0", RowColumnCountError),
    ],
)
def test_parsed_line_rejects(
    value: str, expected_error, sample_header_parts: list[str]
) -> None:
    with pytest.raises(expected_error):
        parse_line(value, sample_header_parts)


from telemetry_boss_fight.parser import parse_telemetry_lines


def test_parser_counts_match_line_counts(sample_telemetry_lines: list[str]) -> None:
    parsed_lines, rejected_readings = parse_telemetry_lines(sample_telemetry_lines)
    found_lines = {pl.original_line for pl in parsed_lines}
    for rr in rejected_readings:
        found_lines.add(rr.original_line)
    assert set(sample_telemetry_lines[1:]) == found_lines


##########           LINE           ##########
