# TA notes

Working notes kept by Claude, in the repo so any session on any machine can pick up where the
last one stopped. Not a diary and not a progress log — those are
[00-dashboard.md](00-dashboard.md) and [background-threads.md](background-threads.md).

Read this at the start of a session. Update it at the end, and commit it.

---

## Where things stand

**Last updated:** 2026-09-11 (end of day 3)

- Curriculum started **Wed 2026-09-09**. Day 1 landed on the syllabus's designated *off* day, so
  don't infer the current week or day-of-rhythm from the calendar — check the dashboard or ask.
- Part 1 deliverable lives at `telemetry/` — uv project, src-layout, `pytest` added as a dev dep.
- Design is in `telemetry/README.md`, committed (`d6ae328`).
- **The pipeline runs end to end as of day 3**:
  `uv run python -m telemetry.main data/sample_telemetry.csv output` → `output/output.json`.
  He fixed day 2's crash bugs himself, mostly in the VS Code debugger.
- Six source files plus new `validator.py` and `.vscode/` were **uncommitted** when he stopped —
  ended the session fried, distractions at home. Prompt a commit first thing.
- `scratchpad.md` at repo root is his notes-away-from-PC file.

## Day 3 (2026-09-11)

Started 16:13; **hours not yet written to `docs/background-threads/week-01.md`** — the entry is
open-ended (`20260911 1613 -`), and Thursday's ~2h was never logged at all. Ask him to backfill
both. Dashboard still says "1 hour"; it's a Sunday job.

Pace at day 3: ~5h of the 10–12h target, week-1 checklist has `mypy`, `logging`, `argparse`,
`pathlib`, `exceptions` untouched. Told him design is ahead, running code is behind, and that
Boss Fight #1 can't rehearse a system that never worked. That framing landed — he built the rest
and ran it the same evening.

He asked what CI stood for (thought it might be "command line"). Explained Continuous
Integration, GitHub Actions, and why an empty machine catches "works on mine". Week 2 topic.

Debugger: his `launch.json` had `"args"` as a bare string. Gave him the list form plus
`${workspaceFolder}`, and warned that `"program": "${file}"` debugs whatever tab is focused.
Tooling, so I answered outright.

### Review given at end of day 3 — he has fixed none of it yet

Delivered as critique, not patches. Ordered as I gave it:

1. **The falsy-return bug — the one that matters.** `Validator.*` returns `(value, None)` on
   success and `(False, msg)` on failure, and callers test `if not valid_float`. A parked robot's
   `velocity == 0.0` is falsy, so amr-01's ~12 s of `v=0` rows are **silently dropped as invalid**
   and its average velocity is wrong. No crash, no message. I pointed at the return shape and the
   parked-robot rows and asked him to count the readings — **did not name the fix.** Ties directly
   to the unticked "exceptions and error boundaries" item: the error channel and the value channel
   are the same channel.
2. `__`-prefixed dataclass fields + `to_json` returning `self.__dict__` → report keys come out as
   `_Analysis__warnings`. Name mangling, not privacy.
3. `Analysis.analyze_robot` and every `Validator` method take no `self` and aren't
   `@staticmethod`. Works only because he always calls them on the class. mypy catches this.
4. `analysis.py:30` divides by `len(robot.readings)` — still ZeroDivisionError if every row for a
   robot is bad.
5. Timestamp regression message reads "is after previous" when it fired because it's *before*.
6. `report()` never creates `output_dir`; `output/` exists locally but is untracked → fresh clone
   and CI both hit `FileNotFoundError`.
7. Dead code: `Reading.parse_line` (undefined names, would `NameError`), `Robot.validate_reading`
   (always `True`) and `Robot.try_add_reading` (never called — the parser appends directly).
8. Still `print` and `sys.argv`.
9. `Warning` still shadows the builtin. Flagged twice now; he's keeping it. Let it go.

