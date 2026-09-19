from pathlib import Path

import pytest

from telemetry_boss_fight.parser import parse_header


@pytest.fixture
def sample_telemetry_path() -> Path:
    cur_dir = Path(__file__).resolve().parent
    data_dir = cur_dir / ".." / "data"
    sample_telemetry_path = data_dir / "sample_telemetry.csv"
    return sample_telemetry_path


@pytest.fixture
def sample_header() -> str:
    return "timestamp,robot_id,velocity,battery,temperature"


@pytest.fixture
def sample_header_parts(sample_header) -> list[str]:
    return parse_header(sample_header)


@pytest.fixture
def sample_known_header_values() -> set[str]:
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
