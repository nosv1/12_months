# Syllabus revisions — September 2026

Why the syllabus differs from the original GPT-generated draft. Recorded so the reasoning
survives contact with month 7, when you'll wonder why C++ got five weeks.

## The starting point that drove the changes

The original draft was written without knowing anything about the person following it. The
actual starting point:

- MS in Computer Science, 2024, **data-science emphasis**
- Two years with little programming since
- Prior Gazebo exposure from a graduate robotics course
- Strong hardware (RTX 5080, Ryzen 9800X3D, 32 GB)
- Goal: not feeling left behind by recent AI/robotics progress → employable capability

The data-science emphasis is the load-bearing detail. It creates an **asymmetric** gap that a
generic roadmap gets backwards.

## The asymmetry

| Area | Generic assumption | Actual likely state | Response |
|---|---|---|---|
| Python, NumPy, notebooks | Needs 4 weeks | Strong, just cold | Cut to ~1 week |
| Software engineering (packaging, testing, CI) | Assumed known | Often skipped in DS tracks | Keep, make it the focus of Part 1 |
| C++, memory, RAII | "Rusty" | Possibly **never learned** | Expand 4 → 5 weeks |
| Linux internals, threads, sockets | "Rusty" | Possibly never learned | Expand, own week each |
| PyTorch, training loops, metrics | Needs 4 weeks | Largely known | Cut 4 → 3 weeks |
| CNNs, vision, deployment | Needs a week | Genuinely new | Keep full weight |
| Gazebo / simulation | Needs 4 weeks | Prior exposure | Cut 4 → 3 weeks |

An initial read treated Parts 1 and 2 as equally remedial and recommended compressing both.
That was wrong once the DS emphasis was known: they need **opposite** treatment. Part 1 shrinks,
Part 2 grows.

## The changes

### 1. Reactivation compressed, and retargeted (4 weeks → 2)

Not "relearn Python." The target is the engineering practice a data-science track typically
skips: package layout, testing, logging, CLI design, CI. The telemetry project survives because
it's a good vehicle for exactly that.

Dropped: the dedicated data-structures/algorithms week. Moved to a background thread from
week 20 (see [background-threads.md](background-threads.md)) — cramming DSA eleven months before
an interview is wasted effort.

### 2. C++ and Linux expanded (4 weeks → 5)

The most important change. Everything from Part 4 onward assumes comfort with memory, threading,
and networking. ROS 2's C++ API is unforgiving if RAII and ownership aren't intuitive. Given a
week each: compilation, memory, STL, Linux internals, networking + Docker.

Added explicitly because they're where the real debugging time goes: `gdb`, `valgrind`, address
sanitizer, `strace`.

**If week 7 arrives and C++ still feels shaky, take a sixth week from Part 3.** Underbuilding
here is far more expensive than a one-week delay.

### 3. Robotics fundamentals compressed (4 weeks → 3)

Prior Gazebo experience. The simulation week goes faster. The *math* week does not — coordinate
frames and transforms are the most common source of robotics bugs, and quaternions were added
explicitly since the original omitted them.

### 4. ROS 2 expanded (4 weeks → 5)

The backbone of everything after, and the most valuable line on a robotics résumé. The original
compressed services, actions, parameters, launch, and logging into one week; those are now split
properly. Added: executors and callback groups, custom messages, lifecycle nodes, and
`launch_testing`.

Added a design skill the original skipped entirely: **choosing** between topic, service, and
action. That judgement is what interviewers probe.

### 5. Physical robot added (new, 3 weeks)

The original was 52 weeks of pure simulation. That's the portfolio's biggest weakness — sim demos
don't demonstrate that you can handle sensor noise, calibration, clock skew, or a robot with real
mass. A ~$250–400 build (Pi 5 + differential drive + RPLIDAR A1 + camera) changes what you can
claim.

Boss Fight #6 is deliberately about the **sim-to-real gap**, not about getting a demo working.
Measuring and writing up why sim-tuned parameters fail on hardware is a more valuable artifact
than the video, and it feeds directly into Part 11's domain randomization.

### 6. Deep learning compressed (4 weeks → 3)

