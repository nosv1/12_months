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

**Updated 2026-09-20 12:14.**

- Started Wed 2026-09-09. **Week 2 ends today.** **34.75 h logged.** Week 3 (C++) starts Mon Sep 21;
  he wants **a light day tomorrow** first.
- **Boss Fight #1 is over.** Built 09-19 (6h29m) and 09-20 (3h09m) — **9h38m against a 6h
  estimate, 1.6x**. Backing out ~1h of header work beyond the original scope gives ~1.4x on
  equivalent scope. That is a different regime from the 3x factor he'd been applying; one data
  point, not a recalibration.
- **Dashboard marks it ◐, not passed.** He hasn't been asked to accept or dispute that — it's his
  call and it's still open.
- **Fight result:** rebuilt from empty — reader, parser, validator, grouper, robot, report, console
  script, 38 tests. §1-§6 largely hold: multi-error rows, original line numbers, raw `original_line`,
  the truncated row correctly unattributed, order-independent header parsing.
- **Review written into `boss-fights/01-telemetry/NOTES.md`**, six findings, all verified by
  running the tool. He fixed #1 (robots were anonymous in the report) during the session. **Still
  open: #2 the installed artifact is a stale `uv tool install` copy printing a dict repr instead of
  JSON, so §8 currently fails; #3 a bad header silently discards the whole file, exit 0; #4 an empty
  `robot_id` becomes a robot; #5 `to_json` substitutes `datetime.now()` and `-1` when an isinstance
  check fails; #6 a missing input file exits with a raw traceback.** Plus §5's `20`/`60` still
  needing a source edit and reinstall.
- **Textbook 17 and 18** written at his request — installed artifacts as snapshots, and union-typed
  fields / who owns exception context. 18 came from two design questions he raised himself, both
  good.
- He planned to spend a hypothetical extra day on "the gross bits". Told him I'd reorder that:
  correctness first, shape sixth. Not re-litigated.
- **Hands-off held** through the fight, with one slip: read "ty" as "type" and handed him
  `type[...]` when he'd already thanked me for the hint. Offered to log the assist; he moved on.
- He asked me to **hold the project-manager voice** — he's playing PM himself. Customer voice on
  request, as before.
- **`docs/ta-notes/telemetry.md` is back in bounds** now the fight is done.

## Next session (Mon 09-21 or whenever he returns — light day)

1. **Log hours:** run `date` at the opener.
2. **Normal rules resume.** The fight is over; critique, review and explanation are all back on.
   Still his design, still no implementation code for the week's learning objective.
3. **A light day has a natural shape:** finish the fight's open findings (#2 and #3 first), or
   close week 2's spillover (README, CI, the `pdb` item), or start week 3 gently. His pick — don't
   stack all three.
4. **Week 3 is C++.** First genuinely new material since the year started, and the first place the
   confidence gap will show up. Be accurate about difficulty rather than reassuring.

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
