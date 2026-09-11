from telemetry.analysis import Analysis
from telemetry.reading import Reading
from telemetry.robot import Robot
from telemetry.validator import Validator


def test_zero_velocity_line():
    validator, value = Validator.validate_velocity("0.0")
    assert validator.is_valid
