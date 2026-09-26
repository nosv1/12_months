import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_file(file_path: Path) -> list[str]:
    with file_path.open("r") as telemetry_file:
        telemetry_lines = telemetry_file.readlines()
        return telemetry_lines
