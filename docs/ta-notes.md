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
| [ta-notes/sessions/](ta-notes/sessions/) | a thread from a past session comes back up (`week-NN.md`) |

---

## Where things stand

**Updated 2026-09-14 18:29.**

- Started Wed 2026-09-09. **Week 2 in progress.** **15.75 h logged.** Nominal week 3 (C++) start:
  Mon Sep 21. Not behind on hours; the boss fight is the thing at risk (see below).
- Week 1 done and verified. C++ toolchain installed and verified.
- **2026-09-14: functional core / imperative shell split, by him.** `analyze_telemetry(lines,
  warnings) -> Analysis` is the pure composition; `main(path, out)` is read → analyze → dump and
  nothing else. New `Analysis` dataclass (`robot_analyses: dict[str, RobotAnalysis]` +
  `bad_readings`) replaced the loose 2-tuple; the old `Analysis` is now `RobotAnalysis`.
  `analyze_robot` moved off the class to a module function. `reporter.py` split into pure
  `build_report` and `dump_analysis`. New `grouper.py`. Broken `__main__` block deleted.
  Verified at close: 3 tests pass, mypy clean on 13 files, console script works.
  **His work is uncommitted** — do not sweep it into a Claude commit.
- **`test_all_defects_caught` now asserts** `num_bad_readings == 8`. First real assertion in the
  suite.
- Textbook through [09](textbook/09-io-at-the-edges.md). **No personal pronouns in textbook
  entries** — his call, now in the entry conventions; 07/08/09 retrofitted.

## Next session

1. **Log hours:** run `date` at the opener.
2. **Review left on the table (all his, none started):**
   - `analyze_telemetry` lives in `analysis.py`, which now imports `grouper` and `parser` — the
     composition is inside one of its own stages. Cycle risk the moment any stage needs the
     `Analysis` type; he's already had that bug (07). Suggested `pipeline.py`.
   - `group_and_validate_robots` has "and" in it and doesn't group — grouping already happened.
     Its chain is `dict[str, list[ParsedLine]] → dict[str, Robot]`.
   - `analyze_robots` takes `bad_readings` only to pass it to the `Analysis` constructor.
   - `build_report(...) -> dict` is a bare `dict`; `"bad_readings"` still shares a key namespace
     with robot ids.
   - Three function-local imports in `test_validations.py` — asked twice why, no answer yet.
3. **Tests, the week-2 item.** Agreed direction, his to write: upgrade `== 8` to a **set of
   line numbers** read off the sample file (identity not count, and pytest prints the symmetric
   difference); add `pytest.mark.parametrize` unit tests per defect kind on inline strings.
   Warned against deriving the expected set from the validators — self-fulfilling test.
4. **His idea, good, not yet built:** distinct exception types per validation failure instead of
   bare `ValueError`. That's what would let `BadReading` carry a stable *kind* so tests can assert
   `(line_number, kind)` without coupling to prose error messages.
5. **Stage order, still open (his):** timestamp order check runs before the value check. Last
   hint given: the order check needs the `datetime` the value check produces — is "first" an
   earlier pass or earlier in the same iteration? Don't go further unless stuck 30+ min.
6. Still open, his: `-Infinity` for a robot with no good readings; who serializes `BadReading`;
   swapped-pair semantics; column indexes; `headers_count`; `readlines()`.
7. Rest of week 2: `pdb` (tick only after real use), CI after tests, README once modules stop
   moving. `conftest.py` explained 09-14, not built — offered as the anchor for the data dir.
8. Offered `ruff` (mine, tooling). Not accepted yet; raised again 09-14 re: an unused import.
9. **Boss Fight #1:** target Sun Sep 20, spill into week 3 allowed. Strictly hands-off. **If the
   week runs short, slip README and CI, not this.**

## Standing instructions

- **I log his hours.** Opener → `date`. Sign-off → `date`, append
  `YYYYMMDD HHMM - HHMM (N hours -- note)` under **Hours** in
  `docs/background-threads/week-NN.md`, bump **Hours logged** in `00-dashboard.md`, commit as
  Claude. No sign-off → ask for the end time next session. Don't guess.
- **Commits I make are authored as Claude** (`--author="Claude <noreply@anthropic.com>"`). Don't
  sweep his uncommitted edits into my commits.
- **Verify before advising** — his "done" and my own summaries both. Run it.
- **Reformat any markdown freely**, his READMEs included. Formatting only; keep his wording.
- **`scratchpad.md` is background, not a prompt.** Read at session start; don't raise entries
  unprompted. Discuss when he asks.
- **Textbook entry whenever a real lesson is given.**
- **I play the customer** for telemetry requirements questions — see telemetry.md.

## How to work with him — the short version

Lead with the answer. Mechanics get direct answers; design stays his. "Feels gross" from him is
usually right — ask him to name it. Name weak reasons plainly. Answer venting with accuracy, not
reassurance. One-word replies mean he's tired: park decisions. Details in
[observations.md](ta-notes/observations.md).
