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
- 09:22 → _(resume time)_ — away briefly. Status at pause: 7/7 tests green; package imports
  resolved after the `01_telemetry` → `telemetry_boss_fight` rename. Uncommitted: 8 modified,
  4 new (`main.py`, `validator.py`, `test/test_parser.py`, `debug.sh`). Open loose end: `data/`
  sits outside the project root. Elapsed so far: 2h12m.

**Stopped:**

### What went wrong

### What I couldn't remember

the bloody imports!

### What I'd do differently
