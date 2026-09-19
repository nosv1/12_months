from telemetry_boss_fight.grouper import group_parsed_lines_by_robot
from telemetry_boss_fight.parser import ParsedLine


def test_robots_found(
    sample_known_robot_ids: set[str], sample_parsed_lines: list[ParsedLine]
):
    parsed_robots = group_parsed_lines_by_robot(sample_parsed_lines)
    assert parsed_robots.keys() == sample_known_robot_ids
    assert len(sample_parsed_lines) == sum(
        len(lines) for lines in parsed_robots.values()
    )