**Planted defects still uncaught: two.** The exact duplicate row (his `<` timestamp check passes
equal timestamps) and velocity `ERR`— actually caught by `validate_float`, so the duplicate is the
live one; I told him "two" counting the duplicate and the zero-velocity loss. The swapped amr-03
pair only ever flags the first row of the pair.

### Next session

1. Commit the working tree (8 files) **before** any refactor.
2. Backfill Thursday + Friday hours in `week-01.md`.
3. Fix the falsy-return bug — he should choose between exceptions and a proper result type, and
   defend the choice.
   **Post-break update (`e986ec1`):** he added four `assert type(x) is ...` lines in `parser`
   *after* the `if messages: continue`, to narrow the Optionals. Does not fix the bug — the
   `v=0.0` rows are diverted before reaching them — and `assert` is stripped under `python -O`.
   Told him the tell is the commit message itself ("given validator returns optionals"): five
   call sites doing damage control for one return shape. **Still haven't named the fix.**
4. `mypy` — pitch as the thing that catches items 3 and 7 for free.
5. First test: parse a line with `velocity=0.0`, assert a `Reading` comes back. The bug is the
   test case. **He has never written a test before** — arrange/act/assert, `test_*.py`,
   `test_*` functions. `tests/test.py` still collects nothing.

## Telemetry — state of the design (day 2)

Decided by him, after review:

- **`main.py` orchestrates** (parse → analyze → report). He first had `report` driving the
  pipeline; he got to "main coordinates" himself once the report-does-three-jobs point landed.
  His blocker was picturing stages as separate programs passing files (pickle) — explained that
  in-process stages pass return values. Worth revisiting when ROS nodes arrive (week 11).
- **Bad rows are dropped and recorded** on the `Robot`, intended to feed an error-rate in the
  output. Pushed: record *why* and the line number; and a truncated row may have no usable
  `robot_id` — unresolved which list that goes in.
- **Warnings: Strategy pattern** — `Warning` ABC with `BatteryWarning`/`TemperatureWarning`,
  list built in `main`. He first applied them in the parser (mutating `Reading`); after pushback
  he **moved detection into `analysis.py`**. Good.
- Validation is per-reading in the same pass (streaming), separate code not a separate loop — he
  raised the batch-vs-live tradeoff himself.

### The sample data — I play the customer

I generated `telemetry/data/sample_telemetry.csv` (committed as Claude, `94b4543`) and gave a
customer-voice spec: ISO 8601 UTC, m/s, battery %, °C; **warn battery < 20%, temperature > 60 °C**.
I offered to answer requirements questions in character — not design questions.

