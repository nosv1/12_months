from pathlib import Path


def read_telemetry_lines(telemetry_path: Path) -> list[str]:
    with open(telemetry_path, "r") as tf:
        return tf.readlines()
