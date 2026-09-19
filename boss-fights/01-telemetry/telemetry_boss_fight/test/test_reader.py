from pathlib import Path

from telemetry_boss_fight.reader import read_telemetry_file


def test_read_file_accepts(sample_telemetry_path: Path) -> list[str]:
    assert type(read_telemetry_file(sample_telemetry_path)) is list
