from datetime import datetime, timezone

import pytest

from telemetry.exceptions import (
    BatteryNotANumberError,
    BatteryOutOfRangeError,
    BatteryWasNaNError,
    ColumnCountError,
    TemperatureNotANumberError,
    TemperatureOutOfRangeError,
    TemperatureWasNaNError,
    TimestampFormatError,
    VelocityNotANumberError,
    VelocityOutOfRangeError,
    VelocityWasNaNError,
)
from telemetry.parser import parse_line
from telemetry.validator import (
    validate_battery,
    validate_temperature,
    validate_timestamp_format,
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
def test_timestamp_format_accepts(value) -> None:
    assert validate_timestamp_format(value) == datetime(
        2026, 9, 3, 14, 0, 0, 16000, tzinfo=timezone.utc
    )


@pytest.mark.parametrize(
    "value, expected_error", [("2060903T14:00:00.016Z", TimestampFormatError)]
)
def test_timestamp_format_rejects(value, expected_error) -> None:
    with pytest.raises(expected_error):
        validate_timestamp_format(value)


###   VELOCITY   ###


@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param("2.0", 2.0, id="at-upper-bound"),
        pytest.param("-2.0", -2.0, id="at-lower-bound"),
        pytest.param("0.0", 0.0, id="zero"),
    ],
)
def test_velocity_accepts(value, expected) -> None:
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
def test_velocity_rejects(value, expected_error) -> None:
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
def test_battery_accepts(value, expected) -> None:
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
def test_battery_rejects(value, expected_error) -> None:
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
def test_temperature_accepts(value, expected) -> None:
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
def test_temperature_rejects(value, expected_error) -> None:
    with pytest.raises(expected_error):
        validate_temperature(value)
