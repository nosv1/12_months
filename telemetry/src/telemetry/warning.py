from abc import ABC, abstractmethod
from typing import Optional

from telemetry.reading import Reading


class Warning(ABC):
    @abstractmethod
    def detect_warning(reading: Reading) -> Optional[str]:
        pass

    def handle_warning(warning: str, value: float, threshold: float)
        return f"WARNING: {warning}={value} (threshold={threshold})"


class BatteryWarning(Warning):
    def __init__(self, min_battery: float):
        self.min_battery = min_battery

    def detect_warning(self, reading: Reading) -> Optional[str]:
        if (reading.battery < self.min_battery):
            return self.handle_warning("LOW BATTERY", reading.battery, self.min_battery)
        return None


class TemperatureWarning(Warning):
    def __init__(self, max_temperature: float):
        self.max_temperature = max_temperature

    def detect_warning(self, reading: Reading) -> Optional[str]:
        if (reading.temperature < self.max_temperature):
            return self.handle_warning("HIGH TEMPERATURE", reading.temperature, self.max_temperature)
        return None
