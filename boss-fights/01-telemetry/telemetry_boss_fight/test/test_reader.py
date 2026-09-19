from pathlib import Path

import pytest
from telemetry_boss_fight.reader import read_file


def test_read_file_accepts(sample_telemetry_path: Path) -> list[str]:
    assert read_file(sample_telemetry_path) is list
