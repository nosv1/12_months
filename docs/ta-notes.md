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

**Updated 2026-09-15 19:01.**

- Started Wed 2026-09-09. **Week 2 in progress.** **17.65 h logged.** Nominal week 3 (C++) start:
  Mon Sep 21. Not behind on hours; the boss fight is the thing at risk (see below).
- Week 1 done and verified. C++ toolchain installed and verified.
- Everything through 2026-09-14 is committed (`8f673c9`). The functional core / imperative shell
  split landed: `analyze_telemetry` in `pipeline.py`, `Analysis` / `RobotAnalysis`, `grouper.py`,
  `build_report` split from `dump_analysis`.
- **2026-09-15: exception taxonomy, all his.** New `exceptions.py` with a `TelemetryException`
  base and per-field classes (`VelocityOutOfRangeError`, `BatteryNotANumberError`, …).
  `BadReading` now holds the **exception object**, and `to_json` emits both `exception` (class
  name) and `error` (message). `validate_timestamp_format` converts the stdlib `ValueError` into
  `TimestampFormatError`. First attempt used a `KNOWN_EXCEPTIONS` set + blind `except Exception`;
  replaced with the base class after three verified findings (see week-02 session log, and
  textbook 10). **Verified at close: ruff clean, mypy clean on 15 files, all 9 defects caught with
  correct kinds.**
- **He committed the spec ranges himself** (`6d86f4e`): README updated, `validator.py` now
  inclusive on velocity and `[-40, 150]` on temperature. **The rest is still uncommitted** —
  5 files plus the new `exceptions.py`; he said he'd commit after me. Do not sweep it into a
  Claude commit.
- Textbook through [10](textbook/10-exception-taxonomies.md).
- **Sample file now has 9 defects, not 8** — added line 363, a three-fault row, at his request.
  See [telemetry.md](ta-notes/telemetry.md). His `assert == 8` will fail; that's expected.

## Next session

1. **Log hours:** run `date` at the opener. He expects to work Wed 2026-09-16 (an off day).
2. **Two live bugs in `validate_robot_timestamps`** — found by running it 09-15, both inside the
   rewrite he already knows is coming. He has been told both:
   - **Wrong row blamed.** The handler attributes to `prev_parsed_line`; the loop walks backwards,
     so `prev` is the innocent earlier row. Reports 235/261 instead of the actual offenders
     238/262. Customer wants the row that arrived out of order.
   - **`del parsed_lines[i]` is unreachable.** Its `except ValueError` is dead code now that the
     custom exceptions subclass `Exception` and the format error is converted. Flagged rows stay
     in the valid set and feed `average_velocity` — the report calls a row invalid while including
     it in the stats. ruff, mypy and the test all stay green on this.
3. **Multi-error collection per row, his next piece.** `validate_parsed_line` still short-circuits
   on `Reading(...)` argument evaluation, so only the first fault per row is reported. He plans to
   do this after reworking the processing order. `MissingDataError` is the deliberate exception —
   a row that can't be split has nothing to validate. Open: whether it belongs under the same base
   as the field errors.
4. **Tests, the week-2 item, still not started.** Upgrade to a **set of line numbers** read off the
   sample file (identity not count; pytest prints the symmetric difference), plus
   `pytest.mark.parametrize` per defect kind on inline strings. Warned against deriving the
   expected set from the validators. Two additions from 09-15: assert the **accepted** count too
   (that's what would have caught the unreachable `del`), and assert the `UnrecognizedError` count
   is zero.
5. **Smaller, all told to him 09-15, none done:**
   - No `from` on any re-raise — chain is discarded everywhere. Offered enabling ruff's `B` rules
     (B904 flags each one).
   - Trailing `\n` from `readlines()` leaks into messages — line 203 renders as `- -273.2\n.`
   - Line 97's message is `Battery was not number. - ` with nothing after it; "was empty" is what
     a tech needs.
   - `NotANumberError("", float_str)` in `validate_float` — the `""` only works because every
     caller wraps and re-raises. Asked what it's for; version exists where the question disappears.
   - `UnknownError` is defined but never raised. He decided (09-15) he wants the quarantine
     bucket, so this needs wiring to a single row-level boundary that logs loudly.
   - `build_report(...) -> dict` is still a bare `dict`; `"bad_readings"` shares a key namespace
     with robot ids. Output shape changed on 09-14 and nothing tests it.
   - Validity limits are magic numbers inline; warning thresholds are constructor-injected. He
     called config out of scope — agreed, but the asymmetry is worth him noticing.
   - ~~Valid ranges not in the README~~ — **done**, he committed them (`6d86f4e`) along with the
     inclusive-velocity and `[-40, 150]` temperature fixes in `validator.py`.
6. **Stage order, still open (his):** timestamp order check runs before the value check, double
   parses, and uses an unchecked row as "previous". Last hint: is "first" an earlier pass or
   earlier in the same iteration? Don't go further unless stuck 30+ min.
7. Still open, his: `-Infinity` for a robot with no good readings; swapped-pair semantics; column
   indexes; `headers_count`; `readlines()`.
8. Rest of week 2: `pdb` (he hit a stray `breakpoint()` 09-15 — tick only after deliberate use),
   CI after tests, README once modules stop moving. `conftest.py` explained 09-14, not built.
9. **ruff is in use and he's responding to it** (BLE001 and T100 both drove real fixes 09-15).
   Offer the `B` ruleset next.
10. **Boss Fight #1:** target Sun Sep 20, spill into week 3 allowed. Strictly hands-off. **If the
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
