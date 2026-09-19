from pathlib import Path

import pytest


@pytest.fixture
def sample_telemetry_path() -> Path:
    cur_dir = Path(__file__).resolve().parent
    data_dir = cur_dir / ".." / "data"
    sample_telemetry_path = data_dir / "sample_telemetry.csv"
    return sample_telemetry_path
