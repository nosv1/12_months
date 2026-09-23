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

**Updated 2026-09-23 13:07.**

- Started Wed 2026-09-09. **41.83 h logged.** Two sessions today: 08:32–09:37 and 10:58–13:07.
- **Week 3's six checklist items are covered.** Still not ticked — see below.
- **`cpp_telemetry/` exists and runs.** CMake, `Reading` with a member initializer list,
  `to_string()` via `ostringstream`, CSV read into `vector<vector<string>>`. Parsing loop is
  mid-flight; he stopped tired, with the next steps clear to him.
- **He adopted strong types unprompted** — `Timestamp`, `RobotID`, `Velocity`, `Battery`,
  `Temperature`, each wrapping one field — after I mentioned them as out-of-scope-but-worth-knowing.
  Real design move, kills the swapped-same-typed-arguments hazard. Also more machinery than the SPEC
  called for; I told him to keep it only if he can defend it, and he can. Watch it for drift.
- **It also made his design decision for him by accident:** conversion now happens in constructors,
  so `std::stod` throws from inside `Velocity`. Exceptions are in the design whether or not he chose
  them. Raised as a decision to make deliberately (throw/catch, `optional`, `from_chars`, or a
  factory); he has not chosen yet. This is design question 3 and it's still his.
- **Three bugs hit and diagnosed today**, all first encounters: the most vexing parse; an uncaught
  `std::invalid_argument` (the CSV header row) found with gdb `catch throw`; a segfault from
  unchecked `operator[]` on the truncated row at line 301. Textbook 22 covers all three.
- **Tooling added (mine):** `.clang-format` (Google/ROS 2, his choice), `.vscode/settings.json` with
  format-on-save. `clang-format` CLI not installed — needs `sudo apt install clang-format`, which I
  can't run.
- **Boss Fight #1 still ◐ on the dashboard**, still neither accepted nor disputed.

## Next session

1. **Log hours:** run `date` at the opener. Log any estimate given in `estimates.md`.
2. **His code is uncommitted** at sign-off: `cpp_telemetry/{main,reading}.cpp`, `reading.h`,
   `CMakeLists.txt`, `data/`, `.gitignore`. His to commit, not mine. Ask at the opener.
3. **Pick up mid-parse-loop.** Remaining: skip the header, handle bad rows, `ParseResult`,
   per-robot min/max/mean, summary output. He said the next steps "seem simple" — that's a
   prediction worth checking against how long they take.
4. **Design question 3 is still open** and he is now inside it. Don't answer it. The options are
   named in textbook 22; let him pick and defend one.
5. **Guard the scope cap.** He asked for a config file at 11-ish and accepted "write it down, don't
   build it." That list is in `cpp_telemetry/SPEC.md` and should grow with his additions.
6. **Do not tick week 3 until `cpp_telemetry/` runs end to end** with a README he wrote.

## 2026-09-23 — what worked

**Afternoon session, 10:58–13:07.**

- **He designed first, then coded, and it held.** The three SPEC questions got real answers over the
  haircut. His answer to #1 (vector of pointers) had the cost model inverted — "what if n is large"
  argues *for* contiguous values — and he took the correction without defending the original.
- **Strong types were his idea, from a throwaway line of mine.** I named them as an out-of-scope
  technique for the swapped-doubles hazard; he built them. First time this year he has taken a
  design idea and run with it unprompted. Worth noting on the confidence ledger.
- **`catch throw` landed the same way `breakpoint()` did.** He was hopping frames by hand and stuck
  on empty `info locals` in a constructor — `info args` was the missing half. The pdb parallel
  (textbook 19) is exact and worth naming to him next time.
- **He found the header-row bug himself** once pointed at the tool, and predicted the bad rows
  coming next. "lmao, it's the header line, forgot to skip."
- **Scope held once.** He wanted a config file; "write it down, don't build it" was accepted without
  argument. The SPEC's out-of-scope list is doing its job.
- **Frustration showed twice** — "im losing my mind" (most vexing parse) and "hard to find the
  error" (segfault). Both were genuinely hard first encounters, not him being slow. Said so, briefly,
  and moved to the mechanism rather than reassuring. Correct call; MVP defeats experienced people.
- **He called the stop himself** at 2h09m into the second session, with next steps clear. Good
  judgment, not a stall.


- **Predict-then-run, again, every time.** Every insight came from a wrong prediction written down
  first: the empty copy-constructor body, `Reading b = a` as a stored recipe, and `r = j` predicted
  as `1, 2, 2`. He is not precious about being wrong when the guess is on record. This is the format.
- **He called out my verbal tic** — "can't wait for you to say 'you're half right, but the bit
  you're wrong on will bite later'". He was right; I'd used that shape three times. Dropped it. Worth
  noticing that the framing had become a formula he could predict, which makes it stop landing.
- **Verifying his "fixed fixed" caught a miss.** He'd deleted the broken copy constructor rather than
  fixing it, which made the symptom go away and threw out the instrument. Reading the file took
  10 seconds. Keep doing this — two of Monday's misses were exactly this shape.
- **Checking GCC's actual output twice changed what I wrote.** The dangling reference segfaulted
  rather than printing stale bytes; the address turned out to be `0`, GCC having replaced the code
  outright. I had been about to tell him the stale-bytes story. Also verified the `discards
  qualifiers` wording rather than quoting from memory.
- **His Rust background is a live asset.** He reached for `mut` unprompted when explaining `const`,
  and the C++/Rust default inversion landed immediately. Use Rust as the bridge for ownership and
  lifetime in week 4; it will be cheaper than teaching from Python.
- **"goodnes so references are kinda dangerous"** needed correcting, not agreeing with. The hazard is
  lifetime, not references — a pointer dangles identically and can also be null. Left him with the
  parameter-safe / returned-or-stored-is-the-risk rule.

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