DS background covers tensors, training loops, loss functions, overfitting, metrics. Skim those;
spend the time on CNNs, vision-specific training, and deployment (ONNX/TensorRT/quantization),
which a DS curriculum usually doesn't touch.

Changed the project to require **collecting and labeling data from your own robot's camera**.
Public datasets are clean in ways the world isn't, and "I built the dataset" is a stronger
interview story than "I fine-tuned on COCO."

**Escape hatch:** if Week 27's checklist is genuinely unfamiliar, take the fourth week back.
This is the one compression that could cut either way.

### 7. Manipulation added; the arm inconsistency fixed (4 weeks → 5)

The original taught inverse kinematics in week 10, spent eight months on a mobile base, then
asked for "pick object / place object" in month 9 with a robot that had no arm. Resolved by
adding a simulated arm (Franka/UR5) and MoveIt 2 — the direction chosen because a large share of
robotics hiring is manipulation.

The arm stays simulated. Real arms are expensive and the mobile robot already provides the
hardware lesson.

### 8. Robot learning modernized (rewritten)

The original taught MDPs → Q-learning → PPO. Solid, and roughly the 2019 curriculum. Since the
stated motivation was *"felt left behind by recent AI and robotics developments,"* finishing the
year without touching what actually shipped recently would be a real miss.

RL foundations compressed to one week (they're the vocabulary). The remaining three go to
learning from demonstration: behavior cloning, DAgger, **LeRobot**, action chunking, **diffusion
policies**, and **VLAs** (RT-2 → OpenVLA → π0).

The original's instinct — don't spend three months on LLMs, they aren't the foundation of
robotics engineering — was correct and is preserved. This is roughly three weeks of modern
material on top of solid foundations, not a pivot.

The deliverable requires reporting a comparison against a **scripted baseline**, including when
the baseline wins. Learned policies frequently lose to scripted ones on simple tasks. Reporting
that honestly is what separates an engineer from a demo.

### 9. Systems engineering compressed (4 weeks → 3)

Still present and still important — it's what separates a portfolio project from a toy — but
three weeks is enough given the practices are threaded through earlier parts.

### 10. Career work moved earlier and made continuous

The original stacked interview prep into week 50: two weeks of cramming after eleven months of
not thinking about it. Now a background thread from week 20, with **applications starting at
week 22**.

Applying at month 6 is deliberate. You will fail those interviews. The failures are the
highest-quality curriculum feedback available — they tell you what the market actually asks,
which no roadmap can predict. Free, fast, and honest.

### 11. Rule 5 added

The original never mentioned AI tooling — odd for a curriculum motivated by AI anxiety. Being
effective with AI tools is itself a hireable 2026 skill, and the dependency failure mode is real.
Rule 5 and the [background threads](background-threads.md) make the boundary explicit.

### 12. Structure changed from months to parts

Weeks no longer divide into 4-week months, so month framing would misrepresent the schedule.
Parts have explicit week ranges. Thirteen parts, twelve boss fights, one final.

## What was deliberately kept

The original draft was better than most. Unchanged:

- **The weekly rhythm.** Wednesday and Friday off is good design — sustainable beats optimal, and
  the two-day gap prevents the all-or-nothing collapse that kills self-directed curricula.
- **Boss fights.** Blank-page rebuilds are the strongest pedagogical device in the document.
  Retrieval practice is how you find out what you actually know versus what you can follow along
  with.
- **"Do not turn one missed week into a missed month."**
- **The psychological framing.** The progression ladder from "no idea" to "can debug someone
  else's version" is accurate and worth rereading in month 8.
- **Refusing to spend three months on LLMs.** Correct call.
- **Rule 3, evidence every part.** Non-negotiable for someone with a two-year gap to explain.

## Open decisions

- **ROS 2 distro** — both WSL distros are Ubuntu 26.04; the mature LTS targets 24.04. Must be
  settled before week 11. See [environment.md](environment.md).
- **Native dual-boot** — planned before Part 3, needed by Part 6.
- **Robot BOM** — order during Part 5 (weeks 16–19) so shipping isn't the bottleneck at week 20.
