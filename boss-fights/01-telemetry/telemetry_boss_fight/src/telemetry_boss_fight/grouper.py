from telemetry_boss_fight.config import EXPECTED_HEADER_VALUES
from telemetry_boss_fight.parser import ParsedLine


def group_parsed_lines_by_robot(
    parsed_lines: list[ParsedLine],
) -> dict[str, list[ParsedLine]]:
    parsed_robots: dict[str, list[ParsedLine]] = {}
    for parsed_line in parsed_lines:
        robot_id = parsed_line.fields[EXPECTED_HEADER_VALUES.ROBOT_ID]
        if robot_id not in parsed_robots:
            parsed_robots[robot_id] = []

        parsed_robots[robot_id].append(parsed_line)

    return parsed_robots
