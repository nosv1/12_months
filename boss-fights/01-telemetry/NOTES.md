# Boss Fight #1 — Telemetry Toolkit, from an empty directory

**Week 2 · starts Saturday 2026-09-19**

Logistics and rules only. Nothing about the solution is in this file, and nothing about the solution
should be added to it until the fight is over.

---

## The task

Rebuild the telemetry analyzer in this directory, from nothing. Design it yourself.

## Permitted

- [`docs/telemetry-requirements.md`](../../docs/telemetry-requirements.md) — the customer's brief,
  §1–§9. This is the spec.
- `telemetry/data/sample_telemetry.csv` — the input file.
- Official documentation for any tool or library. Search engines for error messages.
- Claude as a **rubber duck only** — describe a problem aloud, get questions back, not answers.

## Not permitted

- The `telemetry/` directory, or its `README.md`.
- Copy-paste from anywhere, including your own previous work.
- `docs/ta-notes/telemetry.md` — it is a design summary and a defect list. Out for the same reason
  the README is out.
- Claude designing anything: no architecture, no module layout, no "have you considered".
- Copilot or any other autocomplete. Turn it off before you start.

**Grey area, your call:** [`docs/textbook/`](../../docs/textbook/README.md). Recommended closed —
entries 02 and 07 describe this project's actual structure.

## In scope

Everything the deliverable has, including packaging from scratch — `uv init`, `pyproject.toml`,
layout, `__init__.py`, `py.typed`, a console script on the path — and the tests.

**Out of scope:** CI and the README. Week 2 didn't land them, so they aren't part of the rebuild.

## Process

- Commit as you go. The history is the evidence that this was a rebuild and not a recall of one
  sitting.
- Estimate first, then apply your ~3× factor from Friday 09-18 and plan against that number.
- Write the stop time down before you start.

---

## Log

Fill this in as you go — especially what went wrong.

**Estimated:**
6h

**Started:**
7:10

**Paused:**

- 09:22 → 12:42 (3h20m off the clock). Status at pause: 7/7 tests green; package imports
  resolved after the `01_telemetry` → `telemetry_boss_fight` rename. Uncommitted: 8 modified,
  4 new (`main.py`, `validator.py`, `test/test_parser.py`, `debug.sh`). Open loose end: `data/`
  sits outside the project root. Elapsed so far: 2h12m.
- 14:49 → 15:00 — bathroom break.
- 17:10 (09-19) → end of day 1. Clock stopped at 6h29m.

**Day 2 started:** 09-20 08:15

**Estimate overrun:** 6h29m on the clock at the 17:10 pause, against a 6h estimate, and not
finished. Not drift — deliberate scope beyond the original: a larger test suite (17 green at the
pause, vs 7 at 09:22) and header handling the first pass didn't have. Time was tracked throughout,
so the overage is a scope decision, not a discovery at the end.

Christopher's breakdown at the pause: the header work cost roughly an hour. Backing that out leaves
~5h30m on scope equivalent to the original, with some work still remaining — so the finish lands
a little over 6h, on the order of 10-20%. Worth holding against the 3x factor from 09-18, which
came from being wrong by multiples. One data point, not a recalibration.

**Stopped:** 09-20 11:24

**Total on the clock: 9h38m** (day 1 6h29m + day 2 3h09m), against a 6h estimate — 1.6x over.
Backing out ~1h of header work not in the original scope puts equivalent scope at ~8h40m, 1.4x.
Finished state: 38 tests green; console script installed via `uv tool install` and resolving at
~/.local/bin/telemetry_boss_fight, verified outside the source tree (§8).

### What went wrong

I got tired. I got tired of doing the test. Functionally, it went smoothly enough.
given im kinda racing a clock, i was lazy on some bits, did a weird try except re re-raise thing in parser that im not happy about, but i didn't bother making cleaner because i just couldn't be asked

### What I couldn't remember

the bloody imports!

### What I'd do differently

no idea

---

## TA review — 2026-09-20, after the fight

Reviewed against `docs/telemetry-requirements.md` §1–§9. Findings verified by running the tool, not
by reading alone. Ordered by what would bite a customer first.

### What held up

- **Multi-error collection works.** Line 363 rejects with three errors in one record, which is §6's
  "errors are a list" requirement and the thing you got wrong the first time on 09-18.
- **Line numbers are original-file numbers**, and `original_line` is the raw row, not a re-rendered
  one. That's §6.1 and §6.3, and they're easy to get subtly wrong.
- **The truncated row (line 302) is correctly unattributed** — top-level, not filed under a guessed
  robot. §6's "never invent a robot" holds.
- **Header validation is order-independent.** `ParsedLine` zips header to value by index, so a
  reordered file parses correctly. §9 lists column reordering as undecided; you happened to pick
  the tolerant answer, which is the right way to be wrong.
- **`nan` is rejected** (line 39) — `isnan` in `validate_float` catches the token `float()` accepts.
- Pipeline stages are cleanly separated: read → parse → group → validate → report.

