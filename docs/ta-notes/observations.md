# How to work with him — learned, not in CLAUDE.md

Back to the [TA notes index](../ta-notes.md). Read before a pushback or confidence conversation,
and at the Sunday review. Add dated observations at the bottom; promote patterns to the top.

---

## Patterns (stable)

**Verify before advising.** When he reports something done, check the actual state with bash
first. On day 1 every such report was partially incomplete:

| Reported | Actually |
| --- | --- |
| "git init done, dev branch created" | no commits, no `.gitignore` |
| "committed" | only `telemetry/` — `git add *` from a subdirectory; the shell expands `*`, skipping dotfiles |
| "`.gitignore` fixed" | patterns path-anchored, so nested `__pycache__/` wasn't matched |

Not carelessness — the small tooling detail that never announces itself, which is the gap Part 1
exists to close. **Name what's wrong and why it matters; don't fix his repo for him.**

**Verify my own claims too.** 2026-09-12 I told him input was streamed; `readlines()` was still
there. Check before summarising his work back to him.

- **Defends first, then changes course** when the reason is better — sometimes with a weak reason
  ("flexibility", "perhaps"). Name the weak reason plainly; "could you defend this in an
  interview?" lands. So does "you're allowed to overturn my earlier pushback if your reason is
  better."
- **His design instincts run ahead of his vocabulary.** "Feels gross" has been right every time
  (warnings lacking timestamps, `validate()` on `ParsedLine`, the loop in `cli.py`). Ask him to
  name what's gross rather than naming it for him.
- **Moves fast, edits piecemeal** → self-contradicting docs (day 2 design doc; 2026-09-12 docstring
  vs `headers=1`). Advice that works: reread top-to-bottom; let type-checked code carry the design.
- **Ticks run slightly ahead of evidence** (git ticked before asking how to structure commits;
  pathlib ticked while `os.path.join` remained). Not dishonesty. He self-identified the
  checklist-rush mindset on 2026-09-12 — reinforce the "could redo it from scratch" bar.
- **Mechanics questions get direct answers** (exception messages, `__init__.py`, `Iterable`).
  Design decisions stay his.
- **Review at decision points** is what he should ask for; he was hesitant to ask "check my work."
  Keep inviting it.
- **Fatigue signal:** one-word answers ("maybe"), keyboard mashing. Stop asking him to decide
  things; park the question in the week file and wrap up.
- **~2 h ceiling is decision density, not stamina.** Unprompted 2026-09-15: not burnt out, looks
  forward to the evenings, but "it's just hard to continuing fixing things for more than 2 hours a
  time ... if it was smooth sailing, i could prob keep going, it's just constant thought right
  now." Accurate self-read — that session was ~100%% novel decisions and debugging, zero mechanical
  work, which is the expensive kind. Don't treat the 2 h as a limit to fix. Two levers if a session
  needs to run longer: put something mechanical in the middle, or bank a decision for tomorrow
  rather than making it tired.
- **Confidence:** answer venting with accuracy, not reassurance ("yes, a little rushed; here's the
  fix"). Point at verified evidence (e.g. "refactor kept all 8 defects caught").
- Limited evening hours. Lead with the answer.

- **Prior robotics beyond Gazebo** (told me 2026-09-24): a graduate **path planning** course,
  "one of the most fun classes i've ever done", and hands-on **ArduPilot** drone waypoint work.
  Calibrate Part 5 (navigation, wk 16–19) and Part 3 like the DS material: jog, don't re-teach
  the algorithms; teach the ROS 2 / Nav2 plumbing around them. MAVLink is a live example for
  week 7 (serialization, UDP). This is the part of the year he's looking forward to; use it.

## Things to watch

- Commits: one idea each since week 2 started (`862cc49`/`284ad5a` duplicate message aside). Keep
  noting.
- Whether he writes `parametrize` cases himself or tries to hand them off. He pushed back
  2026-09-12 that "AI writes tests faster"; answered that AI types them, deciding what counts as
  wrong is the skill.
- Estimates vs actuals, first Sunday comparison Sep 13/20.
- **Week 3:** he called `#include` "kinda wild". Feed that curiosity (`g++ -E`, the link stage).

## Dated log

- **Day 2 (09-10):** hesitant to ask for review; took warnings → analysis pushback; vented "maybe
  I'm rushing". Suggested markdownlint. Explained commit messages as what/why.
- **Day 4 (09-12):** asked *why* before accepting a design (warnings placement) — encourage.
  `384a15d` bundled three ideas; taught `git add -p` after.
- **09-12 late:** raised "sessions feel unproductive without coding" and "checklist as fast as
  possible" himself. Asked for a 0–10 skills rating — offered per-skill with evidence instead; not
  taken up, don't push. Drove a full parser redesign mostly on his own instincts.
