from __future__ import annotations

from datetime import datetime

from telemetry.exceptions import TelemetryException


class Reading:
    def __init__(
        self,
        line_number: int,
        robot_id: str,
        timestamp: datetime,
        velocity: float,
        battery: float,
        temperature: float,
    ):
        self.line_number = line_number
        self.robot_id = robot_id
        self.timestamp = timestamp
        self.velocity = velocity  # m/s
        self.battery = battery  # percent of charge, 0–100
        self.temperature = temperature  # °C, motor controller


class BadReading:
    def __init__(
        self,
        line_number: int,
        unparsed_string: str,
        exceptions: list[TelemetryException],
    ):
        self.line_number = line_number
        self.unparsed_string = unparsed_string
        self.exceptions = exceptions

    def to_json(self):
        return {
            "line_number": self.line_number,
            "line": self.unparsed_string,
            "exceptions": [
                {"exception": e.__class__.__name__, "error": str(e)}
                for e in self.exceptions
            ],
        }
