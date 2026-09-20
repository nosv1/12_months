# - **Battery below 20%** — it did not get back to the charger in time.
# - **Temperature above 60 °C** — the motor controller is running hot.

# A warning must tell us **which robot** and **the timestamp of the reading that triggered it**, so we can line it up against the aisle schedule.

from datetime import datetime


class TelemetryWarning:
    def __init__(
        self,
        field: str,
        units: str,
        min_value: float | None = None,
        max_value: float | None = None,
    ):
        self.field = field
        self.units = units
        self.min_value = min_value
        self.max_value = max_value

    def trigger_min_warning(self, value: float) -> bool:
        if self.min_value is None:
            return False

        return value < self.min_value

    def trigger_max_warning(self, value: float) -> bool:
        if self.max_value is None:
            return False

        return value > self.max_value

    def trigger_warning(
        self, robot_id: str, timestamp: datetime, value: float
    ) -> str | None:
        prefix = f"{robot_id} at {timestamp} had a {self.field} reading"
        warn = False
        if self.trigger_min_warning(value):
            warn = True
            direction = "below"

        elif self.trigger_max_warning(value):
            warn = True
            direction = "above"

        if warn:
            return f"{prefix} value {direction} {self.min_value if direction == 'below' else self.max_value}{self.units} -- {value}{self.units}"

        return None


class BatteryWarning(TelemetryWarning):
    def __init__(
        self,
        field: str,
        units: str,
        min_value: float | None = None,
        max_value: float | None = None,
    ):
        super().__init__(field, units, min_value, max_value)


class TemperatureWarning(TelemetryWarning):
    def __init__(
        self,
        field: str,
        units: str,
        min_value: float | None = None,
        max_value: float | None = None,
    ):
        super().__init__(field, units, min_value, max_value)
