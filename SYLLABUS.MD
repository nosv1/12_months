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
| **Simulation** | Gazebo (primary), Isaac Lab (optional, robot learning only) |
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
| 3 | 8–12 | **Components + robotics fundamentals** | Bench rig + simulated mobile robot |
| 4 | 13–17 | **ROS 2** | ROS robot system |
| 5 | 18–21 | Navigation | Autonomous navigation in sim |
| 6 | 22–24 | **Physical robot** | Working hardware robot |
| 7 | 25–28 | Perception | Perception pipeline |
| 8 | 29–31 | Deep learning | Vision model |
| 9 | 32–35 | AI + robotics | Vision-guided robot |
| 10 | 36–40 | **Manipulation + behavior** | Pick-and-place task system |
| 11 | 41–42 | **Modern robot learning** | Learned policy (diffusion / BC) |
| 12 | 43–45 | Systems engineering | Production-grade stack |
| 13 | 46–52 | Capstone + career | Capstone + job campaign |

Bold parts are where this revision differs most from the original draft.

**Continuous background threads** run alongside everything from the week noted — build log
(week 1), interview problems (week 20), applications (week 24). Details in
[docs/background-threads.md](docs/background-threads.md).

---

## Part 1 — Reactivation · Weeks 1–2

**Compressed from 4 weeks to 2.** You have a data-science MS. You know Python, NumPy, and
Jupyter. What a DS track usually skips is *software engineering* — packaging, testing, logging,
interfaces, and code that another person can run. That's the actual gap, so that's the target.

Do **not** re-learn Python syntax. If you find yourself reading "what is a list comprehension,"
you've misread this part.

### Week 1 — Engineering practice, not Python

- [x] WSL2 environment configured, dotfiles, shell you like
- [x] Virtual environments (`venv` / `uv`) and dependency pinning
- [x] Project layout: package vs script, `pyproject.toml`, imports that work
- [x] Type hints + `mypy`
- [x] `dataclasses`
- [x] `logging` (not `print`)
- [x] `argparse` and CLI design
- [x] `pathlib`
- [x] Exceptions and error boundaries
- [x] Git: branches, meaningful commits, `.gitignore`

### Week 2 — Testing, structure, and a real deliverable

- [x] **Project setup from an empty directory, unaided** — `uv init`, `pyproject.toml`,
      `src/` layout, `__init__.py`, `py.typed`, editable install, a console script on the path
- [x] `pytest`: fixtures, parametrize, what's worth testing
- [x] Debugging with `pdb` / debugger — not print statements
- [x] Separating I/O from logic (why it makes things testable)
- [x] README writing
- [x] A CI run on GitHub Actions

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

- [x] Compilation model: preprocessor → compile → link (and what each error looks like)
- [x] Headers, translation units, ODR
- [x] CMake — enough to build a multi-file project
- [x] Classes, constructors, destructors
- [x] References vs pointers vs values
- [x] `const` correctness

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

## Part 3 — Robotics Fundamentals · Weeks 8–12

**Two weeks of physical components first, then math, kinematics, and simulation.** A robot is
what it's made of, how it moves, and how it senses. Writing software for one without knowing
those parts leaves gaps that show up in debugging and in interviews. The components weeks were
added on a critique from Seth (MS Mechanical Engineering, robotics emphasis). Reasoning in
[docs/syllabus-revisions.md](docs/syllabus-revisions.md) §13.

The simulation part is still compressed, because you've used Gazebo before. The math is not
optional, though. Coordinate frames are the single most common source of robotics bugs, and
"I'll figure out transforms later" is a decision you pay for in Part 9.

**The four questions.** For every component in weeks 8–9, answer these in your own words: *what
physical principle does it use, what does it output, how does it connect, and how does it fail?*
The goal is not to memorize a parts catalogue. It's being able to pick up a component you've
never seen, read its datasheet, and answer the four questions.

**Bench kit, ~$100–150. Order by week 6.** Raspberry Pi 5 (it becomes the robot's computer in
Part 6), an ESP32 dev board (3.3 V logic — mind your 5 V breakouts), breadboard and jumpers, a multimeter, an IMU breakout,
a DC gear motor with a quadrature encoder and a motor driver, a hobby servo, a small stepper and
its driver, an ultrasonic rangefinder, and a thermocouple with an amplifier board. Plus a battery
pack or bench supply that can run the motors.

### Week 8 — Components I: compute, interfaces, sensing

- [ ] Microcontroller vs single-board computer, and why real robots use both (the real-time
      loop on one, Linux and planning on the other). ESP32 specifics: 3.3 V logic and level
      shifting, FreeRTOS tasks, a noisy nonlinear ADC
