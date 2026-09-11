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
