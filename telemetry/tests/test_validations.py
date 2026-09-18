from datetime import datetime, timezone

import pytest

from telemetry.exceptions import (
    BatteryNotANumberError,
    BatteryOutOfRangeError,
    BatteryWasNaNError,
    ColumnCountError,
    TelemetryException,
    TemperatureNotANumberError,
    TemperatureOutOfRangeError,
    TemperatureWasNaNError,
    TimestampFormatError,
    TimestampIdenticalError,
    TimestampOutOfOrderError,
    VelocityNotANumberError,
    VelocityOutOfRangeError,
    VelocityWasNaNError,
)
from telemetry.parser import parse_line
from telemetry.validator import (
    validate_battery,
    validate_temperature,
    validate_timestamp_format,
    validate_timestamp_order,
    validate_velocity,
)

###   TELEMETRY LINE   ###


@pytest.mark.parametrize(
    "value, expected_error",
    [
        ("2026-09-03T14:01:39.040Z,amr-03,1.143,70.1\n", ColumnCountError),
        ("2026-09-03T14:00:46.018Z,amr-03,0.992,104.2,46.6,0.0\n", ColumnCountError),
    ],
)
def test_incorrect_column_counts(value, expected_error):
    with pytest.raises(expected_error):
        parse_line(value, 0, 5)


###   TIMESTAMP   ###
@pytest.mark.parametrize("value", [pytest.param("2026-09-03T14:00:00.016Z")])
def test_timestamp_format_accepts(value: str) -> None:
    assert validate_timestamp_format(value) == datetime(
        2026, 9, 3, 14, 0, 0, 16000, tzinfo=timezone.utc
    )


@pytest.mark.parametrize(
    "value, expected_error", [("2060903T14:00:00.016Z", TimestampFormatError)]
)
def test_timestamp_format_rejects(
    value: str, expected_error: type[TelemetryException]
) -> None:
    with pytest.raises(expected_error):
        validate_timestamp_format(value)


@pytest.mark.parametrize(
    "timestamp, prev_timestamp",
    [
        (
            datetime(2026, 9, 3, 14, 0, 0, 16000, tzinfo=timezone.utc),
            datetime(2026, 9, 3, 14, 0, 0, 15000, tzinfo=timezone.utc),
        )
    ],
)
def test_timestamp_order_accepts(timestamp: datetime, prev_timestamp: datetime) -> None:
    assert validate_timestamp_order(timestamp, prev_timestamp)


@pytest.mark.parametrize(
    "timestamp, prev_timestamp, expected_error",
    [
        (
            datetime(2026, 9, 3, 14, 0, 0, 16000, tzinfo=timezone.utc),
            datetime(2026, 9, 3, 14, 0, 0, 17000, tzinfo=timezone.utc),
            TimestampOutOfOrderError,
        ),
        (
            datetime(2026, 9, 3, 14, 0, 0, 16000, tzinfo=timezone.utc),
            datetime(2026, 9, 3, 14, 0, 0, 16000, tzinfo=timezone.utc),
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


###   VELOCITY   ###


@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param("2.0", 2.0, id="at-upper-bound"),
        pytest.param("-2.0", -2.0, id="at-lower-bound"),
        pytest.param("0.0", 0.0, id="zero"),
    ],
)
def test_velocity_accepts(value: str, expected: float) -> None:
    assert validate_velocity(value) == expected


@pytest.mark.parametrize(
    "value, expected_error",
    [
        ("-2.001", VelocityOutOfRangeError),
        ("2.001", VelocityOutOfRangeError),
        ("inf", VelocityOutOfRangeError),
        ("ERR", VelocityNotANumberError),
        ("", VelocityNotANumberError),
        ("nan", VelocityWasNaNError),
    ],
)
def test_velocity_rejects(value: str, expected_error: type[TelemetryException]) -> None:
    with pytest.raises(expected_error):
        validate_velocity(value)


###   BATTERY   ###


@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param("100", 100.0, id="at-upper-bound"),
        pytest.param("0.0", 0.0, id="at-lower-bound (and zero)"),
        pytest.param("50", 50.0, id="fifty"),
    ],
)
def test_battery_accepts(value: str, expected: float) -> None:
    assert validate_battery(value) == expected


@pytest.mark.parametrize(
    "value, expected_error",
    [
        ("-0.1", BatteryOutOfRangeError),
        ("100.1", BatteryOutOfRangeError),
        ("inf", BatteryOutOfRangeError),
        ("ERR", BatteryNotANumberError),
        ("", BatteryNotANumberError),
        ("nan", BatteryWasNaNError),
    ],
)
def test_battery_rejects(value: str, expected_error: type[TelemetryException]) -> None:
    with pytest.raises(expected_error):
        validate_battery(value)


###   TEMPERATURE   ###


@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param("150", 150.0, id="at-upper-bound"),
        pytest.param("-40", -40.0, id="at-lower-bound"),
        pytest.param("0.0", 0.0, id="zero"),
    ],
)
def test_temperature_accepts(value: str, expected: float) -> None:
    assert validate_temperature(value) == expected


@pytest.mark.parametrize(
    "value, expected_error",
    [
        ("-40.1", TemperatureOutOfRangeError),
        ("150.1", TemperatureOutOfRangeError),
        ("inf", TemperatureOutOfRangeError),
        ("ERR", TemperatureNotANumberError),
        ("", TemperatureNotANumberError),
        ("nan", TemperatureWasNaNError),
    ],
)
def test_temperature_rejects(
    value: str, expected_error: type[TelemetryException]
) -> None:
    with pytest.raises(expected_error):
        validate_temperature(value)
