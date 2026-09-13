import pytest

from telemetry.analysis import Analysis
from telemetry.reading import Reading
from telemetry.robot import Robot
from telemetry.validator import validate_velocity


def test_zero_velocity_line():
    assert validate_velocity("0.0") == 0.0


def test_nan_velocity():
    with pytest.raises(ValueError):
        validate_velocity("nan")
