from pathlib import Path

from telemetry_boss_fight.grouper import group_parsed_lines_by_robot
from telemetry_boss_fight.parser import parse_telemetry_lines, validate_parsed_robots
from telemetry_boss_fight.reader import read_telemetry_file
from telemetry_boss_fight.robot import Robot


def pipeline(telemetry_path: Path) -> dict[str, Robot]:
    telemetry_lines = read_telemetry_file(telemetry_path)
    parsed_lines, _rejected_readings = parse_telemetry_lines(telemetry_lines)
    parsed_robots = group_parsed_lines_by_robot(parsed_lines)
    _robots = validate_parsed_robots(parsed_robots)
    return {}