Deliberate defects — **don't tell him; he's finding them** (he'd found `nan` and blank so far):
`nan` velocity, blank battery, battery `104.2`, temperature `-273.2`, two amr-03 rows swapped
(per-robot timestamp regression), one exact duplicate row, one truncated row (4 fields),
velocity `ERR`. Also by design: amr-02 battery drops to ~16%, amr-03 overheats to ~66 °C,
amr-01 parks (v=0) for ~12 s. Cross-robot timestamps interleave out of order — normal, not a
defect. Generator was a throwaway script, not in the repo.

### Bugs in his uncommitted code — let him find them by running it / mypy

Point at the line only if he's stuck. As of end of day 2:

- `robot.py`: `self.id_ = self.id_` (AttributeError).
- `warning.py`: missing colon on `handle_warning`; methods missing `self`; `TemperatureWarning`
  comparison is inverted (`<` should be `>`); class named `Warning` still shadows the builtin
  (I flagged this — he kept the name).
- `analysis.py`: mutable `[]` default in a dataclass (ValueError at import — needs
  `field(default_factory=list)`); `__` name-mangled fields; `analyze_robot` has no `self` and
  builds a new `Analysis` (should be a function or `@staticmethod`); divide-by-zero on a robot
  with no good readings.
- `main.py`: `with open(...)` not bound to a name, passes the path not the file; `Ana` typo;
  missing `.items()`; still `sys.argv` rather than argparse.
- `pyproject.toml` script still points at `telemetry:main`, but `__init__.py` is now empty —
  the `telemetry` command is broken.
- `tests/test.py` has imports only — pytest collects nothing (needs `test_*.py`, `test_*`
  functions). **He's never written tests before** — first target is the line→`Reading`
  function, test cases = the dataset's defects. Explained arrange/act/assert with a toy example.

**Resolved on day 3** — he found and fixed the crash bugs above by running it, except: the
divide-by-zero, the `__` name mangling, the missing `self`, the broken `parse_line`, and
`tests/test.py` still collecting nothing. Those carry forward to the day-3 list below.
`pyproject.toml`'s `telemetry:main` script entry is still broken — he runs it with
`python -m telemetry.main` instead, so the CLI item is unfinished.

Remaining week 1 checklist items — mypy, logging, argparse, pathlib, exceptions — exercise while
building, not as separate topics. Dataclasses and type hints are now in use.

## Environment — verify block run 2026-09-10

OK: Ubuntu 24.04, RTX 5080 visible (driver 591.86), uv, git identity. **Missing:** `gcc`,
`cmake`, `gdb`, `valgrind` (needed before C++ starts), Docker (needed for CI/containers), no
`~/.ssh` (fine if pushing over HTTPS). PyTorch not yet checked. The toolchain checklist in
`environment.md` is still all unticked.

**Boss Fight #1** (week 2) is a blank-page rebuild of this toolkit. Strictly hands-off once it
starts — see CLAUDE.md.

## How to work with him — learned, not in CLAUDE.md

**Verify before advising.** When he reports something done, check the actual state with bash
first. On day 1 every such report was partially incomplete:

| Reported | Actually |
| --- | --- |
| "git init done, dev branch created" | no commits, no `.gitignore` |
| "committed" | only `telemetry/` — syllabus, docs, `.gitignore` left untracked (`git add *` from a subdirectory; the shell expands `*`, skipping dotfiles) |
| "`.gitignore` fixed" | patterns path-anchored, so nested `__pycache__/` wasn't matched |

None of this is carelessness — it's the small tooling detail that never announces itself, which
is exactly the gap Part 1 exists to close. He responded well to each catch and fixed them
himself. **Name what's wrong and why it matters; don't fix his repo for him.** Tooling,
environment, and docs files are the stated exception.

He is on limited evening hours. Lead with the answer.

**Day 2 observations:**

- He was hesitant to ask "check my work" every step. I told him review at *decision points* is
  the high-value work — keep inviting it.
- He takes design pushback well and changes course (warnings → analysis) but defends first,
  sometimes with a weak reason ("flexibility", "perhaps"). Name the weak reason plainly; the
  interview framing ("could you defend this?") lands.
- Moves fast and edits documents piecemeal, which produces self-contradicting designs. He vented
  about it ("maybe I'm rushing"). Answered with accuracy, not reassurance: yes a little; reread
  top-to-bottom; move to type-checked code. That's the confidence-gap pattern from CLAUDE.md.
- Formatting markdown is fine for me to do (tooling). Suggested the markdownlint extension.
- Commit-message question: explained what/why over when. Watch whether commits get smaller.

## Decisions made, so they don't get relitigated

- **uv over pip.** The lockfile is the point, not the speed. `uv.lock` is committed; `.venv/` is
  not.
- **Python 3.12**, because Noble ships it and Jazzy is built against it — not a free choice.
- **Every project gets its own directory** with its own `pyproject.toml`. The repo root is the
  curriculum, not a package.
- **Commits Claude makes are authored as Claude**, not as Chris:
  `git commit --author="Claude <noreply@anthropic.com>"`. This repo is evidence of Chris's own
  work, so authorship has to be honest about who wrote what. A `Co-Authored-By` trailer is not
  sufficient — it claims he co-wrote it.
- Filenames stay boring: no spaces, no glob metacharacters. An earlier `*c` suffix convention
  was reverted — `*` is illegal on NTFS and would break checkout on the Windows side of the
  planned dual-boot.
