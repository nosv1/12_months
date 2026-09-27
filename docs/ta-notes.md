# TA notes

Claude's working notes, in the repo so any session on any machine can pick up where the last one
stopped. Not a progress log — that's [00-dashboard.md](00-dashboard.md) and
[background-threads.md](background-threads.md).

**At session start read this file only.** Open the others when the situation calls for them. At
session end: update *Where things stand* and *Next session* here, append to the week's session
log, commit as Claude. **Keep this file short** — when something here stops being needed every
session, move it out.

He reads these notes too. Write them so that's fine.

| File | Open when |
| --- | --- |
| [ta-notes/observations.md](ta-notes/observations.md) | pushback or confidence conversations; Sunday review |
| [ta-notes/telemetry.md](ta-notes/telemetry.md) | reviewing telemetry code; answering as the customer; Boss Fight #1 rules |
| [ta-notes/decisions.md](ta-notes/decisions.md) | before proposing a process, tooling, or convention change |
| [ta-notes/estimates.md](ta-notes/estimates.md) | giving any time estimate (log it); sign-off (fill actuals); Sunday review (ratios) |
| [ta-notes/sessions/](ta-notes/sessions/) | a thread from a past session comes back up (`week-NN.md`) |

---

## Where things stand

**Updated 2026-09-27 18:35, break** ("i'll be back"). 17:21–18:35 logged (1.23 h). **51.70 h
logged.** Session log: [week-05.md](ta-notes/sessions/week-05.md).

- **Textbook 27 (TVC) stranded** on `origin/claude/aerospace-exploration-b3o9z5` (`91d8bc6`),
  pushed after PR #2 merged. His to PR/cherry-pick. Owed entry is 28.
- **Build log empty weeks 2–5** (Built/Broke/Learned/Stuck). Raised 09-27.
- **Bench kit order due by 10-03** (week 6). Raised 09-27, not acted on.
- Week 5 design: ring buffer, capacity via constructor, `std::vector` sized once. Open, his:
  head == tail ambiguity; default-ctor trap; capacity 0; public interface; checkable end state
  (asked four times now).
- Career thread (09-24, 09-27): optimization/planning lane, ArduPilot as PR target, aerial folded into existing weeks (no syllabus change). **Goals are capabilities, never a company**: his rule. MS: drone research lab, M&S for base defense (classified; public version only). observations.md.

## Week progress — render this as the session opener

```text
Week 5 · STL and idiom   ██░░░░░░░░░░░░░░░░  0.5/5   day 1 of 7 (started 09-26)   my est 8–12 h left
  ◐ vector, unordered_map, string_view, optional   — vector in use; others not touched
  ☐ iterators + <algorithm>
  ☐ templates (reading)                            — lands with SensorBuffer<T> + TempReading
  ☐ exceptions vs error codes
  ☐ build a library, link it from another project  — single executable so far
```

Items are the syllabus checklist for the week; ◐ counts as half. Syllabus ticks still wait for
verification, so this block is the mid-week state. Update it at sign-off with the session log.
When the remaining work fits in one session, **say so up front**.

## Next session: finish the ring, then test it

`labs/w05-sensor-processing/` has `IMUBuffer` v1 (vector + `erase(begin())`), `.cpp` splits for
reading/timestamp, and an untracked `sensor_processing_test.cpp` I haven't seen. **All of it
uncommitted — his.**

Pick up at: head == tail (empty vs full) — the question he left open. Then `IMUBuffer` → `class`,
ring with head/tail(+count), then gtest via FetchContent with the library split. First test: 150
adds, predicted size written down before running.

**Keep replies short.** Instructions I give between tool calls get buried. Put the task in the
**final** message, never mid-turn.

## Open, his — the week-2 `telemetry/` project (not the fight rebuild)

- **No test for the `-Infinity` fix.** The bug is fixed; nothing pins it. Needs a robot with zero
  valid readings — two lines of input. `json.dumps(report, allow_nan=False)` is the oracle.
- **§6's unrecognized-failure count is absent from the report.** Top-level keys are `robots` and
  `bad_readings` only. Requirements gap, not raised with him yet.
