from telemetry.analysis import Analysis
from telemetry.reading import Reading
from telemetry.robot import Robot
from telemetry.validator import validate_velocity


def test_zero_velocity_line():
    try:
        value = validate_velocity("0.0")

    except ValueError as ve:
        assert str(ve) != ""

    assert value == 0.0
