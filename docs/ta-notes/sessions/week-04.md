# Week 4 — Memory and ownership

Session notes moved out of [ta-notes.md](../../ta-notes.md) once they stopped being needed every
session. Newest last.

---

## 2026-09-24 — first evening, 17:20–18:08

- **I opened with a step he'd already done** (ctor/dtor + leak, done 09-22). He caught it: "we've
  done this in the previous week i feel." The hours log said so; I planned from the syllabus
  instead of the log. Check the hours lines before proposing a step.
- **"im so confused with what we're trying to do 😅"** — I'd given a numbered procedure with no
  *why*. The reframe that landed: one story in three acts (break it → catch it with a tool → make it
  impossible), plus a Python contrast (GC). Lead with the story for any new week.
- **Every step ran predict-then-run and it carried the session.** Wrong predictions, all productive:
  "more warnings" (got linker errors — he named the stage instantly: "linker!"); the pointer vs
  pointee backwards ("the literal int is freed up, the pointer still points"); a `T` with no
  destructor declared to "still leak regardless"; "b is just renaming a" → double free. The last
  is the 09-23 copy-construction lesson not yet automatic.
- **I made him guess `target_link_options`.** He guessed `target_linking_options`. Naming a CMake
  command is not a learning objective; just give it.
- **He stopped himself at 18:08: "i just get tired of reading for two hours."** Right call. Two
  hours of reading my text is the fatigue, not C++ — shorter replies, fewer bullets, more "run it."
- **Pace:** ~half the week-4 checklist in 38 minutes of work. Remaining: move semantics,
  `shared_ptr`, use-after-free, valgrind.

**After sign-off (not logged as hours):** he talked through where this goes — companies writing
"a lot of AI code", preferring to write code himself, own venture vs getting hired. Told him it's
not a week-4 decision and that the syllabus projects serve both. What he enjoys: optimization —
path planning, a genetic algorithm for class scheduling. Named planning/optimization as a lane;
suggested ArduPilot for the week-40 open-source PR. Ended with "keep looking out for my future."

## 2026-09-26 — syllabus critique from Seth (not work time)

Opened 00:26 UTC by the container clock. Chris's local start time wasn't given; no hours logged.
Chris paused before any C++ so his brother **Seth** (MS Mechanical Engineering, robotics emphasis)
could critique the syllabus.

- **Seth's point:** the syllabus has little on physical components — motors (stepper, servo,
  linear actuators), sensors beyond vision (radar, thermocouples, IMU, acoustic), processors
  (Arduino, Pi), wiring, protocols, a test robot. *"You cannot fully understand robotics without
  knowing what they're made of, how they move, and how they sense."*
- **Checking the syllabus against his point turned up a bigger gap:** no feedback control anywhere,
  no PID, and no protocols. His critique was right. I pushed back only on "fully/all": the target
  is a software engineer, so the fix is broad coverage by principle plus depth on a few parts, not
  a mechatronics degree.
- **Chris: "write the proposal, I think I'm committed for the whole syllabus, so whatever y'all
  think is good."** Applied as revision §13: Part 3 → 5 weeks with two components weeks first,
  Parts 4–10 shift +2, Part 11 → 2 weeks, applications → wk 24. Bench kit to order by wk 6.
- Noted from observations.md: he already has hands-on ArduPilot waypoint work. Worth asking in
  week 8 how much wiring he did there. It may make parts of Components I a refresher.
- **Next session is unchanged:** move semantics.
