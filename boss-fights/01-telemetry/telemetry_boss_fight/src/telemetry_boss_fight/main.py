from pathlib import Path

from telemetry_boss_fight.reader import read_telemetry_lines


def main(telemetry_path: Path) -> None:
    telemetry_lines = read_telemetry_lines(telemetry_path)
    parsed_telemetry_lines = parse_telemetry_lines(telemetry_lines)
