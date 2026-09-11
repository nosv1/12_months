from datetime import datetime


class Reading:
    def __init__(
        self, timestamp: datetime, velocity: float, battery: float, temperature: float
    ):
        self.timestamp: datetime = (
            timestamp  # ISO 8601, UTC (`2026-09-03T14:00:00.016Z`)
        )
        self.velocity: float = velocity  # m/s
        self.battery: float = battery  # percent of charge, 0–100
        self.temperature: float = temperature  # °C, motor controller
