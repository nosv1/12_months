# Week 6 — Linux internals: session log

## 2026-10-07 Wed, 10:00–10:27 (work off day; hours not logged, see below)

- **10-02 to 10-06 was an off period.** He stayed away partly to avoid the kit question: not buying
  it raises motivation and long-term-goal questions he doesn't want to think about. His own read:
  "in every moment I do what I want… minimal discipline other than moderation." The kit and the
  build log are both dropped (decisions.md 2026-10-07).
- **Week 5 ticked.** Re-verified first: 11/11 tests pass, and `w05-consumer` builds.
- **Week 6:** "doesn't sound too interesting, though easy enough." Told him threads are the hard part.
- **Side project 1, orbital path planning.** Flight-instructor terms were offered and not yet
  confirmed. His question: can gravity leave a moving object "stopped"? Steered him toward the
  reference frame, flyby energy symmetry (same speed in as out against a fixed body), and the
  difference between a momentary stop at zero radial velocity and staying stopped at a zero-net-force
  point. **Not named yet:** Lagrange points, gravity assist. He wants to discover them "ish".
  Suggested a ~40-line NumPy flyby sim (speed in vs out) as his first instrument. Sign convention:
  range rate is negative when closing, DCS closure is positive when closing, radial velocity is
  positive outbound.
- **Side project 2, bowling tracker (shower thought).** Web app, no Go, nothing paid. Pitched it as
  Part 7 perception in costume: offline Python+OpenCV on recorded video first, browser
  (OpenCV.js/MediaPipe on GitHub Pages) later. Core problems: homography to lane boards (39 boards,
  60 ft), ball tracking by background subtraction, pins left (one camera can't easily do both ends;
  his design call). He hasn't picked which project goes first.
- **"Me" across projects.** He wants my awareness of him outside this repo, **including the phone
  app.** Explained that `~/.claude/CLAUDE.md` covers WSL Claude Code only, and phone/web sessions see
  only the committed repo. **Told not to act yet.**

### Open for next session (his answers needed)

1. **Hours today:** 10:00–10:27. Do they count? If they do, are side-project hours logged separately
   from the 52-week total? Not logged until he answers.
2. **Global profile:** should "help, don't perform" go everywhere, stay repo-only, or be the default
   with "just build it" as the override? Also, find out (don't guess) whether claude.ai/code
   supports user-level instructions across repos. If it doesn't, the fallback is a profile file
   committed per repo, or a small profile repo.
3. **Flight-instructor terms** for the side projects, and which project comes first.

### Answered 10:3x, same day

1. **Today's hours and side-project hours are not logged.** Only curriculum hours count.
2. **"You are always my flight instructor until stated otherwise. You have the answers, I need to
   develop the skill."** Settles the scope: teaching mode is the default everywhere, not just in this
   repo. The global profile has still not been built, and the cloud-instructions question is still
   open.
3. **Terms: pass. Bowling app: not now.** Orbital path planning is the active side project.
   Bowling stays parked; don't raise it.

He may come back later today for week 6.

## 2026-10-10 Sat, phone, driving to Omaha for work (not curriculum; not logged)

- **Side project 3, iRacing race engineer.** Brainstorm only. Notes:
  [docs/ideas/iracing-race-engineer.md](../../ideas/iracing-race-engineer.md). The ACC version was
  trigger-only Python; Python wasn't the problem. Wants: local LLM, real conversation, a spotter,
  audio first. Quest 3. **His key takeaway, flagged to keep: log the questions that need the code
  fallback, and promote the repeated ones to built-in functions.**
- **Where the curriculum stands, his words.** Watched an NVIDIA robotics video, thought "better get
  on that train," had GPT write a syllabus, had me edit it. Then hit not wanting to buy things,
  questioned his motivation, and "not seeing that light at the end of the tunnel." **"Not sure what
  the future is with the robotic stuff anymore."** Robotics "was just something to get me by in a
  time where I had no projects." Interests and coding skill are intact; ideas still feel fun. He
  does not see side projects as taking time from robotics.
- He recalled the video as "two weeks ago." Logged hours start 09-09, about a month. Not raised.
- **No decision was made.** I didn't push. Told him I'd rather talk through doubt directly than
  let a side project quietly replace the plan without deciding it.
- **Later in the same call:** stealth goal-seeker from his grad class came up as a curriculum backbone
  ([docs/ideas/stealth-goal-seeker.md](../../ideas/stealth-goal-seeker.md)). Proposed order: 2D Python
  now → Gazebo → ROS 2 → mapping/planning/Nav2. Weeks 6–7 compressed, hardware weeks a decision. Not
  decided; to work out at a keyboard. Also "buy to test, not to learn" (observations.md).
- **Signed off energized**: "I feel energized again about writing some code," whether robotics or the
  race engineer. Credits himself with redirecting rather than avoiding. No hours logged (phone, not
  curriculum).
