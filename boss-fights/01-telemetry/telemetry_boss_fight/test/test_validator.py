from datetime import UTC, datetime

import pytest

from telemetry_boss_fight.errors import (
    TelemetryException,
    TimestampFormatError,
    TimestampIdenticalError,
    TimestampsOutOfOrderError,
    ValueOutOfRangeError,
    ValueStrNotANumber,
)
from telemetry_boss_fight.validator import (
    validate_battery,
    validate_temperature,
    validate_timestamp,
    validate_timestamp_order,
    validate_velocity,
)

##########           TIMESTAMP           ##########


@pytest.mark.parametrize(
    ("value_str, expected"),
    [
        (
            "2026-09-03T14:00:00.026Z",
            datetime(2026, 9, 3, 14, 0, 0, 26000, tzinfo=UTC),
        )
    ],
)
def test_timestamp_format_accepts(value_str: str, expected: int) -> None:
    assert validate_timestamp(value_str) == expected


@pytest.mark.parametrize(
    ("value_str, expected_error"),
    [
        ("2026--03T14:00:00.016Z", TimestampFormatError),
    ],
)
def test_timestamp_format_rejects(
    value_str: str, expected_error: type[TelemetryException]
) -> None:
    with pytest.raises(expected_error):
        validate_timestamp(value_str)


@pytest.mark.parametrize(
    ("timestamp, prev_timestamp, expected_error"),
    [
        (
            datetime(2026, 9, 3, 14, 0, 0, 26000, tzinfo=UTC),  # current
            datetime(2026, 9, 3, 15, 0, 0, 26000, tzinfo=UTC),  # previous
            TimestampsOutOfOrderError,
        ),
        (
            datetime(2026, 9, 3, 14, 0, 0, 26000, tzinfo=UTC),  # current
            datetime(2026, 9, 3, 14, 0, 0, 26000, tzinfo=UTC),  # previous
            TimestampIdenticalError,
        ),
    ],
)
def test_timestamp_order_rejects(
    timestamp: datetime,
    prev_timestamp: datetime,
    expected_error: type[TelemetryException],
) -> None:
    with pytest.raises(expected_error):
        validate_timestamp_order(timestamp, prev_timestamp)


##########           VELOCITY           ##########


@pytest.mark.parametrize(
    ("value_str, expected"),
    [
        pytest.param("-2.0", -2.0, id="at-lower-bound"),
        pytest.param("2.0", 2.0, id="at-upper-bound"),
        pytest.param("0", 0.0, id="at-zero"),
    ],
)
def test_velocity_accepts(value_str: str, expected: int) -> None:
    assert validate_velocity(value_str) == expected


@pytest.mark.parametrize(
    ("value_str, expected_error"),
    [
        ("-2.1", ValueOutOfRangeError),
        ("2.1", ValueOutOfRangeError),
        ("", ValueStrNotANumber),
        ("nan", ValueStrNotANumber),
        ("ERR", ValueStrNotANumber),
    ],
)
def test_velocity_rejects(
    value_str: str, expected_error: type[TelemetryException]
) -> None:
    with pytest.raises(expected_error):
        validate_velocity(value_str)


##########           BATTERY           ##########


@pytest.mark.parametrize(
    ("value_str, expected"),
    [
        pytest.param("0.0", 0.0, id="at-lower-bound"),
        pytest.param("100.0", 100.0, id="at-upper-bound"),
        # pytest.param("0", 0.0, id="at-zero"),
    ],
)
def test_battery_accepts(value_str: str, expected: int) -> None:
    assert validate_battery(value_str) == expected


@pytest.mark.parametrize(
    ("value_str, expected_error"),
    [
        ("-0.1", ValueOutOfRangeError),
        ("100.1", ValueOutOfRangeError),
        ("", ValueStrNotANumber),
        ("nan", ValueStrNotANumber),
        ("ERR", ValueStrNotANumber),
    ],
)
def test_battery_rejects(
    value_str: str, expected_error: type[TelemetryException]
) -> None:
    with pytest.raises(expected_error):
        validate_battery(value_str)


##########           TEMPERATURE           ##########


@pytest.mark.parametrize(
    ("value_str, expected"),
    [
        pytest.param("-40.0", -40.0, id="at-lower-bound"),
        pytest.param("150.0", 150, id="at-upper-bound"),
        pytest.param("0", 0.0, id="at-zero"),
    ],
)
def test_temperature_accepts(value_str: str, expected: int) -> None:
    assert validate_temperature(value_str) == expected


@pytest.mark.parametrize(
    ("value_str, expected_error"),
    [
        ("-40.1", ValueOutOfRangeError),
        ("150.1", ValueOutOfRangeError),
        ("", ValueStrNotANumber),
        ("nan", ValueStrNotANumber),
        ("ERR", ValueStrNotANumber),
    ],
)
def test_temperature_rejects(
    value_str: str, expected_error: type[TelemetryException]
) -> None:
    with pytest.raises(expected_error):
        validate_temperature(value_str)
