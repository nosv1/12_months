from pathlib import Path

from telemetry.reading import BadReading, Reading


class Robot:
    def __init__(self, id_: str):
        self.id_ = id_
        self.readings: list[Reading] = []
        self.bad_readings: list[BadReading] = []

    def plot(self, output_dir: Path):
        import matplotlib.pyplot as plt

        plt.plot([r.velocity for r in self.readings])
        plt.savefig(output_dir / "plot.png")
        plt.show()
