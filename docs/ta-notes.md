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

**Updated 2026-09-21 18:52.**

- Started Wed 2026-09-09. **36.55 h logged.** Calendar week 3 began today; the evening went on
  closing week 2's deliverable, as planned. **Week 3 (C++) starts next session.**
- **Week-2 deliverable closed 09-21.** `telemetry/` README rewritten by him against the code over two
  review rounds (62 min). CI (`.github/workflows/telemetry.yml`, mine) green on GitHub Actions:
  `uv sync --locked`, ruff (no `--fix`), mypy, pytest, one sample run via `uv run`, then **§8 as the
  customer**: `uv tool install .`, run by name from `$RUNNER_TEMP`, strict JSON parse (`4bbcef2`, green). He answered four of five
  review questions; #4 (editable vs installed) he got on the second prompt, cleanly.
- **Syllabus ticks — at his call, Monday rather than Sunday:** pytest, pdb, I/O separation, README,
  CI. **Left open: "project setup from empty, unaided"**, because the fight has no `py.typed`. His
  debugger use is his account (`breakpoint()` + `n` + inspecting); textbook 19 covers `s`/`w`/`u`,
  `pytest --pdb`, and conditional breakpoints. First real use of `--pdb` will be worth noting.
- **Estimates log started** at his request: [ta-notes/estimates.md](ta-notes/estimates.md). Tonight:
  README 1.2x mine / 2.1x his; CI review 0.6x mine. Too few entries to conclude anything.
- **Boss Fight #1 still ◐ on the dashboard**; he hasn't accepted or disputed it. Fight finding #2
  (stale artifact): he reinstalled, checked the output and uninstalled on 09-20 (his account, shell
  history agrees). #3–#6 open in `boss-fights/01-telemetry/NOTES.md`.
- **`json.tool` and `json.loads` accept `-Infinity`** — found writing the CI customer step; textbook 17
  corrected. Worth remembering for the `-Infinity` test still open below.
- **Two misses of mine tonight, same shape:** gave him a ship task he'd already done (checked
  `uv tool list`, not history), and pinned `setup-uv@v10`, a tag that doesn't exist, which failed
  CI's first run. Both came from checking something *near* the fact instead of the fact itself.

## Next session

1. **Log hours:** run `date` at the opener. Log any estimate given in `estimates.md`.
2. **Week 3 step 5 is next: references vs pointers vs values, and `const` correctness.** The only
   untouched checklist item, and the hardest — it is where copies, dangling references and `const`
   actually bite. Everything else in week 3 was covered 09-22. Make copies *visible* (a printing
   copy constructor) the same way destructors made lifetime visible; that framing worked.
3. **No real C++ has been written yet.** Everything so far is a toy `Reading` in untracked
   `cpp_test/`. The week-3 vehicle — a thin telemetry port, one file, one struct, one summary —
   is still unwritten, and that is where any of this consolidates. Scope cap matters: week 2 was
   eaten by exactly that kind of growth.
4. **Do not let him conclude week 3 is done.** He noticed the pace himself ("kinda changes the
   timeline"). Steps 1–4 took 2.05h against my ~7.5h, but the session was guided throughout — the
   ODR diagnosis, the out-of-line syntax and the `static` catch were all mine. Recognition is not
   recall; boss fight #2 (week 7) is the honest test.
5. He wants to fix `telemetry/` with ideas from the fight. His README's "What's next" section holds
   that list now. Don't let it eat C++ time, but don't block it either.

## 2026-09-22 — what worked

- **He named the failure mode himself:** *"this was a teacher showing commands and their outputs and
  a student being like mmm yes, interesting, it's hard to make sense of it without a reason to make
  sense of it."* Correct, and it was the turning point of the session. Demos → a build he had to
  make work. Everything good after that came from tasks with a predict-before-you-run step.
- **"mmmm interesting" is his tell for passive watching.** He used the phrase twice; the second time
  naming it back to him converted the moment into a 30-second action. Watch for it.
- **Predict-then-run is the format that works.** Every real insight tonight came from a wrong
  prediction: the constructor undefined reference, `static` hiding the linker error, `goodbye c`
  never printing, LIFO destruction order. He is not precious about being wrong when he wrote the
  guess down first.
- **Environment papercuts: just fix them.** The Windows Caps Lock OSD was Logi Options+, found in
  30 seconds via `powershell.exe Get-Process` from WSL. He responded "omg tysm". That is the
  correct division of labor and he feels it.
- **I over-estimated the clock three times** (19:05, 19:15 when it was 19:09). Run `date`. Every
  time. Standing instruction, broken three times in one session.

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
