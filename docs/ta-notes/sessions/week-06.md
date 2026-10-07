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
