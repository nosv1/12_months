import json
from pathlib import Path

from telemetry.analysis import Analysis


def build_report(analysis: Analysis) -> dict:
    output_json = {
        "robots": {
            r_id: robot_analysis.to_json()
            for r_id, robot_analysis in analysis.robot_analyses.items()
        },
        "bad_readings": [br.to_json() for br in analysis.bad_readings],
    }
    return output_json


def dump_analysis(analysis: Analysis, output_dir: Path) -> None:
    report = build_report(analysis)

    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "output.json").open("w") as output:
        json.dump(report, output, indent=4)
