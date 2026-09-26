from __future__ import annotations

from dataclasses import dataclass, field

from telemetry.reading import BadReading
from telemetry.robot import Robot
from telemetry.telemetry_warning import TelemetryWarning


@dataclass
class RobotAnalysis:
    # *Output:* average velocity, max temperature, min battery, warnings
    average_velocity: float | None = None
    max_temperature: float | None = None
    min_battery: float | None = None
    warnings: list[str] = field(default_factory=list)
    bad_readings: list[BadReading] = field(default_factory=list)

    def to_json(self):
        return {
            "average_velocity": self.average_velocity,
            "max_temperature": self.max_temperature,
            "min_battery": self.min_battery,
            "warnings": self.warnings,
            "bad_readings": [br.to_json() for br in self.bad_readings],
        }


@dataclass
class Analysis:
    robot_analyses: dict[str, RobotAnalysis] = field(default_factory=dict)
    bad_readings: list[BadReading] = field(default_factory=list)


def analyze_robot(
    robot: Robot, defined_warnings: list[TelemetryWarning]
) -> RobotAnalysis:
    robot_analysis = RobotAnalysis()
    robot_analysis.bad_readings = robot.bad_readings
    sum_velocities: float = 0

    if not robot.readings:
        return robot_analysis

    running_max_temp = float("-inf")
    running_min_battery = float("inf")
    for r in robot.readings:
        sum_velocities += r.velocity
        running_max_temp = max(r.temperature, running_max_temp)
        running_min_battery = min(r.battery, running_min_battery)

        for warning in defined_warnings:
            warning_msg = warning.detect_warning(r)
            if warning_msg:
                robot_analysis.warnings.append(f"{warning_msg}")

    robot_analysis.max_temperature = running_max_temp
    robot_analysis.min_battery = running_min_battery
    robot_analysis.average_velocity = sum_velocities / len(robot.readings)

    return robot_analysis


def analyze_robots(
    robots_dict: dict[str, Robot],
    defined_warnings: list[TelemetryWarning],
) -> dict[str, RobotAnalysis]:
    return {r_id: analyze_robot(r, defined_warnings) for r_id, r in robots_dict.items()}
