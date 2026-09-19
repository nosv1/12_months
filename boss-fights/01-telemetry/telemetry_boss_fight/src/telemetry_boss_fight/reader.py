from pathlib import Path


def read_telemetry_file(telemetry_path: Path) -> list[str]:
    with open(telemetry_path, "r") as tf:
        return tf.readlines()
