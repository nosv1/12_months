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

**Updated 2026-09-17 21:19.**

- Started Wed 2026-09-09. **Week 2 in progress.** **22.05 h logged.** Nominal week 3 (C++) start:
  Mon Sep 21.
- **Boss Fight #1 starts Saturday Sep 19**, his call, agreed. To pay for it, README, CI, `pdb`,
  the `test_validations.py` split and all the cosmetic smalls are **cut into week 3**. Friday is
  multi-error collection only, hard stop Friday night.
- **The fight's permitted input is [docs/telemetry-requirements.md](telemetry-requirements.md)**
  (new, 09-17) — customer voice, requirements only. `telemetry/README.md` is **not** readable during
  the fight: Architecture and Design decisions sit directly under the ranges table.
- **Suite is green: 37 passed.** The attribution bug is fixed and the accepts side exists.
- **He rewrote the timestamp stage and deleted `validate_robot_timestamps`.** Order checking now
  lives in `validate_parsed_line_values`, comparing against the previous *accepted* reading. That
  closed the double format parse, the unvalidated "previous" row, the triple-reported malformed
  timestamp, and the mid-iteration `del` — all in one change.
- **`Reading` now carries `line_number`.** His call, knowingly: cheap now, revisit at week 11 when
  readings arrive off a topic and the identity has to be a *source*, not a line.
- **The accepts side found silent data loss** — `headers_count` (a column count) used as a count of
  header rows to skip, discarding four valid rows. All 29 rejects tests passed over it.
- Textbook through [14](textbook/14-partition-invariants-and-where-tests-go.md).
- He asked me to **hold the project-manager voice** — he's playing PM himself. Customer voice on
  request, as before.

## Next session (Friday 09-18 — one item, then stop)

1. **Log hours:** run `date` at the opener.
2. **Multi-error collection. The only Friday item.** Parked mid-design; his own estimate is 30–45
   min of thinking and coding. He's circling a `field → validator` map iterated over `ParsedLine`.
   Four things put to him, none answered — don't answer them for him:
   - import direction: validator already imports parser, so parser → validator closes the
     textbook-07 cycle
   - does the map belong to the data or to the validating stage
   - it fits the four field validators but **not** the relational order check, which needs a valid
     timestamp before it can run at all
   - `Reading(...)` short-circuits on left-to-right **argument evaluation** — so that function can
     no longer be one expression. **The return type is the design.**
3. **Then stop.** If Friday's item overruns, it goes to week 3 too. Saturday is the fight.
4. **Boss Fight #1, Sat Sep 19.** Strictly hands-off, rubber-duck only. Rules in
   [telemetry.md](ta-notes/telemetry.md). Spill into week 3 allowed.

## Open, his, not blocking the fight

- **No `py.typed` marker** in the package, so his annotations are invisible to mypy from outside
  the source tree. Found 09-17. Packaging, so it matters for the fight.
- `validate_timestamp_order` **returns `True`** — a constant, so the accepts test asserts nothing.
  Every other validator returns the parsed value. Told him 09-17.
- **conftest runs the pipeline twice**: `sample_parsed_lines` and `sample_bad_readings` each call
  `get_parsed_lines_and_bad_readings` and discard half, so the partition test compares two
  independent runs. Passes by determinism, not construction. Told him 09-17.
- **`robot_id` has no validator at all.** Noticed 09-17, not raised with him.
- Every fixture is the sample file; no small hand-made inputs. `parse_lines` has no test for empty
  or headerless input.
- Smaller, still open: `list(lines)[0]` materialises the whole iterable; trailing `\n` in messages;
  `NotANumberError("", ...)` empty first arg; `UnknownError`/`UnrecognizedError` never raised;
  `build_report -> dict` untyped and untested; magic-number limits vs injected thresholds (and the
  same `20`/`60` duplicated in conftest); `-Infinity`; `readlines()`.
- **Customer questions still unanswered**, in §8 of the requirements doc: can columns be reordered;
  should a swapped pair flag both rows. His to ask.
- Done since 09-16: ruff config landed (`select = ["E4","E7","E9","F","B","C4"]`), stale
  `"was missing data"` log string gone, `validate_timestamp_order` has three unit tests.

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
