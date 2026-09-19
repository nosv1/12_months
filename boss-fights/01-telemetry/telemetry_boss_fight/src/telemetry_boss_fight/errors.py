from __future__ import annotations


class TelemetryException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


##########           TEMPERATURE           ##########


class InconsistentHeaderError(TelemetryException):
    def __init__(
        self,
        expected_parts: list[str],
        actual_parts: list[str],
        missing: list[str],
        extra: list[str],
    ) -> None:
        super().__init__(
            f"The header was inconsistent with the expected header in config.py "
            f"\n\tconfig: {expected_parts}"
            f"\n\tactual: {actual_parts}"
            f"\n\tmissing: {missing}"
            f"\n\textra: {extra}"
        )


##########           LINE           ##########


class RowColumnCountError(TelemetryException):
    def __init__(self, expected: int, actual: int) -> None:
        super().__init__(
            f"The number of columns in the data row did not match the number of header values - Expected: {expected}, Actual: {actual}"
        )


##########           TEMPERATURE           ##########


class TemperatureIsNotNumberError(TelemetryException):
    def __init__(self, value_str: str) -> None:
        super().__init__(f"Temperature value is not a number - {value_str}")
