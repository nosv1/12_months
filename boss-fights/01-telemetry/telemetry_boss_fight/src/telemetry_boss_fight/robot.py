from __future__ import annotations

from telemetry_boss_fight.accepted_reading import AcceptedReading
from telemetry_boss_fight.errors import TelemetryException
from telemetry_boss_fight.rejected_reading import RejectedReading


class Robot:
    def __init__(
        self,
        robot_id: str,
        accepted_readings: list[AcceptedReading],
        rejected_readings: list[RejectedReading],
    ):
        self.robot_id = robot_id
        self.accepted_readings = accepted_readings
        self.rejected_readings = rejected_readings

    def reject_accepted_reading(
        self, line_number, original_line, error: TelemetryException
    ) -> None:
        self.accepted_readings.pop()
        self.rejected_readings.append(
            RejectedReading(line_number, original_line, [error])
        )
