# Telemetry toolkit — design history, customer role, Boss Fight #1

Back to the [TA notes index](../ta-notes.md). Read when reviewing telemetry code, answering a
requirements question as the customer, or when Boss Fight #1 starts.

---

## Design, settled by him

- **`main`/`cli` orchestrates** (parse → analyze → report). His original blocker was picturing
  stages as separate programs passing files; in-process stages pass return values. Revisit at
  week 11 (ROS nodes *are* separate processes).
- **Bad rows dropped and recorded** on the `Robot` as `(line, message)`, fed into the report.
- **Warnings: Strategy pattern** in `telemetry_warning.py` (renamed from `Warning`, which shadowed
  the builtin), detected in `analysis.py`, carrying the reading's timestamp. Kept in analysis with
  a batch-vs-live rationale in the README.
- **Validation raises** `ValueError`; one error boundary per row. Came from the falsy-`0.0` bug
  (textbook 02).

## Week 2 redesign (2026-09-12, his)

```text
lines ─► ParsedLine.parse_line ─► validate_parsed_line(parsed, prev_reading) ─► Reading
         parser.py                validator.py
         raises MissingDataError  raises ValueError
         → "unknown" robot        → that robot's bad_readings
```

The loop (`parse_telemetry_lines(lines: Iterable[str], headers_count)`) is in `cli.py` "for now"
(`3aff0b7`) after a validator ↔ parser circular import (textbook 07). Imports now point one way.

Open in the design — **his decisions**, see index for the current list: where the loop lives and
what it's called; indexes in `ParsedLine` vs `main` vs reading the header row; hidden header-skip
rule; `readlines()` still loads the whole file; `report()` mixes JSON building with file I/O.

Minor, older: exceptions short-circuit, so `bad_readings` holds only the *first* reason per row —
never asked him to defend it; good test-design question. `robot.plot()` commented out, would
overwrite one `plot.png` per robot — WIP, don't review until he picks it up.

## Week 2 stages (2026-09-13, his, `b830018`)

```text
read_file ─► parse_lines ─► group_robots ─► per robot: validate_robot_timestamps
reader.py    parser.py      cli.py                     ─► validate_parsed_line_values ─► Robot
             rejects ─► top-level bad_readings in report     rejects ─► robot.bad_readings
```

Came from the naming problem (`reader.read_file` returning `dict[str, Robot]`), then the split.
Known issues he's aware of: order check before value check (double format parse, triple-reported
malformed timestamp, unchecked row as "previous"). Lesson written up in
[textbook 08](../textbook/08-pipeline-stages.md).

## I play the customer

I generated `telemetry/data/sample_telemetry.csv` (committed as Claude, `94b4543`) and gave a
customer-voice spec: ISO 8601 UTC, m/s, battery %, °C; **warn battery < 20%, temperature > 60 °C**.
I answer **requirements** questions in character — not design questions. **Answered 2026-09-13, rejected rows:** report needs (1) line number in the original file,
(2) reason in plain words, (3) the row exactly as it appeared, not rebuilt (for firmware tickets).
Group under the robot when known; unattributable rows listed separately, no invented robot.
`-Infinity` in the JSON breaks the customer's dashboard. Candidate requirements
questions he may raise: does a header always exist; can columns be reordered; should a swapped
pair flag both rows; are sub-zero temperatures valid (validator rejects `< 0`).

### Spoilers: the planted defects

*He reads these notes. As of week 1 his code catches all of these, so this is no longer secret in
practice — but the boss fight is a rebuild, so skim past if you want it cold.*

`nan` velocity, blank battery, battery `104.2`, temperature `-273.2`, two amr-03 rows swapped
(per-robot timestamp regression), one exact duplicate row, one truncated row (4 fields), velocity
`ERR`. By design: amr-02 battery drops to ~16%, amr-03 overheats to ~66 °C, amr-01 parks (v=0)
~12 s. Cross-robot timestamps interleave — normal.

Verified output (week 1 and again after the week-2 redesign): bad rows per robot
`{unknown: 1, amr-01: 2, amr-02: 2, amr-03: 3}` = all 8. The swapped pair only flags the
*second-arriving* row — legitimate requirements question if he asks.

## Boss Fight #1 — rules as stated to him (2026-09-12)

- **From an empty directory, all of it** — `uv init`, `pyproject.toml`, layout, console script,
  `__init__.py`. Packaging was a week-1 time sink, so it's half the test.
- In scope: everything the finished deliverable has, including tests (and CI if week 2 landed it).
- **Allowed:** official docs, searching error messages, `sample_telemetry.csv` and the customer
  spec, me as rubber duck only.
- **Not allowed:** the old `telemetry/` directory or its README, copy-paste, me designing anything.
- **Grey area left to him:** the textbook. Recommended *not* opening it (`02-exceptions…` contains
  his actual fix; `07` describes the redesign's module layout).
- Suggested its own directory (e.g. `boss-fights/01-telemetry/`) with commits as he goes.

**During the fight: strictly hands-off per CLAUDE.md.** Rubber-duck only. No "have you considered."
