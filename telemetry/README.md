# Telemetry Toolkit

A toy problem: import a telemetry CSV file, then parse, validate, analyze, and report on that data.

| | |
| --- | --- |
| **Input** | `timestamp`, `robot_id`, `velocity`, `battery`, `temperature` |
| **Output** | average velocity, max temperature, min battery, warnings |

---

## Setup and running

Requires [uv](https://docs.astral.sh/uv/) — it handles Python for you.

```bash
cd telemetry
uv sync                  # optional — `uv run` syncs automatically

# uv run telemetry <telemetry_path> <output_dir>
uv run telemetry data/sample_telemetry.csv output
```

---

## Input format

See [data/sample_telemetry.csv](data/sample_telemetry.csv) for a two-minute log dump from three of
our mobile robots (`amr-01`, `amr-02`, `amr-03`). That's 361 data rows plus a header.

The robots log at roughly 1 Hz and all write to the same file, so their rows are mixed together.
It's what our loggers actually produce, and they aren't perfect.

| Column | Units / format |
| --- | --- |
| `timestamp` | ISO 8601, UTC (`2026-09-03T14:00:00.016Z`) |
| `robot_id` | e.g. `amr-01` |
| `velocity` | m/s [-2.0, 2.0] |
| `battery` | percent of charge, [0, 100] |
| `temperature` | °C, motor controller [-40, 150] |

> **Warn us when** a robot's battery drops below 20% or its temperature goes above 60 °C.

---

## Architecture

```text
raw data → parser → validation → analysis → report
```

| Stage | Responsibility |
| --- | --- |
| **Raw data** | The CSV telemetry data: timestamp (ISO 8601), velocity (m/s), battery (percent of charge, 0–100), and temperature (°C, motor controller). |
| **Parser** | Reads the data file line by line, passing each of the line's data points to their appropriate validation checks. |
| **Validation** | Validates the inputs. Timestamps should be after the robot's previous timestamp, floats should be in range and not NaN, etc. |
| **Analysis** | Analyzes the robot's readings, capturing average velocity, max temperature, min battery, and warnings. Bad readings are recorded as well. |
| **Report** | A JSON output of the analysis, written to an output directory. |

---

## Design decisions

### Detect warnings in analysis, not the parser

Given the data comes from a file (**not live**), warnings can be detected during analysis rather
than during parsing. The parser's duty remains simply to observe the facts of the file. If we
wanted to be warned during data handling, we could develop a handler to "do things with this valid
data."

### Raise errors in validation — don't judge validity by the returned value

One could imagine the returned value being the tell for whether it passed validation, but some
valid values are **falsy**. The encountered case was a velocity of `0.0`: Python treats `0` as
`False`, but `0` is also a valid velocity (a parked robot).

### Missing telemetry data goes to an `unknown` robot

When a reading doesn't come with all the expected data points, it's unsafe to assume the robot id
is in the line at all — and even less safe to assume it's at the correct index. So the reading is
considered bad and appended to an `unknown` robot in `robots_dict`.

---

## Lessons

1. **`main` is still the conductor**, even though the report needs everything run first.

   Early on, "report" felt like the final product, so it seemed natural to put `main()` in
   `report.py` and have it call everything else. Instead, `main()` lives in `cli.py` and
   orchestrates the calls:

   ```text
   main → parser → validator → main → analyzer → main → report
   ```
