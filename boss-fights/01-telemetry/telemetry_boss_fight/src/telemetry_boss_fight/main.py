from pathlib import Path

from telemetry_boss_fight.pipeline import pipeline


def main(telemetry_path: Path) -> None:
    pipeline(telemetry_path)
