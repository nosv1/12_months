import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_telemetry_file(telemetry_path: Path) -> list[str]:
    logger.info("Reading %s...", str(telemetry_path))
    with open(telemetry_path, "r") as tf:
        return tf.readlines()
