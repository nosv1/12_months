# Robotics + AI Engineer

## 52-Week Curriculum — revised September 2026

> Revised from the original 12-month draft against a specific starting point: MS in CS (2024,
> data-science emphasis), two years out of practice, prior Gazebo exposure from a graduate
> robotics course. See [docs/syllabus-revisions.md](docs/syllabus-revisions.md) for what changed
> and why.

## At a glance

| | |
| --- | --- |
| **Weekly commitment** | 10–12 hours |
| **Availability** | Evenings after work + Saturday |
| **Primary languages** | Python + C++ |
| **Core platform** | ROS 2 |
| **Simulation** | Gazebo (primary), Isaac Lab (robot learning only) |
| **ML** | PyTorch, LeRobot |
| **OS** | Linux (WSL2 → native dual-boot by Part 3) |
| **Version control** | Git/GitHub |

**Realistic outcome:** ~550 hours gets you to a credible junior-to-mid robotics software
engineer with a portfolio that survives scrutiny. Not a research scientist. Aiming at the right
target is what keeps week 30 from feeling like failure.

---

## The weekly rhythm

| Day | Mode | Time | What happens |
| --- | --- | --- | --- |
| **Monday** | Learn | ~1.5 h | New concepts, documentation, videos, examples. |
| **Tuesday** | Build | ~1.5 h | Implement what Monday taught. |
| **Wednesday** | Off | — | No guilt. |
| **Thursday** | Build | ~1.5 h | Continue the week's project. |
| **Friday** | Off | — | — |
| **Saturday** | Deep work | 4–5 h | The main project session. |
| **Sunday** | Review | 1.5–2 h | Fix things, document progress, test, plan next week. |

Roughly **10–12 hours/week**. On a bad week, **6 hours is acceptable**.

> **Do not turn one missed week into a missed month.**

---

## The four rules

**Rule 1 — Projects drive learning.** You will never know everything before starting. The project
creates the questions.

**Rule 2 — Tutorials are scaffolding.** Use them to get moving, then deliberately move away.

**Rule 3 — Every part produces evidence.** A repository, demo, video, report, benchmark, or
working system.

**Rule 4 — Confusion is expected.** "I'm stuck" means *investigate.* It does not mean *"I'm not
good enough."*

**Rule 5 — Use AI, don't outsource to it.** You may ask anything, read anything, and have any
concept explained at any depth. You may not accept code you couldn't have written. The test:
can you delete it and rewrite it from memory tomorrow? See
[docs/background-threads.md](docs/background-threads.md).

---

## Year map

| Part | Weeks | Focus | Deliverable |
| --- | --- | --- | --- |
| 1 | 1–2 | Reactivation | Telemetry toolkit |
| 2 | 3–7 | **C++ + Linux systems** | Sensor simulator + network service |
| 3 | 8–10 | Robotics fundamentals | Simulated mobile robot |
| 4 | 11–15 | **ROS 2** | ROS robot system |
| 5 | 16–19 | Navigation | Autonomous navigation in sim |
| 6 | 20–22 | **Physical robot** | Working hardware robot |
| 7 | 23–26 | Perception | Perception pipeline |
| 8 | 27–29 | Deep learning | Vision model |
| 9 | 30–33 | AI + robotics | Vision-guided robot |
| 10 | 34–38 | **Manipulation + behavior** | Pick-and-place task system |
| 11 | 39–42 | **Modern robot learning** | Learned policy (diffusion / BC) |
| 12 | 43–45 | Systems engineering | Production-grade stack |
| 13 | 46–52 | Capstone + career | Capstone + job campaign |

Bold parts are where this revision differs most from the original draft.

**Continuous background threads** run alongside everything from the week noted — build log
(week 1), interview problems (week 20), applications (week 22). Details in
[docs/background-threads.md](docs/background-threads.md).

---

## Part 1 — Reactivation · Weeks 1–2

**Compressed from 4 weeks to 2.** You have a data-science MS. You know Python, NumPy, and
Jupyter. What a DS track usually skips is *software engineering* — packaging, testing, logging,
interfaces, and code that another person can run. That's the actual gap, so that's the target.

Do **not** re-learn Python syntax. If you find yourself reading "what is a list comprehension,"
you've misread this part.

### Week 1 — Engineering practice, not Python