- [ ] GPIO, pull-ups, debouncing, interrupts; PWM; analog signals and the ADC
- [ ] Buses: UART, I2C, SPI. How each is wired, addressed, and clocked, and when each is used.
      CAN: what it is and why vehicles and robot arms use it
- [ ] Read one sensor from its datasheet register map, with no library
- [ ] Proprioceptive sensors, which measure the robot itself: encoders (incremental, absolute,
      quadrature), IMU (accelerometer, gyro, magnetometer), current sensing, force/torque,
      limit switches
- [ ] Exteroceptive sensors, which measure the world: camera, LiDAR, radar, ultrasonic,
      time-of-flight, bump
- [ ] Environmental sensors: thermocouple (and cold-junction compensation), thermistor, and the
      analog chain from physical quantity to bits
- [ ] How sensors lie: noise, drift, bias, quantization, sampling rate, latency. This is why
      sensor fusion exists
- [ ] Power: batteries (LiPo safety), regulators, common ground, and why motors brown out a Pi

### Week 9 — Components II: actuators and control

- [ ] Actuators: brushed DC, brushless with ESC, stepper, hobby servo vs smart servo, and linear
      actuators (lead/ball screw, belt, pneumatic; hydraulic conceptually)
- [ ] Transmissions: gear ratios and the torque–speed trade, backlash, belts, harmonic drives.
      Torque–speed curves and stall current
- [ ] Driving actuators: H-bridge and motor drivers, step/direction, servo PWM
- [ ] Open loop vs closed loop, and what a stepper does when it misses steps
- [ ] PID: what P, I and D each do, integral windup, derivative noise. Tune a real motor with
      an encoder and plot the step response
- [ ] Mounting: IMU placement and vibration, why a mount that isn't rigid invalidates your
      extrinsics, field of view and occlusion, cable strain relief

### Components deliverable — Bench Rig

- A real IMU, read over I2C in C++, added to the week-7 sensor bus **without modifying the core**.
  This is Boss Fight #2 again, this time with hardware.
- A DC motor under PID velocity or position control, with a plotted step response and a
  paragraph on how you tuned it.
- A README with a four-questions table for every part on the bench.

> **WSL note:** the Pi is its own Linux machine, so reach it over SSH. The Arduino connects
> over USB, which WSL only sees through `usbipd-win`. Flashing from Windows is fine.

### Week 10 — Robotics mathematics

- [ ] Coordinate systems and frame conventions
- [ ] Vectors, matrices, matrix multiplication as transformation
- [ ] Rotation matrices
- [ ] Euler angles, and why they betray you (gimbal lock)
- [ ] Quaternions — enough to use them correctly
- [ ] Homogeneous transforms and composing them

You don't need mathematical perfection. You need intuition and correct signs.

### Week 11 — Kinematics

- [ ] Frames, links, joints, and how the joints map to the actuators from week 9
- [ ] Forward kinematics
- [ ] Inverse kinematics (concept + one worked 2-link example by hand)
- [ ] Joint space vs Cartesian space
- [ ] Differential-drive kinematics: from wheel encoder ticks to robot velocity

### Week 12 — Simulation

