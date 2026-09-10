# Background threads

Continuous activities that run alongside the weekly syllabus. Small, regular, and easy to skip —
which is exactly why they're written down.

---

## 1. Build log — from week 1

One short entry per week. Not a diary; a record of technical decisions.

```markdown
## Week N — <topic>

**Built:** what exists now that didn't before
**Broke:** what went wrong, and the actual root cause
**Learned:** the thing you'd tell past-you
**Stuck on:** open questions carried forward
**Hours:** actual, not aspirational
```

**Why it matters:** in month 12 you need to explain two years of gap and one year of work to a
stranger. Reconstructing that from memory produces vague claims. Reconstructing it from 52
entries produces specifics, and specifics are what get believed.

Second reason: "Broke" is the highest-value field. Debugging stories are what senior interviewers
actually probe, and they're the first thing you forget.

Publish it. A public log creates mild accountability and doubles as portfolio evidence.

---

## 2. Interview problems — from week 20

**Two problems per week. Not more.**

Starting at week 20 rather than week 1 is deliberate: the original syllabus put DSA in month 1
and interview prep in month 12, both wrong. Skills decay, so cramming eleven months early is
wasted — but two weeks of panic at the end is also wasted.

- Weeks 20–30: fundamentals (arrays, hash maps, two pointers, trees, graphs, BFS/DFS)
- Weeks 30–40: alternate — one algorithm problem, one systems/robotics question
- Weeks 40–52: mock interviews, out loud, with a timer

Robotics-specific questions to be able to answer cold:

- Explain a coordinate frame transform chain. Why did your TF tree break?
- Topic vs service vs action — when each, and why
- How does a Kalman filter work? When does it fail?
- A* vs Dijkstra — what does the heuristic buy you?
- How would you debug a robot that drifts left?
- Sensor fusion: why fuse IMU and wheel odometry?
- What's the sim-to-real gap and how did you measure it?

That last one you'll be able to answer from Boss Fight #6, which most candidates cannot.

---

## 3. Applications — from week 22

**Start applying at week 22, not week 46.**

This feels premature. It isn't. You will fail these interviews, and that's the point — failure
transcripts are the highest-quality feedback in the entire curriculum. They tell you what the
market actually asks rather than what a roadmap guessed.

- 2–3 applications per week, low effort, no agonizing
- Take every screen offered
- After each: write down every question you couldn't answer
- **Feed those gaps back into the syllabus.** This is the actual mechanism.

Realistic targets given the background: robotics software engineer, perception engineer, ML
engineer at a robotics company, simulation engineer, autonomy software engineer. Less realistic
in twelve months: robotics research scientist, controls engineer at a company that wants a
mechanical/EE background.

If something lands early, take it. This syllabus is a means, not a commitment.

---

## 4. Open source — one merged PR by week 40

One merged pull request to a real ROS 2 package. Documentation fixes count. Bug fixes count more.

**Why:** it's third-party evidence that someone who isn't you judged your work acceptable. For a
career-changer with a gap, external validation is disproportionately valuable — and reading a
mature ROS 2 codebase teaches things no tutorial does.

Start looking around week 25, once you can read ROS 2 code fluently. Nav2, `slam_toolbox`, and
`robot_localization` all have approachable issue trackers.

---

## 5. AI tooling fluency — continuous

Rule 5: **use AI, don't outsource to it.** The boundary, concretely.

**Legitimate — use freely:**

- Explaining concepts at any depth, repeatedly, until they land
- Reading error messages and pointing at the failing line
- Reviewing code you wrote and being blunt about what's wrong
- Generating scaffolding that isn't the learning objective: dotfiles, Dockerfiles, CI config,
  install scripts, plotting throwaway results
- Rubber-ducking a design before you build it
- Summarizing papers, then checking your understanding against the summary

**Not legitimate:**

- Accepting implementation code for the thing the week is teaching
- Any assistance during a boss fight beyond rubber-ducking
- Pasting an error and applying the fix without understanding the cause
- Letting it design your architecture

**The test:** can you delete it and rewrite it from memory tomorrow? If not, you didn't learn it —
you rented it.

**Why this is itself a skill:** in 2026, being effective with AI tooling is hireable, and being
dependent on it is disqualifying. Interviews are increasingly designed to detect the difference.
The habit you build over 52 weeks is the one you'll have in the room.

---

## Weekly review checklist

Sunday, ~10 minutes:

- [ ] Build log entry written
- [ ] Week's checkboxes updated in [00-dashboard.md](00-dashboard.md)
- [ ] Code committed and pushed
- [ ] Two interview problems done (from week 20)
- [ ] Applications sent (from week 22)
- [ ] Next week's Monday material identified — so Monday starts, rather than begins with deciding
