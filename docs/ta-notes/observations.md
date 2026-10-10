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
  Calibrate Part 5 (navigation, wk 18–21) and Part 3 like the DS material: jog, don't re-teach
  the algorithms; teach the ROS 2 / Nav2 plumbing around them. MAVLink is a live example for
  week 7 (serialization, UDP). This is the part of the year he's looking forward to; use it.
- **What he enjoys is optimization** (2026-09-24): "it was just fun to write code that solved a
  problem the best it could" — path planning, and a genetic algorithm for class scheduling. Points
  at planning/optimization as a lane (motion planning, trajectory opt, multi-robot task
  allocation). Bring up at the capstone scope decision; watch whether Parts 5 and 10 light him up.
  Also his own framing of the career worry: likes writing code himself more than directing AI.

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
- **09-26:** his own read on stamina: *reading/explaining ~1 h a stint, 2 h max; pure coding
  3–4 h.* Said after three prediction-heavy days (09-24/25/26) felt like "a lot of reading." Plan
  sessions around it: front-load the concept, then hand over a build. Links to 09-12's "sessions
  feel unproductive without coding" — the same signal, now with numbers.
- **09-27 (car ride, not work time):** background I didn't have. **BS CS 2020 → rejected by
  SpaceX → about a year away from CS → MS** while working in a **drone research lab**. Public-release
  description, his words: **modeling and simulation developer for base defense**, working out
  the best way to defend a base with a given set of effectors. Side projects: ArduPilot and
  waypoint navigation. **Details are classified. Don't probe past the public version.** That
  work needed a **Secret clearance**, now
  inactive after 2+ years unused. That changes the calibration: his aerial-sim background is more
  than "ArduPilot waypoints." Base defense with effectors is an allocation/optimization problem, the
  **fourth** optimization data point, and it's a résumé line for defense autonomy.
  - **His rule, and it's right: a specific company is not a goal.** Someone else's decision is
    outside his control, so it's a setup for disappointment. I had framed SpaceX as "the target"
    and he corrected it. Aim at capabilities and directions (aerial autonomy, planning and
    optimization, defense and aerospace), never at employers.
  - Would not join the military even with a SpaceX offer in hand, so that idea is closed. He'd be
    "scared shitless" to work at SpaceX today. Treat that as an accurate read of week 5, not a
    permanent one. Answer it with evidence as it builds up, not with reassurance.
  - Optimization pattern, **four data points** now: base-defense M&S, path planning, the GA class scheduler, and a
    drone-fleet optimal-routing problem from applied calculus. Also follows BPS Space. Parked idea:
    a grounded TVC test stand (ESP32 + IMU + servo gimbal) as a weeks 8–9 side project.
- **Hardware nerves (09-29).** Soldering is a named worry, alongside the bench kit sitting unordered
  since 09-28 with low energy for it. Same pattern as C++: unfamiliar reads as "can't." Answer with
  the concrete scope (one row of header pins) and a cheap way to fail safely (practice kit), not
  with "it's easy." Evidence arrives after the first practice board.
- **"Pick one that seems right," then graded by convention (09-30).** He picked `length_error`
  then `domain_error`, each with sound plain-English reasoning, and got corrected twice. His
  pushback was right. When the answer is convention, **say it's convention up front**, or just
  give it — mechanics get direct answers. Asking him to derive something that can't be derived
  reads as a trap, and it costs trust.
- **Checklist vs application (09-30).** "I feel like I'm mixing requirements for the sensor buffer
  and C++ learnings together." Forcing syllabus features into the app produces bent designs, then
  a feature he learned gets dropped, and that reads as wasted effort. Proposed standalone drills;
  awaiting his answer.
- **He derives more than he credits himself for.** 09-30, unprompted: fail fast in the ctor,
  `CMAKE_SOURCE_DIR` pointing at the consumer, the copies in `get_ordered_readings`, "the consumer
  only needs the library." Same day: "one day i'll understand this shit." The gap he feels is
  lookup syntax, not judgement. Point at the specific instances, not at general encouragement.
- **Curiosity outside the syllabus (10-07).** Watched a Kurzgesagt video, came in wanting to talk
  gravity-assist trajectory planning (the long braking sequence in *Aurora*). Gave keywords:
  Lambert's problem as a steer function, flyby-sequence search, GTOC, kinodynamic planning,
  underactuated robotics (Tedrake). He declined a write-up — "just sharing thoughts." Interest in
  the field is alive even after a quiet week. Don't turn it into homework; if Tedrake fits a later
  control/planning week, mention it once there.
- **Robotics as a placeholder (10-10, phone).** "That pursuit was just something to get me by in a
  time where I had no projects." The origin was FOMO (an NVIDIA video, "get on that train"), not a
  pull toward the work. Stalled on the kit purchase, questioning his motivation, no light at the
  end of the tunnel. Interest in building things is intact: three side-project ideas in a week
  (orbital, bowling, iRacing engineer). So the problem is the frame, not his ability or drive.
  Don't defend the syllabus for its own sake. The CLAUDE.md goal is employable capability plus the
  confidence of having built things that work, and projects he actually wants to build can serve
  that. Help him make it a decision, not a drift.
- **Design over building (10-10, phone).** His words: he enjoys "the heck out of thinking through
  the whole problem" but rarely finishes, because "I've already thought of the whole solution" and
  the thing isn't needed. Example: the unfinished grad-class project, a goal-seeker robot evading
  2–3 detector robots (pursuit-evasion / covert path planning; the mirror image of his base-defense
  work). This explains a lot: the kit stall, energy for ideas, low energy for execution weeks. Push
  back gently on "whole solution": the bugs he found this year (`-Infinity`, the conftest double
  run) were all invisible until built. Finishing is also the only thing that answers the confidence
  gap. Don't moralize; it's fine if some ideas stay thoughts.
- **Buy to test, not to learn (10-10, phone).** His hypothesis: hardware might appeal once a
  simulation works and raises "does this work in real life?", in contrast to the kit, which was
  buying to learn. Examples: rocket launch/landing (ties to the parked TVC stand), robots for the
  goal-seeker. He's unsure whether "saw it work in sim" will kill it like "saw it in my head" does.
  Unresolved. Test it by building the sim first and noticing. Don't sell hardware.
- **Calibration from his GitHub (10-10).** 37 public repos under `nosv1`. The 2022 class
  (ME5501) was **ROS 2 + Gazebo + TurtleBot3**, not just "Gazebo exposure": he wrote nodes, lidar
  object detection, PID and PN controllers, pursuit-evasion, and A* / Dijkstra / RRT / Dubins / GA-TSP
  in Python. **So syllabus Parts 4–5 (ROS 2, planning) are partly review**, and CLAUDE.md's "some
  prior exposure: Gazebo" undersells it; propose the edit to him. Also: `sra-insights`, a live
  React/TypeScript web app for his sim-racing league (pushed May 2026), `F1-Schedule-Optimizer`
  (another optimization data point), an ACC UDP interface fork, SimHub plugins, an ArduPilot fork,
  UAV-Sandbox. The ACC race engineer isn't public. Ask where it lives.
