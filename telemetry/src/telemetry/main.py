from pathlib import Path

from telemetry.pipeline import analyze_telemetry
from telemetry.reader import read_file
from telemetry.reporter import dump_analysis
from telemetry.telemetry_warning import BatteryWarning, TemperatureWarning


def main(telemetry_file_path: Path, output_dir: Path) -> None:
    defined_warnings = [
        BatteryWarning(min_battery=20),
        TemperatureWarning(max_temperature=60),
    ]
    telemetry_lines = read_file(telemetry_file_path)
    analysis = analyze_telemetry(telemetry_lines, defined_warnings)
    dump_analysis(analysis, output_dir)
