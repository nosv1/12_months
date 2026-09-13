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

**Updated 2026-09-12 22:45.**

- Started Wed 2026-09-09. **Week 2 in progress** (started early, Sat evening). **11.5 h logged.**
  Nominal week 3 (C++) start: Mon Sep 21. Not behind.
- Week 1 done and verified. C++ toolchain installed and verified.
- Telemetry is mid-redesign, by him: `ParsedLine` (`parser.py`) → `validate_parsed_line`
  (`validator.py`) → loop in `cli.py` "for now". 2 tests, mypy clean, all 8 defects caught.
- Textbook through [07](textbook/07-circular-imports.md).

## Next session

1. **Log hours:** run `date` at the opener.
2. **Where `parse_telemetry_lines` lives and what it's called.** He tried `preprocessing`,
   `processor`; I pushed that both are too broad. His call. Settle before tests (imports depend on it).
3. **Tests for `ParsedLine.parse_line` and `validate_parsed_line`** — the reason for the redesign.
   Test-first suggested. Then `parametrize` over the defects.
4. Still open, his: column indexes in `ParsedLine` vs `main` vs read from the header row; hidden
   header-skip rule (`headers_count`); `readlines()` in `main`; `report()` mixes JSON with file I/O.
5. Rest of week 2: `pdb` (tick only after real use — `breakpoint()` / `pytest --pdb`), CI after
   tests, README once modules stop moving (stranger test; I hold a gap list).
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