- [ ] WSL2 environment configured, dotfiles, shell you like
- [ ] Virtual environments (`venv` / `uv`) and dependency pinning
- [ ] Project layout: package vs script, `pyproject.toml`, imports that work
- [ ] Type hints + `mypy`
- [ ] `dataclasses`
- [ ] `logging` (not `print`)
- [ ] `argparse` and CLI design
- [ ] `pathlib`
- [ ] Exceptions and error boundaries
- [ ] Git: branches, meaningful commits, `.gitignore`

### Week 2 — Testing, structure, and a real deliverable

- [ ] `pytest`: fixtures, parametrize, what's worth testing
- [ ] Debugging with `pdb` / debugger — not print statements
- [ ] Separating I/O from logic (why it makes things testable)
- [ ] README writing
- [ ] A CI run on GitHub Actions

### Deliverable — Telemetry Toolkit

A command-line robot telemetry analyzer, as a real repository.

*Input:* `timestamp`, `robot_id`, `velocity`, `battery`, `temperature`
*Output:* average velocity, max temperature, min battery, warnings

`raw data → parser → validation → analysis → report`

Must have: clean module boundaries, tests, a CLI, a README someone else could follow, an example
dataset, and CI that runs the tests on push.

### 🥊 Boss Fight #1

Rebuild the telemetry analyzer from an empty directory. No tutorial, no copying your previous
implementation. You may look things up. You must design it yourself.

---

## Part 2 — C++ + Linux Systems · Weeks 3–7

**Expanded from 4 weeks to 5, and this is the most important change in the document.** A
data-science degree generally does not teach manual memory management, RAII, threading, or
sockets. This isn't rust — it may be genuinely new, and every part after this one assumes it.
Do not rush it. If you need a sixth week, take it from Part 3.

### Week 3 — C++ that compiles

- [ ] Compilation model: preprocessor → compile → link (and what each error looks like)
- [ ] Headers, translation units, ODR
- [ ] CMake — enough to build a multi-file project
- [ ] Classes, constructors, destructors
- [ ] References vs pointers vs values
- [ ] `const` correctness

### Week 4 — Memory and ownership

- [ ] Stack vs heap
- [ ] RAII — the central idea in modern C++
- [ ] `unique_ptr`, `shared_ptr`, when each is correct
- [ ] Move semantics and why copies are expensive
- [ ] Dangling references, use-after-free, and how they present
- [ ] Debug with `gdb`, `valgrind`, and sanitizers (`-fsanitize=address`)

### Week 5 — STL and idiom

- [ ] `vector`, `unordered_map`, `string_view`, `optional`
- [ ] Iterators and the algorithm header
- [ ] Templates — enough to read them, not to write clever ones
- [ ] Error handling: exceptions vs error codes
- [ ] Build a small library and link it from another project

`Sensor → SensorBuffer → Processor → Statistics`

### Week 6 — Linux internals

- [ ] Processes, fork/exec, PIDs
- [ ] Threads, `std::thread`, mutexes, race conditions you can actually observe
- [ ] Filesystems, permissions, file descriptors
- [ ] Signals, pipes, environment variables
- [ ] `htop`, `strace`, `lsof`, `journalctl`, `systemd` basics
- [ ] Processes vs threads, and when concurrency is the wrong answer

### Week 7 — Networking + Docker

- [ ] TCP vs UDP, and why robotics cares about the difference
- [ ] Sockets — write a client and a server by hand
- [ ] Serialization: why you can't just send a struct
- [ ] Latency, buffering, backpressure
- [ ] Docker images, containers, volumes, networking
- [ ] Docker Compose

### Deliverable — Robot Sensor Simulator

A C++ program simulating multiple sensors at different rates, exposed over a network interface.

```md
GPS ───────┐
IMU ───────┼──> Sensor Bus ──> Logger
LIDAR ─────┤
Camera ────┘
```

Requirements: sensors run on independent threads at independent rates, the bus is thread-safe,
data is serialized over a socket, and it runs in a container.

### 🥊 Boss Fight #2

Add a new sensor type **without modifying the core processing system.** If you have to touch the
bus, your abstraction was wrong — that's the lesson, not a failure.

---

## Part 3 — Robotics Fundamentals · Weeks 8–10

