from telemetry_boss_fight.config import KNOWN_HEADER_VALUES
from telemetry_boss_fight.errors import InconsistentHeaderError, RowColumnCountError

##########           LINE           ##########


def validate_header_parts(header_parts: list[str]) -> list[str]:
    missing_parts: list[str] = []
    extra_parts: list[str] = []

    for header_field in header_parts:
        if header_field not in KNOWN_HEADER_VALUES:
            extra_parts.append(header_field)

    unique_header_parts = set(header_parts)
    for known_header_value in KNOWN_HEADER_VALUES:
        if known_header_value not in unique_header_parts:
            missing_parts.append(known_header_value)

    if missing_parts != [] or extra_parts != []:
        raise InconsistentHeaderError(
            expected_parts=list(KNOWN_HEADER_VALUES),
            actual_parts=header_parts,
            missing=missing_parts,
            extra=extra_parts,
        )

    return header_parts


def validate_line_parts(
    line_parts: list[str], header_parts: list[str]
) -> dict[str, str]:
    if len(line_parts) != len(header_parts):
        raise RowColumnCountError(len(header_parts), len(line_parts))
    return line_parts
