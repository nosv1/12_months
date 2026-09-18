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
`-Infinity` in the JSON breaks the customer's dashboard.

**Answered 2026-09-15, valid ranges** (he was right that these were never specified — he'd invented
`[-2, 2]` and `>= 0` himself). All **inclusive**:

| field | range | rationale given |
| --- | --- | --- |
| velocity | `[-2.0, 2.0]` m/s | drive firmware hard-caps at 2.0; reverse same magnitude (docking) |
| battery | `[0, 100]` % | already specified 09-13 |
| temperature | `[-40, 150]` °C | motor controller sensor's rated range |

**Sub-zero temperatures are valid** — two sites run cold-storage aisles at −20 °C ambient, and a
controller parked overnight reads near that. `-273.2` stays rejected. This makes his old `< 0`
rule wrong, and the inclusive velocity bound exposes an off-by-one in `abs(value) >= 2` that no
sample row catches (fastest legitimate row is `1.468`).

**Answered 2026-09-15, error reporting:** errors per row are a **list**, always, even at length
one. Report carries both a stable error *name* (filterable) and a plain-words *message* (goes in
firmware tickets) — he proposed both, accepted. Unrecognized errors go in an `UnrecognizedError`
bucket with a count that should always be zero; **quarantine, don't crash** — a shift can't wait
for a release.

**Answered 2026-09-16, wrong column count:** `MissingDataError` replaced by **`ColumnCountError`**
— the name says what's wrong with the row, not why, because half these rows are truncated writes
and half are duplicated delimiters. Message must carry both counts: `Expected 5 columns, found 4.`
(it gets pasted into firmware tickets). **A header is always present**, first line, no exceptions;
a file without one is a broken export and should fail loudly — not be parsed with a data row as
the header. **A vendor firmware update once appended a column and the old tooling rejected all
40,000 rows**, so checking against the header beats a constant someone has to remember to update.
Handling *new* columns gracefully is explicitly not required yet, but don't build something that
makes it impossible. (TA note: deriving the count fixes appended columns and turns *inserted*
columns from a loud failure into silent field-shifting corruption. He was told; his call.)

Remaining candidate requirements questions: can columns be reordered; should a swapped pair flag
both rows.

**The ranges and warn thresholds are in `telemetry/README.md`** (his, `6d86f4e`). But the README
also carries the stage pipeline and the design-decisions section, so it is *not* readable during
Boss Fight #1. The permitted input is [docs/telemetry-requirements.md](../telemetry-requirements.md)
— requirements only, customer voice, no design and no defect list. Extracted 2026-09-17.

### Spoilers: the planted defects

*He reads these notes. As of week 1 his code catches all of these, so this is no longer secret in
practice — but the boss fight is a rebuild, so skim past if you want it cold.*

`nan` velocity, blank battery, battery `104.2`, temperature `-273.2`, two amr-03 rows swapped
(per-robot timestamp regression), one exact duplicate row, one truncated row (4 fields), velocity
`ERR`. By design: amr-02 battery drops to ~16%, amr-03 overheats to ~66 °C, amr-01 parks (v=0)
~12 s. Cross-robot timestamps interleave — normal.

Verified output (week 1 and again after the week-2 redesign): bad rows per robot
`{unknown: 1, amr-01: 2, amr-02: 2, amr-03: 3}` = all 8.

**Added 2026-09-15 at his request, line 363** (appended, so nothing renumbers):
`2026-09-03T14:02:00.018Z,amr-01,4.812,118.4,-41.0` — velocity, battery *and* temperature all out
of range in one row. Timestamp is valid and correctly ordered, so it is purely a value-fault row.
Three faults, not two: two would let "collect the first two" pass. **Bad rows are now 9, but total
errors are 11** — those numbers diverging is what proves the errors field is a list. Every other
planted defect is single-fault, so the sample alone could never have tested multi-error collection. The swapped pair only flags the
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
