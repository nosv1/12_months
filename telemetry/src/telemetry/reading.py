from __future__ import annotations

from datetime import datetime


class Reading:
    def __init__(
        self,
        robot_id: str,
        timestamp: datetime,
        velocity: float,
        battery: float,
        temperature: float,
    ):
        self.robot_id = robot_id
        self.timestamp = timestamp
        self.velocity = velocity  # m/s
        self.battery = battery  # percent of charge, 0–100
        self.temperature = temperature  # °C, motor controller


class BadReading:
    def __init__(self, line_number: int, unparsed_string: str, exception: Exception):
        self.line_number = line_number
        self.unparsed_string = unparsed_string
        self.exception = exception

    def to_json(self):
        return {
            "line_number": self.line_number,
            "line": self.unparsed_string,
            "exception": self.exception.__class__.__name__,
            "error": str(self.exception),
        }
