# TELEMETRY TOOLKIT

The telemety toolkit is a toy problem involving importing a telemetry csv vile then parsing, validating, analyzing, and reporting on that data.

*Input:* `timestamp`, `robot_id`, `velocity`, `battery`, `temperature`
*Output:* average velocity, max temperature, min battery, warnings

Must have: clean module boundaries, tests, a CLI, a README someone else could follow, an example dataset, and CI that runs the tests on push.

## SETUP AND RUNNING

```bash
# install uv (it'll handle python)
cd telemetry
uv sync # optional (`uv run` syncs)
# uv run telemetry <telemetry_path> <output_dir>
uv run telemetry data/sample_telemetry.csv output
```

## INPUT FORMAT

See [data/sample_telemetry.csv](data/sample_telemetry.csv) for a two-minute log dump from three of our mobile robots (`amr-01`, `amr-02`, `amr-03`). They log at roughly 1 Hz and all write to the same file, so the robots' rows are mixed together. It's what our loggers actually produce, and they aren't perfect.

- **timestamp**: ISO 8601, UTC (`2026-09-03T14:00:00.016Z`)
- **velocity**: m/s
- **battery**: percent of charge, 0–100
- **temperature**: °C, motor controller
- **Warn us when** a robot's battery drops below 20% or its temperature goes above 60 °C.

That's 361 data rows plus a header.

## ARCHITECTURE

`raw data → parser → validation → analysis → report`

### Raw data

The csv telemetry data with inputs for timestamp (ISO 8601), velocity (m/s), battery (percent of charge, 0–100) and temperature (°C, motor controller)

### Parser

Reads the data file line by line - passing the each of the line's data points to their appropriate validation checks.

### Validation

Validate the inputs. Timestamps should be in the future. Floats should be in range and not nan.

### Analysis

Analyze the robot's readings - capturing average velocity, max temperature, min battery, warnings. Additionally, bad readings are recorded as well.

### Report

A JSON output of analysis to an output directory.

## DESIGN DECISIONS

### Document warnings in analysis, not the parser

Given the data is from a file (AND NOT LIVE) the warnings can be detected during analysis and not during parsing. The parser's duty remains simply to observe the facts of the file. If we wanted to be warned during data handling, we may develop a handler to "do things with this valid data."

### Raise errors in validation, not the parser

Similar to above and keeping the parser simple. It's not the parser's job to detect errors or shout when there is one. The parser reads a line, hands it to the validator, and then the validator either raises an error or returns a valid value. The parser does handle the valid and erroneous Readings.

### Drop and record bad rows; don't treat them as fatal

## LESSONS