- [ ] Gazebo refresher (you've seen this — go faster)
- [ ] URDF: robot description from scratch
- [ ] Physics, collision meshes vs visual meshes
- [ ] Simulated sensor plugins, and which of the week-8 failure modes they don't model
- [ ] The simulation loop, real-time factor, determinism

### Deliverable — Your First Robot

A simulated differential-drive robot with wheels, LiDAR, a camera, and odometry. You should be
able to teleop it.

### 🥊 Boss Fight #3

Write a controller that makes the robot **drive forward → detect obstacle → stop.**

That's it. No autonomous navigation. Small, complete wins build the confidence that carries the
hard months.

---

## Part 4 — ROS 2 · Weeks 13–17

**Expanded from 4 weeks to 5.** ROS 2 is the backbone of everything after this and the single
most valuable line on a robotics résumé. Depth here pays compound interest.

> **Distro decision required before Week 13.** See [docs/environment.md](docs/environment.md) —
> your machine currently has only Ubuntu 26.04, which constrains the choice.

### Week 13 — Foundations

- [ ] Installation, sourcing, workspace layout
- [ ] Packages, `colcon`, build/install/devel
- [ ] Nodes and the node lifecycle
- [ ] `ros2` CLI — become fast with it, it's your debugger

### Week 14 — Topics

- [ ] Publishers, subscribers, message types
- [ ] Custom messages
- [ ] QoS profiles — and what actually happens when they mismatch
- [ ] Executors, callback groups, spinning
- [ ] `ros2 topic echo/hz/bw`, `rqt_graph`

### Week 15 — Services, actions, parameters

- [ ] Services (request/response)
- [ ] Actions (long-running, cancellable, with feedback)
- [ ] Choosing between topic / service / action — this is a design skill
- [ ] Parameters and reconfiguration
- [ ] Launch files (Python launch), composing systems

### Week 16 — Transforms and description

- [ ] TF2 — the tree, broadcasting, listening
- [ ] Static vs dynamic transforms
- [ ] Debugging frame errors (`tf2_echo`, `view_frames`)
- [ ] URDF + Xacro
- [ ] RViz2 — configure it well, you'll live here

### Week 17 — Tooling and rigor

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

## Part 5 — Navigation · Weeks 18–21

### Week 18 — State estimation

- [ ] Odometry and wheel encoders
- [ ] Dead reckoning and why drift is inevitable
- [ ] The localization problem
- [ ] Kalman filter — intuition, then the equations
- [ ] `robot_localization` / EKF fusion

### Week 19 — Mapping

- [ ] Occupancy grids
- [ ] SLAM concepts: front end, back end, loop closure
- [ ] `slam_toolbox`
- [ ] Map serving and AMCL localization

### Week 20 — Planning

- [ ] Configuration space
- [ ] Dijkstra, A*, and the heuristic that makes A* work
- [ ] Global vs local planning
- [ ] Costmaps, inflation layers
- [ ] Collision checking
- [ ] DWB / MPPI local control

### Week 21 — Nav2

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

## Part 6 — Physical Robot · Weeks 22–24

**New.** The original syllabus was 52 weeks of pure simulation. Every applicant has Gazebo
videos; almost none have dealt with a robot that physically falls over. This is the single
highest-leverage addition to your portfolio, and it's the part interviewers will ask about.

**Budget: ~$250–400.** Raspberry Pi 5, differential-drive base with encoders, RPLIDAR A1, a
camera, a battery, and a motor driver. The Pi and the IMU carry over from the Part 3 bench kit.
Order the rest during Part 5 — shipping will otherwise become the bottleneck.

Prefer separate parts over a pre-integrated kit where it's cheap to do so. Mount the LiDAR and
IMU yourself rather than using a pre-drilled plate. The mounting decisions are part of the lesson.

### Week 22 — Bring-up

- [ ] Ubuntu + ROS 2 on the Pi
- [ ] Cross-machine ROS 2 (DDS discovery over the network — expect pain, budget for it)
- [ ] Motor driver and `cmd_vel`, with the wheel-velocity PID loop from week 9 running on the
      ESP32, bridged to ROS 2 with micro-ROS (serial first; WiFi carries telemetry, never the loop)
- [ ] Encoder reading and odometry publishing
- [ ] Teleop a real robot

### Week 23 — Real sensors

- [ ] LiDAR driver, real scan data
- [ ] Camera driver, real images
- [ ] Your I2C IMU from week 8, now as a ROS 2 node, fused into odometry
- [ ] Calibration: camera intrinsics, LiDAR and IMU mounting transforms
- [ ] Time synchronization and message filters
- [ ] Compare real sensor noise against your sim assumptions — write down every difference

### Week 24 — Port the stack

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

## Part 7 — Perception · Weeks 25–28

### Week 25 — Camera geometry

- [ ] Pinhole model, intrinsics, distortion
- [ ] Extrinsics and camera↔robot transforms
- [ ] RGB, depth, stereo, point clouds
- [ ] Projection and back-projection — by hand, at least once

### Week 26 — Classical CV

- [ ] OpenCV fundamentals
- [ ] Color spaces, thresholding, morphology
- [ ] Edges, contours, features
- [ ] When classical CV beats a neural network (more often than you'd think)

### Week 27 — Detection

- [ ] Detection vs classification vs segmentation
- [ ] Bounding boxes, IoU, NMS
- [ ] Confidence and calibration
- [ ] Running a pretrained detector (YOLO or similar)
- [ ] Dataset concepts, labeling, class imbalance

### Week 28 — Perception in ROS

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

## Part 8 — Deep Learning · Weeks 29–31

**Compressed from 4 weeks to 3.** Your DS background covers tensors, training loops, loss
functions, overfitting, and metrics. Skim those hard and spend the time on what's actually new:
convolutional architectures, vision-specific training, and deployment.

If any of Week 29's list is genuinely unfamiliar, stop compressing and take the fourth week.
Be honest with yourself here — this is the one place where the DS asterisk could cut either way.

### Week 29 — PyTorch fluency (fast)

- [ ] Tensors, devices, dtypes
- [ ] `Dataset` / `DataLoader`, collate, augmentation
- [ ] Autograd mechanics — what `backward()` actually does
- [ ] Training loop, validation split, checkpointing
- [ ] Reproducibility: seeds, determinism

### Week 30 — Vision

- [ ] CNNs: convolution, stride, padding, receptive field
- [ ] Modern backbones (ResNet, and why residuals)
- [ ] Transfer learning and fine-tuning
- [ ] Augmentation strategy
- [ ] Detection fine-tuning on a custom dataset
- [ ] Error analysis — look at the failures, individually

### Week 31 — Deployment

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

## Part 9 — AI + Robotics · Weeks 32–35

Where the previous eight parts connect.

### Week 32 — Inference in the loop

- [ ] Model inference inside a ROS 2 node
- [ ] Threading: don't block the executor
- [ ] Real-time constraints and dropping frames gracefully
- [ ] Detection message design

### Week 33 — 3D localization

- [ ] From bounding box to 3D position (depth, stereo, or geometry)
- [ ] Camera → robot → map frame chains
- [ ] Uncertainty propagation
- [ ] Publishing detections into TF

### Week 34 — Tracking

- [ ] Multi-object detection
- [ ] Data association
- [ ] Track lifecycle: birth, update, death
- [ ] Temporal consistency and filtering

### Week 35 — Perception-driven behavior

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

## Part 10 — Manipulation + Behavior · Weeks 36–40

**Expanded to 5 weeks and given an arm.** The original syllabus taught inverse kinematics in
week 10, then asked you to "pick object / place object" in month 9 with a robot that had no
manipulator. This fixes that inconsistency — and manipulation is where a large share of robotics
hiring actually is.

The arm is simulated (Franka Panda or UR5 in Gazebo). Do not buy one.

### Week 36 — Arm kinematics

- [ ] Serial manipulators, DH parameters
- [ ] Forward kinematics for a 6/7-DOF arm
- [ ] Analytical vs numerical IK
- [ ] Jacobians, singularities, redundancy
- [ ] Workspace limits

### Week 37 — MoveIt 2

- [ ] MoveIt 2 architecture and setup assistant
- [ ] Planning scene and collision objects
- [ ] Motion planning (OMPL), planning groups
- [ ] Cartesian paths
- [ ] Grasp pose generation and execution

### Week 38 — State machines and behavior trees

- [ ] Finite state machines: states, events, guards, recovery
- [ ] Behavior trees: why robotics prefers them
- [ ] BehaviorTree.CPP and Nav2's BT integration
- [ ] Reactive vs deliberative behavior

### Week 39 — Task composition

- [ ] Task planning and preconditions
- [ ] Trajectory constraints
- [ ] Collision checking during execution
- [ ] Blackboards and shared state

### Week 40 — Robustness

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

## Part 11 — Modern Robot Learning · Weeks 41–42

**Substantially rewritten, then compressed from 4 weeks to 2** to pay for the Part 3
components weeks (see [syllabus-revisions.md](docs/syllabus-revisions.md) §13). The original gave
you MDPs, Q-learning, and PPO — a solid but roughly 2019 curriculum. That's not what's moving
robotics right now, and "left behind by recent developments" is the reason you started this. The
current centre of gravity is **learning from demonstration at scale**: behavior cloning,
diffusion policies, and vision-language-action models.

RL is now vocabulary only, with no dedicated week. What got cut is depth, not coverage. If
interviews from week 24 onward show that RL depth is what the market wants from you, take a
week back from here.

### Week 41 — RL vocabulary + imitation learning

- [ ] RL vocabulary: MDP, policy, value, reward, PPO in one paragraph, and why pure RL is hard
      on real robots (sample complexity, reward design, safety)
- [ ] Behavioral cloning and the compounding-error problem
- [ ] DAgger and interactive correction
- [ ] Demonstration collection — teleoperate your own robot to gather data
- [ ] LeRobot: datasets, training, evaluation
- [ ] Action chunking (ACT)

### Week 42 — Diffusion policies + VLAs

- [ ] Diffusion policies: enough theory to understand why they suit multimodal actions
- [ ] Train a diffusion policy in LeRobot; evaluate success rate, and why it's noisy
- [ ] Vision-language-action models: the RT-2 → OpenVLA → π0 lineage; run one open checkpoint
- [ ] Domain randomization and sim-to-real — connect this to what you measured in Boss Fight #6
- [ ] *Optional, if time allows:* Isaac Lab vectorized environments. Otherwise randomize in Gazebo

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

> If you followed the background threads, you've been applying since week 24 and have real
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

**Hardware** — what robots are made of: actuators, sensors, microcontrollers vs SBCs, buses,
power, and PID on a real motor. Enough to read a datasheet and debug across the software/hardware
line.

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
