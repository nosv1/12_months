from __future__ import annotations

from dataclasses import dataclass

from telemetry.robot import Robot
from telemetry.warning import Warning


@dataclass
class Analysis:
    # *Output:* average velocity, max temperature, min battery, warnings
    __average_velocity: float = 0.0
    __max_temperature: float = -float("inf")
    __min_battery: float = float("inf")
    __warnings: list[str] = []

    def analyze_robot(robot: Robot, defined_warnings: list[Warning]) -> Analysis:
        analysis = Analysis()
        sum_velocities: float = 0
        for r in robot.readings:
            sum_velocities += r.velocity
            analysis.__max_temperature = max(analysis.__max_temperature, r.temperature)
            analysis.__min_battery = min(analysis.__min_battery, r.battery)

            for warning in defined_warnings:
                warning_msg = warning.detect_warning(r)
                if warning_msg:
                    analysis.__warnings.append(warning_msg)

        analysis.__average_velocity = sum_velocities / len(robot.readings)

        return analysis

    def to_json(self):
        return self.__dict__