**Compressed from 4 weeks to 3** — you've used Gazebo before, so the simulation ramp is faster.
The math is not optional, though. Coordinate frames are the single most common source of
robotics bugs, and "I'll figure out transforms later" is a decision you pay for in Part 9.

### Week 8 — Robotics mathematics

- [ ] Coordinate systems and frame conventions
- [ ] Vectors, matrices, matrix multiplication as transformation
- [ ] Rotation matrices
- [ ] Euler angles, and why they betray you (gimbal lock)
- [ ] Quaternions — enough to use them correctly
- [ ] Homogeneous transforms and composing them

You don't need mathematical perfection. You need intuition and correct signs.

### Week 9 — Kinematics + sensors

- [ ] Frames, links, joints
- [ ] Forward kinematics
- [ ] Inverse kinematics (concept + one worked 2-link example by hand)
- [ ] Joint space vs Cartesian space
- [ ] IMU, encoders, LiDAR, depth camera — what each measures and how each lies
- [ ] Noise, drift, bias, sampling rate, and sensor fusion motivation

### Week 10 — Simulation

- [ ] Gazebo refresher (you've seen this — go faster)
- [ ] URDF: robot description from scratch
- [ ] Physics, collision meshes vs visual meshes
- [ ] Simulated sensor plugins
- [ ] The simulation loop, real-time factor, determinism

### Deliverable — Your First Robot

A simulated differential-drive robot with wheels, LiDAR, a camera, and odometry. You should be
able to teleop it.

### 🥊 Boss Fight #3

Write a controller that makes the robot **drive forward → detect obstacle → stop.**

That's it. No autonomous navigation. Small, complete wins build the confidence that carries the
hard months.

---

## Part 4 — ROS 2 · Weeks 11–15

**Expanded from 4 weeks to 5.** ROS 2 is the backbone of everything after this and the single
most valuable line on a robotics résumé. Depth here pays compound interest.

> **Distro decision required before Week 11.** See [docs/environment.md](docs/environment.md) —
> your machine currently has only Ubuntu 26.04, which constrains the choice.

### Week 11 — Foundations

- [ ] Installation, sourcing, workspace layout
- [ ] Packages, `colcon`, build/install/devel
- [ ] Nodes and the node lifecycle
- [ ] `ros2` CLI — become fast with it, it's your debugger

### Week 12 — Topics

- [ ] Publishers, subscribers, message types
- [ ] Custom messages
- [ ] QoS profiles — and what actually happens when they mismatch
- [ ] Executors, callback groups, spinning
- [ ] `ros2 topic echo/hz/bw`, `rqt_graph`

### Week 13 — Services, actions, parameters

- [ ] Services (request/response)
- [ ] Actions (long-running, cancellable, with feedback)
- [ ] Choosing between topic / service / action — this is a design skill
- [ ] Parameters and reconfiguration
- [ ] Launch files (Python launch), composing systems

### Week 14 — Transforms and description

- [ ] TF2 — the tree, broadcasting, listening
- [ ] Static vs dynamic transforms
- [ ] Debugging frame errors (`tf2_echo`, `view_frames`)
- [ ] URDF + Xacro
- [ ] RViz2 — configure it well, you'll live here

### Week 15 — Tooling and rigor

- [ ] `rosbag2`: record, replay, and why it changes how you debug
- [ ] Testing ROS nodes (`launch_testing`)
- [ ] Logging and diagnostics
- [ ] Lifecycle nodes
- [ ] ROS 2 debugging methodology

### Deliverable — ROS Robot

Turn your simulated robot into a real ROS 2 system.

```md
                ┌─────────────┐
                │   Camera    │
                └──────┬──────┘
                       ▼
                  Perception
                       │
LiDAR ────────────────►│
                       ▼
                 Robot State
                       ▼
                    Motion
```

### 🥊 Boss Fight #4

Empty workspace. Build `sensor_node → processing_node → control_node` using the correct ROS
interface for each link — and be able to defend why each is a topic, service, or action.

---

## Part 5 — Navigation · Weeks 16–19

### Week 16 — State estimation

- [ ] Odometry and wheel encoders
- [ ] Dead reckoning and why drift is inevitable
- [ ] The localization problem
- [ ] Kalman filter — intuition, then the equations
- [ ] `robot_localization` / EKF fusion

### Week 17 — Mapping

- [ ] Occupancy grids
- [ ] SLAM concepts: front end, back end, loop closure
- [ ] `slam_toolbox`
- [ ] Map serving and AMCL localization

### Week 18 — Planning

- [ ] Configuration space
- [ ] Dijkstra, A*, and the heuristic that makes A* work
- [ ] Global vs local planning
- [ ] Costmaps, inflation layers
- [ ] Collision checking
- [ ] DWB / MPPI local control

### Week 19 — Nav2

- [ ] Nav2 architecture and behavior trees
- [ ] Goal poses and the action interface
- [ ] Recovery behaviors
- [ ] Tuning — expect this to be most of the week
- [ ] Visualization and failure diagnosis

### Deliverable — Autonomous Navigation

`START → MAP → TARGET → PLAN → NAVIGATE → ARRIVE`

### 🥊 Boss Fight #5

Randomly place obstacles. The robot must still reach the target. Record success rate, average
time, path length, and a written analysis of each failure mode.

You've now built your first genuinely autonomous system.

---

## Part 6 — Physical Robot · Weeks 20–22

**New.** The original syllabus was 52 weeks of pure simulation. Every applicant has Gazebo
videos; almost none have dealt with a robot that physically falls over. This is the single
highest-leverage addition to your portfolio, and it's the part interviewers will ask about.

**Budget: ~$250–400.** Raspberry Pi 5, differential-drive base with encoders, RPLIDAR A1, a
camera, a battery, and a motor driver. Order it during Part 5 — shipping will otherwise become
the bottleneck.

### Week 20 — Bring-up

- [ ] Ubuntu + ROS 2 on the Pi
- [ ] Cross-machine ROS 2 (DDS discovery over the network — expect pain, budget for it)
- [ ] Motor driver and `cmd_vel`
- [ ] Encoder reading and odometry publishing
- [ ] Teleop a real robot

### Week 21 — Real sensors

- [ ] LiDAR driver, real scan data
- [ ] Camera driver, real images
- [ ] Calibration: camera intrinsics, LiDAR mounting transform
- [ ] Time synchronization and message filters
- [ ] Compare real sensor noise against your sim assumptions — write down every difference

### Week 22 — Port the stack

- [ ] Run SLAM on real data
- [ ] Nav2 on hardware
- [ ] Tune for a robot with real mass and real latency
- [ ] Safety: e-stop, velocity limits, watchdog

### Deliverable — Working Physical Robot

Autonomous navigation on real hardware, in your actual apartment. Record video. This is portfolio
project #1.

### 🥊 Boss Fight #6

Your sim-tuned navigation parameters will not work on hardware. Diagnose *why* — measure it,
don't guess — and write up the sim-to-real gap you found. That write-up is worth more than the
demo.

---

## Part 7 — Perception · Weeks 23–26

### Week 23 — Camera geometry

- [ ] Pinhole model, intrinsics, distortion
- [ ] Extrinsics and camera↔robot transforms
- [ ] RGB, depth, stereo, point clouds
- [ ] Projection and back-projection — by hand, at least once

### Week 24 — Classical CV

- [ ] OpenCV fundamentals
- [ ] Color spaces, thresholding, morphology
- [ ] Edges, contours, features
- [ ] When classical CV beats a neural network (more often than you'd think)

### Week 25 — Detection

- [ ] Detection vs classification vs segmentation
- [ ] Bounding boxes, IoU, NMS
- [ ] Confidence and calibration
- [ ] Running a pretrained detector (YOLO or similar)
- [ ] Dataset concepts, labeling, class imbalance

### Week 26 — Perception in ROS

- [ ] `image_transport`, camera topics, compression
- [ ] `vision_msgs`
- [ ] Point cloud processing (PCL / Open3D basics)
- [ ] Latency budgets and dropped frames
- [ ] Visualizing and debugging a perception pipeline

### Deliverable — Robot Vision Pipeline

`Camera → Vision Model → Object → Position → ROS message`

Running on your real robot, not just in sim.

### 🥊 Boss Fight #7

Given a camera frame, answer *"where is the object, in the robot's frame?"* — in metres, with
the transform chain correct. Not necessarily perfectly. It needs to work.

---

## Part 8 — Deep Learning · Weeks 27–29

**Compressed from 4 weeks to 3.** Your DS background covers tensors, training loops, loss
functions, overfitting, and metrics. Skim those hard and spend the time on what's actually new:
convolutional architectures, vision-specific training, and deployment.

If any of Week 27's list is genuinely unfamiliar, stop compressing and take the fourth week.
Be honest with yourself here — this is the one place where the DS asterisk could cut either way.

### Week 27 — PyTorch fluency (fast)

- [ ] Tensors, devices, dtypes
- [ ] `Dataset` / `DataLoader`, collate, augmentation
- [ ] Autograd mechanics — what `backward()` actually does
- [ ] Training loop, validation split, checkpointing
- [ ] Reproducibility: seeds, determinism

### Week 28 — Vision

- [ ] CNNs: convolution, stride, padding, receptive field
- [ ] Modern backbones (ResNet, and why residuals)
- [ ] Transfer learning and fine-tuning
- [ ] Augmentation strategy
- [ ] Detection fine-tuning on a custom dataset
- [ ] Error analysis — look at the failures, individually

### Week 29 — Deployment

- [ ] Export: TorchScript, ONNX
- [ ] TensorRT and why robotics cares
- [ ] Batch vs real-time inference
- [ ] Quantization and the accuracy/latency tradeoff
- [ ] Profiling GPU inference
- [ ] CUDA on your hardware — see [docs/environment.md](docs/environment.md), the 5080 has a
      specific gotcha

### Deliverable — Train Your Own Vision Model

Collect and label your own dataset **from your robot's camera**, then train a detector on it.

`Dataset → Training → Validation → Testing → Error analysis`

Using your own data is the point. Public datasets are clean in ways the world isn't.

### 🥊 Boss Fight #8

Someone hands you an unfamiliar dataset. Load it → inspect it → train → evaluate → report. No
walkthrough.

---

## Part 9 — AI + Robotics · Weeks 30–33

Where the previous eight parts connect.

### Week 30 — Inference in the loop

- [ ] Model inference inside a ROS 2 node
- [ ] Threading: don't block the executor
- [ ] Real-time constraints and dropping frames gracefully
- [ ] Detection message design

### Week 31 — 3D localization

- [ ] From bounding box to 3D position (depth, stereo, or geometry)
- [ ] Camera → robot → map frame chains
- [ ] Uncertainty propagation
- [ ] Publishing detections into TF

### Week 32 — Tracking

- [ ] Multi-object detection
- [ ] Data association
- [ ] Track lifecycle: birth, update, death
- [ ] Temporal consistency and filtering

### Week 33 — Perception-driven behavior

- [ ] Closing the loop: perception → decision → motion
- [ ] Handling detection failure without crashing
- [ ] Confidence thresholds as a control decision

### Deliverable — Vision-Guided Robot

`SEE → IDENTIFY → LOCATE → DECIDE → MOVE`

On hardware. This is portfolio project #2.

### 🥊 Boss Fight #9

Several objects in the environment, one named target. The robot identifies the correct one and
navigates to it.

---

## Part 10 — Manipulation + Behavior · Weeks 34–38

**Expanded to 5 weeks and given an arm.** The original syllabus taught inverse kinematics in
week 10, then asked you to "pick object / place object" in month 9 with a robot that had no
manipulator. This fixes that inconsistency — and manipulation is where a large share of robotics
hiring actually is.

The arm is simulated (Franka Panda or UR5 in Gazebo). Do not buy one.

### Week 34 — Arm kinematics

- [ ] Serial manipulators, DH parameters
- [ ] Forward kinematics for a 6/7-DOF arm
- [ ] Analytical vs numerical IK
- [ ] Jacobians, singularities, redundancy
- [ ] Workspace limits

### Week 35 — MoveIt 2

- [ ] MoveIt 2 architecture and setup assistant
- [ ] Planning scene and collision objects
- [ ] Motion planning (OMPL), planning groups
- [ ] Cartesian paths
- [ ] Grasp pose generation and execution

### Week 36 — State machines and behavior trees

- [ ] Finite state machines: states, events, guards, recovery
- [ ] Behavior trees: why robotics prefers them
- [ ] BehaviorTree.CPP and Nav2's BT integration
- [ ] Reactive vs deliberative behavior

### Week 37 — Task composition

- [ ] Task planning and preconditions
- [ ] Trajectory constraints
- [ ] Collision checking during execution
- [ ] Blackboards and shared state

### Week 38 — Robustness

- [ ] System architecture for failure
- [ ] Failure detection and classification
- [ ] Recovery strategies and retry policy
- [ ] Safety boundaries and interlocks

### Deliverable — Robot Task Manager

`Find object → Approach → Verify → Grasp → Transport → Place`

### 🥊 Boss Fight #10

Break it deliberately: the target disappears mid-approach, navigation fails, detection returns a
false positive, a sensor dies. The system must degrade and recover rather than crash.

This is where you start thinking like an engineer instead of a programmer completing happy-path
demos.

---

## Part 11 — Modern Robot Learning · Weeks 39–42

**Substantially rewritten.** The original gave you MDPs, Q-learning, and PPO — a solid but
roughly 2019 curriculum. That's not what's moving robotics right now, and "left behind by recent
developments" is the reason you started this. The current centre of gravity is **learning from
demonstration at scale**: behavior cloning, diffusion policies, and vision-language-action
models.

Keep the RL foundations — they're the vocabulary. But land the plane on what shipped recently.

### Week 39 — RL foundations (fast)

- [ ] MDPs: state, action, reward, transition, discount
- [ ] Policy, value function, Q-function
- [ ] Exploration vs exploitation
- [ ] Policy gradients → PPO, conceptually
- [ ] Why pure RL is hard on real robots (sample complexity, reward design, safety)

### Week 40 — Imitation learning

- [ ] Behavioral cloning and the compounding-error problem
- [ ] DAgger and interactive correction
- [ ] Demonstration collection — teleoperate your own robot to gather data
- [ ] LeRobot: datasets, training, evaluation
- [ ] Action chunking (ACT)

### Week 41 — Diffusion policies

- [ ] Diffusion models — enough theory to understand the policy
- [ ] Why diffusion suits multimodal action distributions
- [ ] Training a diffusion policy in LeRobot
- [ ] Evaluation: success rate, and why it's noisy

### Week 42 — VLAs and simulation scale

- [ ] Vision-language-action models: the RT-2 → OpenVLA → π0 lineage
- [ ] Read one VLA paper properly, end to end
- [ ] Run inference with an open VLA checkpoint
- [ ] Isaac Lab: vectorized envs, domain randomization
- [ ] Sim-to-real transfer — connect this to what you measured in Boss Fight #6

### Deliverable — Learned Robot Behavior

Train a policy from your own demonstrations to solve a manipulation task. Start embarrassingly
simple.

`observe state → policy → action → environment → reward`

Report: demonstrations collected, success rate, failure modes, and a comparison against a
scripted baseline. **If the scripted baseline wins, say so.** That's a real and publishable
result, and pretending otherwise is how portfolios lose credibility.

### 🥊 Boss Fight #11

Change the environment — move the target, alter lighting, swap the object. Measure how far
performance degrades. Then introduce domain randomization and measure again.

---

## Part 12 — Systems Engineering · Weeks 43–45

**Compressed to 3 weeks.** Deliberately less glamorous, and one of the things that separates a
portfolio project from a toy.

### Week 43 — Observability

- [ ] Structured logging
- [ ] Metrics and time-series (Prometheus/Grafana or ROS diagnostics)
- [ ] Performance profiling: CPU, GPU, memory
- [ ] Latency measurement across a distributed pipeline

### Week 44 — Concurrency and deployment

- [ ] Multithreading, async, queues, synchronization
- [ ] Real-time considerations in ROS 2
- [ ] Docker for robotics (GPU passthrough, device access)
- [ ] Configuration management and reproducible environments
- [ ] Launch orchestration for a full system

### Week 45 — Rigor

- [ ] Automated tests: unit, integration, simulation-in-the-loop
- [ ] CI/CD for a ROS 2 workspace
- [ ] System documentation and architecture diagrams
- [ ] Failure injection / chaos testing

### Deliverable — Production Robotics Stack

Take a previous project and make it look like software a team could maintain.

`Camera → Perception → Planner → Control → Robot → Telemetry → Dashboard`

### 🥊 Boss Fight #12

Kill one component at random. The system must detect the failure, log it, avoid catastrophic
behavior, and recover or shut down safely.

---

## Part 13 — Capstone + Career · Weeks 46–52

You're no longer primarily learning. You're packaging the capability you've built.

> If you followed the background threads, you've been applying since week 22 and have real
> interview feedback by now. Use it to aim this part.

### Week 46 — Choose and scope

**Autonomous AI Robot** — ROS 2 + perception + navigation + manipulation + learned policy +
telemetry, running on real hardware.

Scope it to what's achievable in four weeks. An impressive narrow demo beats an ambitious broken
one.

### Weeks 47–48 — Build

Integrate. Expect integration to take longer than any component did.

### Week 49 — Benchmark

- [ ] Success rate over ≥20 trials
- [ ] End-to-end latency
- [ ] CPU/GPU utilization
- [ ] Inference time
- [ ] Navigation time
- [ ] Failure mode taxonomy

Numbers, honestly reported. Including the bad ones.

### Week 50 — Documentation + reimplementation

- [ ] README, architecture diagram, setup instructions
- [ ] Design decisions and tradeoffs, written down
- [ ] Benchmark results
- [ ] Demo video — 90 seconds, no narration required, must show a failure and a recovery
- [ ] **Reimplement one VLA paper's inference path** from the paper alone

That last item is the "not left behind" checkpoint. Being able to read a 2026 robot-learning
paper and make it run is the durable skill.

### Week 51 — Career packaging

- [ ] Résumé rewritten around systems built, not courses taken
- [ ] GitHub profile and three pinned projects
- [ ] LinkedIn
- [ ] Be able to explain each project at three depths:
  - **30 seconds** — "I built an autonomous robot that…"
  - **5 minutes** — architecture and major components
  - **30 minutes** — design decisions, failures, tradeoffs, implementation detail

### Week 52 — 👑 Final Boss

Empty repository. The brief:

> Build an autonomous robot that can perceive an environment, make decisions, navigate to a
> target, and report its performance.

You have documentation, Stack Overflow, GitHub, AI assistants, papers, and tutorials. You have no
step-by-step instructions. You have one week.

This isn't about building the world's best robot. It answers one question:

> **Can you take an ambiguous engineering problem and figure out how to build it?**

That's the skill this year trains.

---

## Your three portfolio projects

**1. Autonomous Mobile Robot (physical)** — ROS 2 + SLAM + Nav2 on real hardware
*Demonstrates:* robotics fundamentals, systems integration, sim-to-real

**2. Vision-Guided Robot** — PyTorch + perception + ROS 2
*Demonstrates:* AI + perception + robotics

**3. Autonomous AI Robot** — perception + planning + manipulation + learned policy + monitoring
*Demonstrates:* integrated engineering ability

Everything else supports those three. The physical robot is the differentiator — lead with it.

---

## What you should know by the end

Not *"I know all of robotics."* That's impossible. Instead:

**Software** — Python + C++ + Linux + Git + Docker, comfortably.

**Robotics** — ROS 2, sensors, frames, kinematics, localization, navigation, motion planning.

**AI** — PyTorch, computer vision, training, inference, deployment.

**Robot learning** — imitation learning, diffusion policies, RL fundamentals, sim-to-real, and
enough VLA literacy to read what ships next.

**Engineering** — debug → test → profile → document → deploy.

**Problem solving** — you encounter something you've never seen and say: *"Okay. Let me figure
this out."*

That's the real graduation requirement.

---

## The psychological constraint is part of the curriculum

Explicit, because it matters more than any checklist here.

**You are not allowed to judge your ability by whether you understand something immediately.**

Your progression will routinely look like:

```md
"I have no idea what this is."
             ↓
"I kind of understand it."
             ↓
"I can follow an example."
             ↓
"I can modify the example."
             ↓
"I can build it myself."
             ↓
"I can debug someone else's version."
```

That is learning. It looks like confusion from the inside, every time.

A note on the asterisk: you got the degree. Two years of not using something is not a verdict on
whether you can do it — it's just two years of not using it. The boss fights exist precisely so
your confidence tracks demonstrated evidence rather than vibes.

When you reach *"I can figure this out,"* not-knowing stops being threatening. That's what this
year is for.

---

## Getting started

**Week 1 is the entire assignment.** Do not read ahead and turn this into another intimidating
thing you're supposed to already understand.

Finish Week 1. Then Week 2. One checkbox at a time.

Track progress in [docs/00-dashboard.md](docs/00-dashboard.md).
