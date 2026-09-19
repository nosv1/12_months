from __future__ import annotations


class TelemetryException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InconsistentHeaderError(TelemetryException):
    def __init__(
        self,
        expected_parts: list[str],
        actual_parts: str,
        missing: list[str],
        extra: list[str],
    ):
        super().__init__(
            f"The header was inconsistent with the expected header in config.py "
            f"\n\tconfig: {expected_parts}"
            f"\n\tactual: {actual_parts}"
            f"\n\tmissing: {missing}"
            f"\n\textra: {extra}"
        )


class RowColumnCountError(TelemetryException):
    def __init__(self, expected: int, actual: int):
        super().__init__(
            f"The number of columns in the data row did not match the number of header values - Expected: {expected}, Actual: {actual}"
        )
