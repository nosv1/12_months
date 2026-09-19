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

**Updated 2026-09-18 20:12.**

- Started Wed 2026-09-09. **Week 2.** **24.25 h logged.** Nominal week 3 (C++) start: Mon Sep 21.
- **Boss Fight #1 starts Saturday Sep 19.** Directory scaffolded at
  `boss-fights/01-telemetry/NOTES.md` — rules, permitted inputs, and an empty log. No code, by
  design. **`docs/ta-notes/telemetry.md` is now explicitly out** during the fight: it is a design
  summary plus the defect list, so it's out for the same reason the README is. Told him 09-18.
- **Multi-error collection shipped.** `validate_parsed_line -> Reading | list[TelemetryException]`,
  `BadReading` holds the list, one record per row. **Suite green at 40**, mypy and ruff clean.
- **He changed course on the record granularity mid-design.** His plan was one `BadReading` per
  *value*; §6 says one record per row with a list inside. He took the contract's reading — which also
  left the partition invariant intact.
- **He dropped "exceptions carry line numbers"** after the import-cycle consequence was named.
  `exceptions.py` still imports nothing.
- **`-Infinity` requirements violation found and fixed** (§7). `±inf` seeds now live in loop locals
  with an early return, so they can't reach the dataclass. Verified with
  `json.dumps(..., allow_nan=False)`.
- **Requirements doc gains §8 "How we run it"** (installable, console script on the path) at his
  request, so the packaging half of the fight has a requirement behind it. "Not yet specified" is now
  §9. Matching syllabus week-2 checklist item added.
- Textbook through [16](textbook/16-folds-sentinels-and-where-missing-leaks.md).
- He asked me to **hold the project-manager voice** — he's playing PM himself. Customer voice on
  request, as before.

## Next session (Saturday 09-19 — Boss Fight #1)

1. **Log hours:** run `date` at the opener.
2. **Strictly hands-off.** Rubber-duck only: questions back, no answers, no architecture, no module
   names, no "have you considered". Rules in [telemetry.md](ta-notes/telemetry.md) and in the fight's
   own NOTES.md. **Do not open telemetry.md in his presence** — quoting it leaks the design.
3. **If he asks me to just write it**, remind him once what the exercise is for, then respect the
   call.
4. **Spill into week 3 is allowed.** Cut into week 3 already: README, CI, `pdb`, the
   `test_validations.py` split, and the cosmetic smalls.

## Open, his, not blocking the fight

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
  magic-number limits vs injected thresholds (same `20`/`60` duplicated in conftest); `readlines()`;
  `description = "Add your description here"` still in `pyproject.toml`.
- **Customer questions still unanswered**, §9: can columns be reordered; should a swapped pair flag
  both rows. His to ask.
- Resolved 09-18: `validate_timestamp_order` no longer returns a constant (`a57b142`, his), stray
  `Literal` import gone, `set_analysis_to_none` gone. **`py.typed` added and verified** — a consumer
  outside the tree now gets real type errors instead of `import-untyped`, and `uv build` ships the
  marker in the wheel without any `pyproject.toml` entry.

## Standing instructions

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
- **Textbook entry whenever a real lesson is given.**
- **I play the customer** for telemetry requirements questions — see telemetry.md.

## How to work with him — the short version

Lead with the answer. Mechanics get direct answers; design stays his. "Feels gross" from him is
usually right — ask him to name it. Name weak reasons plainly. Answer venting with accuracy, not
reassurance. One-word replies mean he's tired: park decisions. Details in
[observations.md](ta-notes/observations.md).
