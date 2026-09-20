# Machine-readable output (JSON is fine)
# The report needs, per robot: its warnings, and its rejected rows. Plus the rejected rows that couldn't be attributed to any robot, and the unrecognized-failure count.

# If the tool hits a failure it doesn't have a category for, put it in an **unrecognized** bucket with a count, and ____report that count every time_____ — it should always be zero.
# **Quarantine the row, don't crash.** A

import json
from pathlib import Path

from telemetry_boss_fight.errors import UnknownError
from telemetry_boss_fight.rejected_reading import RejectedReading
from telemetry_boss_fight.robot import Robot
from telemetry_boss_fight.telemetry_warnings import TelemetryWarning


def dump_report(output_dir: Path, report: dict) -> None:
    with open(output_dir / "report.json", "w") as f:
        json.dump(report, f, indent=4)


def print_report(report: dict) -> None:
    print(json.dumps(report, indent=4))


def generate_report(
    robots: dict[str, Robot],
    rejected_readings: list[RejectedReading],
    defined_warnings: list[TelemetryWarning],
) -> dict:
    # {robots: [robot: {warnings: [], rejected_readings: []}], rejected_readings: [], unrecognized_failures: 0}
    report: dict = {
        "robots": [{r.robot_id: r.to_json(defined_warnings) for r in robots.values()}],
        "rejected_readings": [rr.to_json() for rr in rejected_readings],
        "unrecognized_failures": 0,
    }

    def count_unrecognized_failures(rejected_readings: list[RejectedReading]):
        unrecognized_failures = 0
        for rejected_reading in rejected_readings:
            for error in rejected_reading.errors:
                if isinstance(error, UnknownError):
                    unrecognized_failures += 1
        return unrecognized_failures

    for robot in robots.values():
        report["unrecognized_failures"] += count_unrecognized_failures(
            robot.rejected_readings
        )
    report["unrecognized_failures"] += count_unrecognized_failures(rejected_readings)

    return report
