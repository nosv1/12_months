# Telemetry Toolkit

A toy problem: import a telemetry CSV file, then parse, validate, analyze, and report on that data.

| | |
| --- | --- |
| **Input** | `timestamp`, `robot_id`, `velocity`, `battery`, `temperature` |
| **Output** | average velocity, max temperature, min battery, warnings |

---

## Setup and running

Requires [uv](https://docs.astral.sh/uv/) — it handles Python for you.

### Scratch run

```bash
cd telemetry
uv sync                  # optional — `uv run` syncs automatically

# uv run telemetry <telemetry_path> <output_dir>
uv run telemetry data/sample_telemetry.csv output
```

### Testing

```bash
uv run pytest            # to only run pytest
```

To run ruff (with `--fix` to fix safe fixes), mypy, pytest, and the toolkit all in one shot, use
[debug.sh](debug.sh) — pauses for user "enter to continue" at each step.

### Shipping

```bash
# 1. Ship: from the directory holding pyproject.toml
uv tool install --reinstall .       # --reinstall: take a fresh snapshot even if one exists
uv tool list                        # confirm the name and version on the path

# 2. Test as the customer: somewhere else, no venv, command by name, absolute path in
cd ~
deactivate 2>/dev/null              # harmless if nothing was active
which telemetry                     # should be ~/.local/bin/<command>, not a .venv path
telemetry /abs/path/to/sample.csv <output_dir>
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

## Output format

The output is a in JSON formatted report saved in specified directory when running the command.

The report organizes each robot by robot id and reports their average velocities, maximum
temperatures, minimum battery levels, the warnings as they were triggered throughout, and any bad
readings due to improper values like temperature readings being out of range or a malformed
timestamp.

In addition, the JSON report includes a list of bad readings that were due to line-level errors —
errors like `ColumnCountError` where the columns in the line do not match the expected columns from
the headers.

```text
{
   "robots": {
      "<robot_id>": {
         "average_velocity": <float> | null,
         "max_temperature": <float> | null,
         "min_battery": <float> | null,
         "warnings": list[str],
         "bad_readings": [
            {
               "line_number": int,
               "line": str,
               "exceptions": [
                  {
                     "exception": str (error name),
                     "error": str (error message),
                  }, ...
               ]
            }, ...
         ]
      }, ...
   },
   "bad_readings": [
      {
         "line_number": int,
         "line": str,
         "exceptions": [
            {
               "exception": str (error name),
               "error": str (error message),
            }, ...
         ]
      }, ...
   ]
}
```

---

## Architecture

```text
raw data → parser → grouper → validation → analysis → report
```

| Stage | Responsibility |
| --- | --- |
| **Raw data** | The CSV telemetry data: timestamp (ISO 8601), velocity (m/s), battery (percent of charge, 0–100), and temperature (°C, motor controller). |
| **Parser** | Reads the data file line by line, passing each of the line's data points to their appropriate validation checks. |
| **Grouper** | Groups the parsed lines by robot id. |
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

---

## Lessons

1. **`main` is still the conductor**, even though the report needs everything run first.

   Early on, "report" felt like the final product, so it seemed natural to put `main()` in
   `report.py` and have it call everything else. Instead, `main()` now lives in `main.py` and is
   called by `cli.py` and orchestrates the calls:

   ```text
   main → analyze_telemetry() → parser → validator → analyzer → main → report
   ```

---

## What broke?

### Circular import

**Problem.** Parser outputs a list of `ParsedLine`s, but the parser also used to use functions
inside of validation to validate column count, for example; but, this means `validator.py` couldn't
be aware of the `ParsedLine` class, because **circular import** and `ParsedLine` lived inside the
parser (and omg that needs to be the solution — move `ParsedLine` to its own file...)

**Solution.** The acting solution was to pull any validation functions that parser was using to
`parser.py`. `validator.py` can now import `ParsedLine`, allowing type hints to exist without
circular import.

### Infinities in JSON

**Problem.** The analysis involves determining the max temperature and minimum battery. Issues
arise when a robot does not have any valid readings, but the analysis still tries to do math on
them. The seed infinites never go away and JSON received invalid formatted floats.

**Solution.** The solution was to seed the max/min locally in the aggregator, instead of at the
class attribute level.

> **Note:** it is possible for a robot to still exist with no valid readings as it can still have
> only bad readings — it doesn't get axed from the report and analysis for not having valid
> readings.

---

## Known issues / What's next?

- Based on the [telemetry requirements](../docs/telemetry-requirements.md), headers can be in any
  order, and there is currently not a "header handler" in the parser. The parser can know what
  headers to expect and attribute them appropriately.

- Readings can be renamed to accepted and rejected readings.

- Warnings and headers can be defined inside a `config.env` file to expose the fields with measured
  ranges as well as thresholds for the warnings.

- A count of the rejected reading errors not caught by the validator but still allowed the toolkit
  to run needs to be reported in the JSON report; the expectation is it is always 0, however it is
  possible a validator failed to cover new and unique errors.

- Reorganize the flow of data. As it stands:

  ```text
  cli -> main -> pipeline.analyze_telemetry() ...
  ```

  As it should be:

  ```text
  cli -> main -> pipeline -                 -> analyzer -> reporter
                          |  -> reader      |
                          |  -> parser      |
                          |  -> grouper     |
                          |  -> validator - |
  ```

  `main` calls the `pipeline`. The `pipeline` gathers the necessary data for what main wants to do
  (in this case, receive validated robots and bad readings), then main can send those `robots` and
  `bad_readings` to `analyzer` to receive an `Analysis`, then ship that `Analysis` to the reporter.

- A test needs to be created to judge the output vs expected. At the moment tests exist to validate
  single functions and their outputs, but nothing is checking to make sure the whole report is
  accurate.
