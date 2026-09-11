import os
import sys
from typing import TextIO

from telemetry.analysis import Analysis
from telemetry.reading import Reading
from telemetry.robot import Robot


def parser(telemetry_file: TextIO) -> dict[str, Robot]:
    pass


if __name__ == "__main__":
    telemetry_file = sys.argv[1]  ## python main.py <telemetry_path>
    with open(telemetry_file, "r"):
        robots_dict = parser(telemetry_file)
        analysis_dict = {r_id: Ana for r_id, r in robots_dict}