- `test_parsed_line_rejects` now pins the **count** (1 and 3) — verified to fail against a
  short-circuiting `validate_parsed_line`. Still only checks the *base* type, so three wrong error
  classes would pass. Naming the classes is the stronger version; told him, not blocking.
- **conftest runs the pipeline twice**: `sample_parsed_lines` and `sample_bad_readings` each call
  `get_parsed_lines_and_bad_readings` and discard half, so the partition test compares two
  independent runs. Passes by determinism, not construction. Told him 09-17.
- **`robot_id` has no validator at all.** Noticed 09-17, still not raised.
- Fixtures: `sample_valid_line` (09-18) is the **first hand-made input** in the suite. The rest are
  still the sample file. `parse_lines` has no test for empty or headerless input.
- Smaller, still open: `seed_max_temp` names the running value, not the seed; `list(lines)[0]`
  materialises the whole iterable; trailing `\n` in messages (arguably correct per §6); `"had a/an
  exception(s)"` log string; `",".join` with no space; `NotANumberError("", ...)` empty first arg;
  `UnknownError`/`UnrecognizedError` never raised; `build_report -> dict` untyped and untested;
  magic-number limits vs injected thresholds (same `20`/`60` duplicated in conftest); `readlines()`.
  Resolved 09-21: `pyproject.toml` description filled in; `matplotlib` and the
  dead `Robot.plot` removed.
- **Customer questions still unanswered**, §9: can columns be reordered; should a swapped pair flag
  both rows. His to ask.
- Resolved 09-18: `validate_timestamp_order` no longer returns a constant (`a57b142`, his), stray
  `Literal` import gone, `set_analysis_to_none` gone. **`py.typed` added and verified** — a consumer
  outside the tree now gets real type errors instead of `import-untyped`, and `uv build` ships the
  marker in the wheel without any `pyproject.toml` entry.

## Standing instructions

- **Open every session with the week progress bar** (block above): items done/total, day of the
  week, my estimate of what's left. Asked for 2026-09-26 — the remaining-work picture should come
  at the start, not as a surprise "that's the week" at the end.
- **I log his hours.** Opener → `date`. Sign-off → `date`, append
  `YYYYMMDD HHMM - HHMM (N hours -- note)` under **Hours** in
  `docs/background-threads/week-NN.md`, bump **Hours logged** in `00-dashboard.md`, commit as
  Claude. No sign-off → ask for the end time next session. Don't guess.
- **Commits I make are authored as Claude** (`--author="Claude <noreply@anthropic.com>"`). Don't
  sweep his uncommitted edits into my commits. **Mechanism: stage explicit paths. Never `git add -A`
  or `git add .`** — a clean tree at session start is no guarantee it's clean twenty minutes later.
  Broke this 09-18 (swept his `test_validations.py` into a docs commit); he caught it.
- **Verify before advising** — his "done" and my own summaries both. Run it.
- **Never approximate a time.** Run `date`, every time. Said "~18:50" when it was 18:44 and burned
  six minutes of his evening on paper. He is pacing against these numbers. Told me 09-18.
- **Reformat any markdown freely**, his READMEs included. Formatting only; keep his wording.
- **`scratchpad.md` is background, not a prompt.** Read at session start; don't raise entries
  unprompted. Discuss when he asks.
- **Log every time estimate** in [ta-notes/estimates.md](ta-notes/estimates.md), his and mine, when
  given; fill actuals from `date`/commits at sign-off. Never revise an estimate after the fact.
  Asked for 2026-09-21: my numbers were priors, not measurements of him.
- **Textbook entry whenever a real lesson is given.**
- **I play the customer** for telemetry requirements questions — see telemetry.md.

## How to work with him — the short version

Lead with the answer. Mechanics get direct answers; design stays his. "Feels gross" from him is
usually right — ask him to name it. Name weak reasons plainly. Answer venting with accuracy, not
reassurance. One-word replies mean he's tired: park decisions. Details in
[observations.md](ta-notes/observations.md).
