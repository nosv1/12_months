from telemetry.reading import Reading


class Robot:
    def __init__(self, id_: str):
        self.id_ = id_
        self.readings: list[Reading] = []
        self.bad_readings: list[list[Reading, list[str]]] = []
