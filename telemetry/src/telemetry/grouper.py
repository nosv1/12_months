from telemetry.parser import ParsedLine


def group_robots_as_parsed_lines(
    parsed_lines: list[ParsedLine],
) -> dict[str, list[ParsedLine]]:
    parsed_robots_dict: dict[str, list[ParsedLine]] = {}
    for parsed_line in parsed_lines:
        if parsed_line.robot_id not in parsed_robots_dict:
            parsed_robots_dict[parsed_line.robot_id] = []
        parsed_robots_dict[parsed_line.robot_id].append(parsed_line)
    return parsed_robots_dict
