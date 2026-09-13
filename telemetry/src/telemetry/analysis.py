from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from telemetry.reading import BadReading
from telemetry.robot import Robot
from telemetry.telemetry_warning import TelemetryWarning


@dataclass
class Analysis:
    # *Output:* average velocity, max temperature, min battery, warnings
    average_velocity: Optional[float] = 0.0
    max_temperature: float = -float("inf")
    min_battery: float = float("inf")
    warnings: list[str] = field(default_factory=list)
    bad_readings: list[BadReading] = field(default_factory=list)

    @staticmethod
    def analyze_robot(
        robot: Robot, defined_warnings: list[TelemetryWarning]
    ) -> Analysis:
        analysis = Analysis()
        analysis.bad_readings = robot.bad_readings
        sum_velocities: float = 0
        for r in robot.readings:
            sum_velocities += r.velocity
            analysis.max_temperature = max(analysis.max_temperature, r.temperature)
            analysis.min_battery = min(analysis.min_battery, r.battery)

            for warning in defined_warnings:
                warning_msg = warning.detect_warning(r)
                if warning_msg:
                    analysis.warnings.append(f"{warning_msg}")

        analysis.average_velocity = (
            (sum_velocities / len(robot.readings)) if robot.readings else None
        )

        return analysis

    def to_json(self):
        return {
            "average_velocity": self.average_velocity,
            "max_temperature": self.max_temperature,
            "min_battery": self.min_battery,
            "warnings": self.warnings,
            "bad_readings": [
                {
                    "line_number": br.line_number,
                    "line": br.unparsed_string,
                    "error": br.err,
                }
                for br in self.bad_readings
            ],
        }
