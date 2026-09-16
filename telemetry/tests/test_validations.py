from pathlib import Path

import pytest

from telemetry.exceptions import VelocityWasNaNError
from telemetry.validator import validate_velocity


def test_zero_velocity_line():
    assert validate_velocity("0.0") == 0.0


def test_nan_velocity():
    with pytest.raises(VelocityWasNaNError):
        validate_velocity("nan")


def test_all_defects_caught():
    cur_dir = Path.cwd()
    telemetry_file_path: Path = cur_dir / "data/sample_telemetry.csv"
    output_dir: Path = cur_dir / "output"
    telemetry_main(telemetry_file_path, output_dir)
    # work in progress
    pass
