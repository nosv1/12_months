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

**Updated 2026-09-13 15:30.**

- Started Wed 2026-09-09. **Week 2 in progress.** **14.0 h logged.** Nominal week 3 (C++) start:
  Mon Sep 21. Not behind.
- Week 1 done and verified. C++ toolchain installed and verified.
- Telemetry redesigned into stages, by him (`b830018`): `read_file` (`reader.py`) → `parse_lines`
  → `group_robots` → per-robot `validate_robot_timestamps` then `validate_parsed_line_values` →
  analysis → `report`. `main(path, out)` is only function calls; `cli()` does argparse. Rejected
  rows are `BadReading(line_number, original_line, err)`; unparseable rows go in a top-level
  list, no `"unknown"` robot. Verified at close: all 8 defects reported, console script works,
  mypy clean, 3 tests pass. **One of the 3 has no assertion** (see below).
- Textbook through [08](textbook/08-pipeline-stages.md).

## Next session

1. **Log hours:** run `date` at the opener.
2. **Stage order, still open (his):** the timestamp order check runs before the value check, so
   the format gets parsed twice, a malformed timestamp gives up to 3 `BadReading`s, and an
   unchecked row can be "previous." My last hint: the order check needs the `datetime` the value
   check produces. Is "first" an earlier pass or earlier in the same iteration? Don't go further
   unless he's stuck 30+ min.
3. **`test_all_defects_caught` asserts nothing** and depends on cwd (`Path.cwd() / "data/..."`,
   writes to `telemetry/output/`, which is gitignored). Passing it proves nothing. Ask him what it
   should check. It should have caught the dropped-truncated-row regression earlier today.
4. Still open, his: `-Infinity` in JSON for a robot with no good readings (customer complaint);
   who serializes `BadReading` (`Analysis.to_json` knows its fields); swapped-pair semantics
   (forward vs backward walk); column indexes; `headers_count`; `readlines()`.
5. Rest of week 2: `pdb` (tick only after real use), CI after tests, README once modules stop
   moving (stranger test; I hold a gap list).
6. Offered `ruff` setup (mine, tooling). Not accepted yet.
7. **Boss Fight #1:** target Sun Sep 20, spill into week 3 allowed. Strictly hands-off.

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
