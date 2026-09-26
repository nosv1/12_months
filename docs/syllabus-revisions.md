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

### 13. Physical components added; robot learning compressed (2026-09-26)

**Critique from Seth**, Chris's brother (MS Mechanical Engineering, robotics emphasis), given in
session in week 4. His argument: *you cannot fully understand robotics without knowing what
robots are made of, how they move, and how they sense the environment, even if you only write
the software.* Cameras and LiDAR don't cover the physical components of most robots. He named
motors (stepper, servo), linear actuators, sensors beyond vision (radar, thermocouples, IMUs,
acoustic), processors (Arduino, Raspberry Pi), wiring, communication protocols, and building a
test robot.

**What checking the syllabus showed.** He was right, and the gap was bigger than he said:

- **No feedback control anywhere.** No PID, no motor control loop. Actuators appeared once,
  as "motor driver and `cmd_vel`" in the physical-robot week.
- **No communication protocols.** I2C, SPI, UART, CAN, PWM and the ADC were never taught. The
  Part 6 kit hides all of them behind USB drivers. He could have finished the year without ever
  reading a datasheet register map.
- **Sensors covered only for use, not for selection.** Week 9 asked how the four standard mobile
  sensors lie, but never how to choose a sensor for a job.
- **Mounting reduced to one calibration number.** Nothing on vibration, rigidity, field of view,
  or cable strain.
- **Power absent entirely.**

**Where the critique was scoped rather than adopted whole.** "Fully understand all physical
components" is most of a mechatronics degree. It doesn't fit in ~550 hours alongside everything
else. The target is a robotics *software* engineer who knows the hardware well enough to choose
it, wire it, read it, and debug it. CAD and structural design stay out of scope. Coverage is
**broad and organized by principle**: every component gets the same four questions (physical
principle, output, interface, how it fails). There is **hands-on depth on a few parts**: one
sensor read from its datasheet, one PID loop on a real motor. The principle-based framing is the
point. It carries over to parts he has never seen, and a catalogue wouldn't.

**What changed.**

- **Part 3 expands 3 → 5 weeks (8–12).** Weeks 8–9 are new: *Components I* (compute, buses,
  sensing, power) and *Components II* (actuators, transmissions, PID, mounting). They come
  first so kinematics can refer to real joints and actuators, and so simulation can be judged
  by what it leaves out. Week 9's old sensor-noise items moved into week 8.
- **The components deliverable reuses Part 2's sensor bus.** A real I2C IMU gets added to it
  without touching the core. That's Boss Fight #2's lesson, tested against hardware.
- **Bench kit, ~$100–150, ordered by week 6.** The Pi and the IMU carry over to Part 6, so the
  Part 6 budget effectively absorbs part of it.
- **Part 6 builds on it.** The PID loop drives the wheels, the IMU is fused into odometry, and
  he mounts the LiDAR and IMU himself instead of using a pre-drilled plate.
- **Parts 4–10 shift two weeks later.** Boss fights #3–#10 move with them.
- **Applications move from week 22 to 24.** They were timed to land when the physical robot
  was finished, and it now finishes at week 24. Interview problems stay at week 20.

**What paid for it: Part 11, 4 → 2 weeks.** RL foundations drop to vocabulary. Imitation
learning and diffusion/VLA get one week each, and Isaac Lab becomes optional. Chosen because:

- it's the most speculative part of the plan;
- he has since said he leans toward planning/optimization, not learning-based control;
- week 50's VLA reimplementation still carries the "not left behind" checkpoint;
- hands-on hardware knowledge is more likely to come up in a robotics interview than a second
  learning framework.

**Reverse it** if interviews from week 24 onward show that RL/learning depth is what the market
asks of him. Take the week back from Part 11 then.

**Estimate, mine:** the components weeks at ~20–25 h. Logged in `ta-notes/estimates.md`.

Seth offered domain review. When weeks 8–9 arrive, have him check the component list for
anything missing or misweighted.

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
- **Bench kit** — order by week 6 for the Part 3 components weeks (see §13).
- **Robot BOM** — order during Part 5 (weeks 18–21) so shipping isn't the bottleneck at week 22.