### Bugs

1. **The report never says which robot a robot is.** `Robot.to_json` returns
   `{"warnings": [...], "rejected_readings": [...]}` with no `robot_id` key. §7 asks for output
   "per robot"; what ships is an anonymous list. Warnings happen to embed the id inside a prose
   string, and rejected rows don't carry it at all — the dashboard would have to re-parse
   `original_line` to find out whose row it was. This is the one that fails the customer.

2. **The installed command is stale, and it doesn't emit JSON.** `uv tool install` copies the
   package; it does not track the source tree. The copy at
   `~/.local/share/uv/tools/telemetry-boss-fight/` predates `print_report`, so the installed tool
   prints a Python dict repr — single quotes, `None` instead of `null`. Not JSON, so §7's
   dashboard cannot parse it. The live code is correct; the shipped artifact is not. §8 is
   satisfied only by the installed artifact, so §8 is currently failing.

3. **A bad header silently discards the entire file.** `parse_telemetry_lines` catches
   `InconsistentHeaderError` and returns empty lists, so a header typo produces
   `{"robots": [], "rejected_readings": [], "unrecognized_failures": 0}` and exit 0 — identical to
   a file with no data rows. §6 says quarantine rather than crash, but silently reporting nothing
   is worse than crashing: nobody learns the shift's data was dropped.

4. **An empty `robot_id` becomes a robot.** A row with `,,` groups under `""` and appears as a
   robot in the report. That is filing a row under a robot that doesn't exist, which §6 forbids.

5. **`Robot.to_json` fabricates data to satisfy the type checker.** If the timestamp isn't a
   `datetime` it substitutes `datetime.now()`, and if the value isn't a float it substitutes `-1`.
   A fabricated `-1` battery is below 20, so it would emit a warning, stamped with the time the
   report ran, for a reading that never happened — into a ticket a vendor engineer reads.
   Unreachable today because validation guarantees the types, which is exactly why it will survive
   until it isn't. Narrow the type or raise; never invent a value to quiet mypy.

6. **A missing input file exits with a raw traceback.** Ops types a wrong path and gets a stack
   trace from `reader.py`. §8's user "is not going to activate a virtual environment" — they are
   also not going to read a traceback.

### Requirements not fully met

- **§5, thresholds.** `20` and `60` live in `config.py`. The customer said not to bury them
  "somewhere we have to come to you to change." Because the tool ships via `uv tool install`,
  changing a threshold today means editing source and reinstalling — which is coming to you. A
  cold-storage site with a different battery threshold cannot be served by the shipped artifact.
- **§7, `-Infinity`.** Currently unreachable, since the report contains no computed floats — the
  right outcome, reached by accident rather than by decision. Note that `json.dumps` emits the
  bare tokens `Infinity` and `NaN` by default; `allow_nan=False` turns that into an exception
  instead. Worth knowing for when a float does enter the report.

### Shape

The nested `try`/`try` at `parser.py:143` (self-described as "disgusting") exists because
`validate_timestamp_order` raises errors carrying the literal string `"unknown"` for `robot_id`,
so the caller catches and rebuilds each one just to fill in a value it already had. The validator
doesn't know the robot id because it wasn't given it. Both branches then do the same thing.

`validate_velocity`, `validate_battery` and `validate_temperature` are the same twenty lines three
times, differing only in which `Header` and which two error classes they use — and those error
classes are themselves empty subclasses that add nothing to their parents.

### Tests

38 green, and the suite is real — parametrized rejects, fixtures composed from other fixtures.
Two structural gaps:

- **No test covers `report.py` or `main`.** The deliverable is the least-tested module, and finding
  #1 (no robot id) and #2 (not JSON) both live there. Unit tests on parts don't compose into a
  guarantee about the whole.
- **Every fixture derives from the one sample file.** Same shape as the `-Infinity` miss on 09-18:
  the suite can only find bugs the sample file contains. `TimestampIdenticalError` is still
  referenced by no test, and the sample file happens to contain one.

### If there were an extra day

In order: give the robot an id in the report (#1), reinstall and verify the artifact (#2), make a
bad header loud (#3), then test the report module. The gross bits are sixth. Shape is cheap to fix
later and correctness isn't.

### Addendum, 2026-09-20 — finding #1 fixed

`robots` now carries the id: `"robots": [{"amr-01": {"warnings": [...], "rejected_readings": [...]}}, ...]`.
The information the dashboard needed is there. The shape is worth one more thought, though — a list
of single-key dicts is the awkward middle between the two shapes a consumer can use directly:

- `{"amr-01": {...}, "amr-02": {...}}` — a mapping, if lookup by id is what the dashboard does.
- `[{"robot_id": "amr-01", "warnings": [...]}, ...]` — a list of uniform records, if it iterates.

With the current shape a consumer must take `list(entry.keys())[0]` on every element to learn the
id, which reads as a mapping and indexes as a list. Not a bug, and not urgent. Findings #2 (stale
installed artifact) and #3 (silent header failure) still matter more.
