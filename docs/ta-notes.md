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

**Updated 2026-10-07 10:27, signed off.** **59.77 h logged** (10-07 not counted, his call). Session log:
[week-06.md](ta-notes/sessions/week-06.md). ~11 days ahead of the calendar.

- **10-07 (work off day): 10-02 to 10-06 was an off period**, partly to avoid the kit question.
  The kit and the build log are both dropped; see decisions.md 2026-10-07. **Week 5 ticked**, after
  re-verifying (11/11 tests, consumer builds). Current week: 6. He finds Linux internals
  unexciting but doable.

- **10-10 (phone, Saturday): curriculum future open.** He said robotics was "something to get me by"
  while he had no projects. He's unsure about continuing. New side-project idea: iRacing race engineer
  ([docs/ideas/iracing-race-engineer.md](ideas/iracing-race-engineer.md)). No decision made. See
  observations.md 10-10. **Signed off energized** after reframing: backbone project instead of a
  checklist, and hardware bought to test a working sim rather than to learn.
  **By the end of the call, three projects, each with a reason:** race engineer (leads, "useful and
  fun"), stealth robot (mood days), motorcycle telemetry (hardware with a reason; may replace the
  kit). Ideas in [docs/ideas/](ideas/). His goal may be race strategy work, not a robotics job; see
  observations.md 10-10. CLAUDE.md profile updated from his GitHub and career history.

- **Off days are now real**: Fri 10-02 off. Running ~19 h/week, 22 days straight before today;
  enthusiasm dropping. Watch hours, not just progress. See decisions.md 2026-10-01.
- **Critique tags in force**: fix now / noted / taste; taste stays out of chat. Agree tonight's
  "done" at the opener.
- Week-5 loose ends, tagged: **noted** — `-Wall` inside the top-level guard; `emplace` with a
  temporary. The other three are taste; don't raise.

## Week progress — render this as the session opener

```text
Week 5 · STL and idiom   ██████████████████  5/5 (unverified)   day 7 of 7 (started 09-26)   left: verify + tick
  ✓ vector, unordered_map, string_view, optional   — string_view tb 37; optional tb 36
  ✓ iterators + <algorithm>                        — accumulate + lambda (tb 36)
  ✓ templates (reading)                            — SensorBuffer<T> (tb 33)
  ✓ exceptions vs error codes                      — invalid_argument in ctor, EXPECT_THROW (tb 34)
  ✓ build a library, link it from another project  — w05-consumer, add_subdirectory (tb 35)
```

Items are the syllabus checklist for the week; ◐ counts as half. Syllabus ticks still wait for
verification, so this block is the mid-week state. Update it at sign-off with the session log.
When the remaining work fits in one session, **say so up front**. **"Week length" is not a
deadline** — he read "day 4 of 7, tight" as falling behind (09-29). Say where he stands against
the calendar if it's ambiguous.

## Next session

1. **Ask where he landed on the curriculum** (10-10) before assuming week 6. Continue, reshape
   around projects, or stop: all fine. It should be a decision.
   **Later on 10-10 the race engineer took the lead** ("useful and fun"; he'll use it as long as he
   races). **His call: keep both open; pick by mood.** But once the engineer is started he'd stay on
   it until it's useful. The robot is "fun in my head, then 'you did a good job, whatever.'" Help
   him define "useful" as a concrete first milestone. Still open: does the robotics curriculum continue?
   He wants race strategy work someday. Ask whether he pushed the ACC code.
   Earlier lead candidate: **the stealth goal-seeker from his grad class**, which he'd "enjoy the
   heck out of" as a curriculum project. He'll bring the original project details.
   [docs/ideas/stealth-goal-seeker.md](ideas/stealth-goal-seeker.md).
2. **Week 6** (processes, fork/exec, threads) if he comes back for it. Agree "done" first.
3. **Side projects**: orbital (active) or iRacing engineer (idea, 10-10). **Orbital side project**, if he chooses it: flight-instructor mode, and his hours aren't logged.
   State in [week-06.md](ta-notes/sessions/week-06.md).
4. **Global profile, researched 10-10 (docs, not guessed):** cloud sessions do **not** read a user
   `~/.claude/CLAUDE.md`; they read only what's in the clone. Two supported routes: (a) a **setup
   script on his cloud environment** that writes `~/.claude/CLAUDE.md` (loaded as user instructions in
   every cloud session, phone included); (b) **Projects** (beta, Pro/Max, rolling out): one
   conversation across several repos, with shared instructions (16k chars) and project memory, usable
   on mobile. Proposed: 12_months becomes the hub (profile, TA notes, ideas); each project gets its own
   repo with a short CLAUDE.md pointing at the hub. **Privacy answered: public is fine** ("my resume
   is public enough"). **Still open:** is Projects in his sidebar? Gist of the hub plan approved; build
   it at a keyboard.

**Keep replies short.** Put the task in the **final** message, never mid-turn.

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

- **Open every session with the week progress bar** (block above): items done/total, day of the
  week, my estimate of what's left. Asked for 2026-09-26 — the remaining-work picture should come
  at the start, not as a surprise "that's the week" at the end.
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
- **Tag every critique: fix now / noted / taste.** Taste never goes in chat. Agree tonight's "done" at the
  start; stop there. See decisions.md, 2026-10-01.
- **Textbook entry whenever a real lesson is given.**
- **I play the customer** for telemetry requirements questions — see telemetry.md.

## How to work with him — the short version

Lead with the answer. Mechanics get direct answers; design stays his. "Feels gross" from him is
usually right — ask him to name it. Name weak reasons plainly. Answer venting with accuracy, not
reassurance. One-word replies mean he's tired: park decisions. Details in
[observations.md](ta-notes/observations.md).
