from pathlib import Path

from telemetry_boss_fight.config import DEFINED_WARNINGS
from telemetry_boss_fight.pipeline import pipeline
from telemetry_boss_fight.report import dump_report, generate_report, print_report


def main(telemetry_path: Path) -> None:
    robots, rejected_readings = pipeline(telemetry_path)
    report = generate_report(robots, rejected_readings, DEFINED_WARNINGS)
    print_report(report)
    # dump_report(Path(__file__).resolve().parent, report)
