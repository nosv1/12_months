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

**Updated 2026-09-26 18:35, signed off by him** ("maybe back later"). 16:27–18:35 logged, split
across week 4 (0.82 h) and week 5 (1.32 h). **49.49 h logged.** Session logs:
[week-04.md](ta-notes/sessions/week-04.md), [week-05.md](ta-notes/sessions/week-05.md).

- **Week 4 ticked 09-26** (`f576084`), finished day 3 of 7. Textbooks 24–26; copy elision added to 25.
- **Root reorganized 09-26** (`14a8d6f`, other session; re-authored as Claude 09-26, was `cb37641` on the remote): `projects/`, `labs/wNN-topic/`,
  `boss-fights/`. `cpp_memory/` → `labs/w04-cpp-memory/`, now tracked with a README. Old paths in
  logs and textbook left as written.
- **Week 5 started 09-26 17:16**: STL library, `Sensor → SensorBuffer → Processor → Statistics`.
  His design so far: `Reading` base with `IMUReading`/`TempReading`; ring buffer, keep newest N;
  Processor integrates 1-axis accel → velocity; Statistics compares against simulated truth to
  show drift. Open, his: what the base `Reading` interface is; checkable end state (asked twice).
- **Syllabus revision §13 merged into `dev`** (`d99bc75`, conflict in estimates.md only, both sides
  kept). Components weeks 8–9, Parts 4–10 shifted +2, Part 11 → 2 weeks, ESP32 + micro-ROS. **Bench
  kit must be ordered by week 6 — raise it in week 5.** Merge is local; **he pushes**. Remote branch
  `claude/chat-session-5ev4q7` can be deleted once pushed; his call.
- Career thread (09-24, 09-27): optimization/planning lane, ArduPilot as PR target, aerial folded into existing weeks (no syllabus change). **Goals are capabilities, never a company**: his rule. MS lab was drone M&S. observations.md.

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

## Next session: `IMUBuffer`, the ring-buffer policy

Where it stands: `labs/w05-sensor-processing/` builds and runs (`IMUReading` with `Timestamp` on
`steady_clock`, `Acceleration`/`Gyro` in mps2/rad_s). **Untracked — his to commit.** No buffer yet.

Open, his: where "capacity N, drop oldest" lives and what erasing element 0 of a `vector` costs
(ring index vs `std::deque`); run the 30-second slicing experiment; a checkable end state for the
week (asked three times — get it before building); README.

He's **decision-fatigued** at the end of 09-26. Next session: give him a concrete, buildable step
first, not another open design question. Sunday 09-27 he's busy — review may be short or slip.
**Bench kit order (by wk 6) still to raise.**

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
