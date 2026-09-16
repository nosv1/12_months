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

**Updated 2026-09-16 18:40.**

- Started Wed 2026-09-09. **Week 2 in progress.** **20.05 h logged.** Nominal week 3 (C++) start:
  Mon Sep 21. Not behind on hours; the boss fight is still the thing at risk.
- Week 1 done and verified. C++ toolchain installed and verified.
- Last commit is `5fb53c2`. **Everything from 09-15 and 09-16 is uncommitted and his** — he said
  he'd commit after me both nights. Do not sweep it into a Claude commit.
- **2026-09-16: the test suite, all his.** 29 tests. Parametrized accepts/rejects tables for
  velocity, battery, temperature, timestamp format, and column count; boundaries at both ends with
  `pytest.param(id=...)`; `inf` covered. `test_all_defects_caught` now compares a **set of
  `(line_number, error_name)` pairs** against nine hand-read line numbers — symmetric-difference
  diff, both directions. Closed at **1 failed, 28 passed**, the red being the deliberate 235/238.
- **He fixed the `del` bug himself.** Partition verified by running it: 361 in, 353 good, 8 bad,
  no overlap. It works via a guard that fires a lap late — load-bearing coupling to the
  attribution bug, which he knows.
- **`MissingDataError` → `ColumnCountError`**, after a customer answer. `NUM_COLUMNS` moved out of
  `ParsedLine`; `parse_lines` now derives it from the header row.
- Textbook through [12](textbook/12-exception-chaining-and-lint-rulesets.md).

## Next session

1. **Log hours:** run `date` at the opener. Session ended 09-16 at 1840.
2. **The accepts side — his stated next item.** "idk how to test accepts yet", parked deliberately.
   Nothing in 29 tests asserts anything about the 353 good rows, which is exactly where the `del`
   bug lived. Start here. He may need the partition invariant restated as a concrete assertion
   shape, but let him get there.
3. **`validate_timestamp_order` has no unit tests** and is the next function he rewrites. Three
   direct tests (ordered pair, out-of-order pair, identical pair) before he touches it. Raised
   09-16, not done.
4. **Attribution bug is the live red.** 235/261 blamed instead of 238/262. The test now states it
   in both directions. This is the fix that turns the suite green.
5. **Two tautological accepts tests**, told to him 09-16:
   `validate_timestamp_format(v) == datetime.fromisoformat(v)` and
   `validate_velocity(v) == float(v)`. Expected values must be hand-written literals.
6. **ruff config does not exist in the repo.** `uv run ruff check .` passes while his editor
   extension fires BLE001/T100. Told him 09-16; fix before CI. `select = [...]` in
   `pyproject.toml`, `B` and `C4` both earning their keep already.
7. **`parse_lines` findings from 09-16, his to act on:** `lines[0]` on an `Iterable[str]` (mypy
   flags it), read before the `headers_count` check, `IndexError` on an empty file, stale
   `"was missing data"` log string, `test_incorrect_column_counts` missing `-> None`, `""` absent
   from every reject table.
8. **Multi-error collection**, still his next design piece. `validate_parsed_line` short-circuits
   on argument evaluation. When it lands, the test's expected shape goes from `line -> error` to
   `line -> {errors}` — line 363 carries three faults.
9. **Smaller, all still open:** no `from` outside the field validators; trailing `\n` in messages;
   `NotANumberError("", ...)` empty first arg; `UnknownError`/`UnrecognizedError` never raised;
   `build_report -> dict` untyped and untested; magic-number limits vs injected thresholds;
   `-Infinity`; swapped-pair semantics; `readlines()`.
10. **Stage order, still open (his).** Last hint given: is "first" an earlier pass or earlier in
    the same iteration? Don't go further unless stuck 30+ min.
11. Rest of week 2: `pdb` (not yet used deliberately), CI, README, splitting
    `test_validations.py` into parser/validator/pipeline files.
12. **Boss Fight #1:** target Sun Sep 20, spill into week 3 allowed. Strictly hands-off. **If the
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
