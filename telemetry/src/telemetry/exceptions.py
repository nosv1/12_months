from datetime import datetime

# timestamp,robot_id,velocity,battery,temperature


class TelemetryException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class UnknownError(TelemetryException):
    def __init__(self, *args):
        super().__init__(*args)


class NotANumberError(TelemetryException):
    def __init__(self, field: str, cause: str):
        super().__init__(f"{field} was not number. - {cause}")


class NaNError(TelemetryException):
    def __init__(self, field: str, cause: str):
        super().__init__(f"{field} was nan. - {cause}")


###### EXCEPTIONS FOR INDIVIDUAL LINES   ######


class ColumnCountError(TelemetryException):
    def __init__(self):
        super().__init__("Data was missing from the input.")


######   EXCEPTIONS FOR INDIVIDUAL FIELDS   ######


###   TIMESTAMP   ###
class TimestampOutOfOrderError(TelemetryException):
    def __init__(self, timestamp: datetime, prev_timestamp: datetime):
        super().__init__(
            f"The timestamp is earlier in time than the robot's previous timestamp - {timestamp} <= {prev_timestamp}"
        )


class TimestampIdenticalError(TelemetryException):
    def __init__(self, timestamp: datetime):
        super().__init__(
            f"The timestamp matches the robot's previous timestamp - {timestamp}"
        )


class TimestampFormatError(TelemetryException):
    def __init__(self, timestamp_str: str):
        super().__init__(
            f"The timestamp format does not match ISO 8601, UTC - {timestamp_str}"
        )


###   VELOCITY   ###
class VelocityNotANumberError(NotANumberError):
    def __init__(self, cause: str):
        super().__init__(field="Velocity", cause=cause)


class VelocityWasNaNError(NaNError):
    def __init__(self, cause: str):
        super().__init__(field="Velocity", cause=cause)


class VelocityOutOfRangeError(TelemetryException):
    def __init__(self, cause: str):
        super().__init__(f"The velocity was out of the specified range - {cause}")


###   BATTERY   ###
class BatteryNotANumberError(NotANumberError):
    def __init__(self, cause: str):
        super().__init__(field="Battery", cause=cause)


class BatteryWasNaNError(NaNError):
    def __init__(self, cause: str):
        super().__init__(field="Battery", cause=cause)


class BatteryOutOfRangeError(TelemetryException):
    def __init__(self, cause: str):
        super().__init__(f"Battery was out of the specified range - {cause}.")


###   TEMPERATURE   ###
class TemperatureNotANumberError(NotANumberError):
    def __init__(self, cause: str):
        super().__init__(field="Temperature", cause=cause)


class TemperatureWasNaNError(NaNError):
    def __init__(self, cause: str):
        super().__init__(field="Temperature", cause=cause)


class TemperatureOutOfRangeError(TelemetryException):
    def __init__(self, cause: str):
        super().__init__(f"Temperature was out of the specified range - {cause}.")
