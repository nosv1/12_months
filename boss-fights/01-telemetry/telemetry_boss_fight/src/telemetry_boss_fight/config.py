# these are the known header values, not the known header order

from enum import Enum


class EXPECTED_HEADER_VALUES(str, Enum):
    TIMESTAMP = "timestamp"
    ROBOT_ID = "robot_id"
    VELOCITY = "velocity"
    BATTERY = "battery"
    TEMPERATURE = "temperature"
