# Deliverable — Telemetry Toolkit

A command-line robot telemetry analyzer, as a real repository.

*Input:* `timestamp`, `robot_id`, `velocity`, `battery`, `temperature`
*Output:* average velocity, max temperature, min battery, warnings

`raw data → parser → validation → analysis → report`

Must have: clean module boundaries, tests, a CLI, a README someone else could follow, an example
dataset, and CI that runs the tests on push.

## Input data

See [data/sample_telemetry.csv](data/sample_telemetry.csv).

Here's a two-minute log dump from three of our mobile robots (`amr-01`, `amr-02`, `amr-03`). They
log at roughly 1 Hz and all write to the same file, so the robots' rows are mixed together. It's
what our loggers actually produce, and they aren't perfect.

- **timestamp**: ISO 8601, UTC (`2026-09-03T14:00:00.016Z`)
- **velocity**: m/s
- **battery**: percent of charge, 0–100
- **temperature**: °C, motor controller
- **Warn us when** a robot's battery drops below 20% or its temperature goes above 60 °C.

That's 361 data rows plus a header.

## Design

### `Reading`

- timestamp: datetime # ISO 8601, UTC (`2026-09-03T14:00:00.016Z`)
- velocity: float # m/s
- battery: float # 0-100
- temperature: float # °C
- warning_msgs: list[str] # populated when Robot.detect_warnings detects a warning

validate_reading(reading) -> Optional[str]

parse_line(line) -> Reading | str

### Warning

type holder for various warnings

### BatteryWarning(Warning)

- min_battery
- max_battery

detect_warning(reading) -> str

### `Robot`

- readings: list[Reading]
- error_messages: list[str]
- warnings: list[Warning]

```python
detect_warnings(reading)
    for w in warnings:
        warning_msg = w.detect_warning(reading)
        if warning_msg:
            r.warning_msgs.append(warning_msg)
```

### `validator(line, prev robot line) -> str`

Validate each value in the line as well as validate timestamp order.
If erroneous values, return the error message and the raw line.

### `parser(telemetry_file, defined_warnings) -> robots dict`

Returns `{robot_id: Robot, ...}`.

- Loop telemetry file, adding to robots dict as unique robot ids are found.
- Update Robot with defined warnings
- Send line to Reading class to get parsed
- Send reading to `validator(reading, prev_reading)` — where prev reading is the current robot's prev
  line.
- If the line isn't validated, add the line to `Robot.bad_readings`, otherwise detect warnings via `Robot.detect_warnings` and then add the reading to  `Robot.readings`.

### `Analysis(robot) -> dict`

- average_velocity: float = 0
- max_velcoity: float = -float('inf')
- min_velocity: float = float('inf')
- warnings: list[str] = []

```python
sum_velocity = 0
analysis = Analysis()

for r in robot.readings:
    sum_velocity += r.velocity
    analysis.max_temperature = max(analysis.max_temperature, r.temperature)
    analysis.min_temperature = min(analysis.min_temperature, r.temperature)
    warnings += [w for w in r.warning_msgs]
analysis.average_velocity = sum_velocity / len(robot.readings)
return analysis.__dict__
```

*Output:* average velocity, max temperature, min battery, warnings

### `report(robot_analyses(?)) -> None`

Dumps file analysis dicts to file, all robots in one file.

### `main.py`

```python
defined_warnings = [BatteryWarning(min, max)] # good enough for now, ideally this would be in a config file of sorts
argv = sys.argv[1] # to get path of telemetry file, probably going to assume users are perfect at sending paths for this project
robots_dict = parser(telemetry_file, defined_warnings)
analysis_dict = {r_id: analysis(r) for r_id, r in robots_dict.items()}  # not sure if this works
report(analysis_dict)
```
