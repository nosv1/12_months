from __future__ import annotations

from datetime import UTC, datetime

from telemetry_boss_fight.accepted_reading import AcceptedReading
from telemetry_boss_fight.config import EXPECTED_HEADERS
from telemetry_boss_fight.errors import TelemetryException
from telemetry_boss_fight.rejected_reading import RejectedReading
from telemetry_boss_fight.telemetry_warnings import TelemetryWarning


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

    def to_json(self, defined_warnings: list[TelemetryWarning]) -> dict:
        warnings: list[str] = []
        for reading in self.accepted_readings:
            for defined_warning in defined_warnings:
                timestamp = reading.fields[EXPECTED_HEADERS.TIMESTAMP.value.header]
                value = reading.fields[defined_warning.field]
                warning = defined_warning.trigger_warning(
                    robot_id=self.robot_id,
                    timestamp=(
                        timestamp
                        if isinstance(timestamp, datetime)
                        else datetime.now().astimezone(UTC)
                    ),
                    value=value if isinstance(value, float) else -1,
                )
                if warning is not None:
                    warnings.append(warning)

        return {
            "warnings": warnings,
            "rejected_readings": [rr.to_json() for rr in self.rejected_readings],
        }
