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
        self.timestamp: datetime = timestamp
        self.velocity: float = velocity  # m/s
        self.battery: float = battery  # percent of charge, 0–100
        self.temperature: float = temperature  # °C, motor controller
