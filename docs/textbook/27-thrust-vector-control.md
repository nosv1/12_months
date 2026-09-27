# 27 — Thrust vector control: balancing a pencil on a jet

**Week 5 (preview of weeks 8–9).** No syllabus item yet. Previews *IMU* (week 8) and *PID
control* (week 9).

Prompted by a car-ride conversation about aerospace and BPS Space's model rockets. The question
was "what is this thrust vector stuff?"

---

## The problem: a rocket wants to flip

A rocket's engine pushes from the bottom. If the thrust line doesn't pass exactly through the
**center of mass**, the thrust creates a torque and the rocket starts to rotate. Once it tilts,
the thrust points further off-center, which tilts it more. Left alone, it's unstable, like
balancing a broom on your palm.

Model rockets usually solve this passively. Fins at the tail put the **center of pressure** (where
aerodynamic force acts) behind the center of mass, so the airflow straightens the rocket out, the
same way feathers stabilize an arrow. The catch is that fins need airspeed. At liftoff, or in
vacuum, they do nothing.

## The fix: steer the engine

**Thrust vector control (TVC)** mounts the engine on a **gimbal**, a two-axis pivot, and tilts it
a few degrees. Tilting the thrust creates a sideways torque on the rocket. Point the engine the
right way and that torque cancels the tip-over. It's your palm moving under the broom.

Falcon 9 and Starship gimbal their engines. BPS Space does the same on hobby rockets, with two
servos tilting the motor mount.

## The loop

Many times per second:

```text
IMU (gyro + accel) → attitude estimate → controller (PID) → servo angles → gimbal → torque
        ↑                                                                              │
        └──────────────────── the rocket's actual rotation ────────────────────────────┘
```

1. **Sense.** The gyro measures rotation *rate* (rad/s) on each axis.
2. **Estimate.** Integrate rate to get angle: which way is the rocket pointing?
3. **Decide.** Error = desired angle − estimated angle. A PID controller turns error into a
   gimbal command.
4. **Act.** Servos tilt the motor, which produces torque and changes the rotation, which the gyro
   measures on the next pass.

## Why it's hard

- **Drift.** Integrating a gyro accumulates error, the same effect as the week-5 accel → velocity
  experiment, one derivative up. Real systems fuse the gyro with other sensors (a complementary
  filter or an EKF, week 18).
- **Speed.** A small rocket can flip in a fraction of a second. The loop has to run fast, and
  servo lag eats part of the budget.
- **The plant changes during flight.** Thrust follows the motor's thrust curve, and mass drops
  as propellant burns. Gains that are right at ignition can be wrong at burnout.
- **One shot.** You can't pause a flight and attach a debugger, so logging telemetry matters (week
  2 again).

## A bench version

A version that never leaves the table. The bench kit already has the parts: ESP32, IMU, servos.

1. **No thrust.** Gimbal an arm with two servos and mount the IMU on the base. Tilt the base by
   hand, and the gimbal should counter-steer to keep the arm vertical. This tests the sense →
   estimate → act loop.
2. **Thrust, still tethered.** Replace the rocket motor with an electric ducted fan on a pivoting
   stand. There's real torque and real instability, and no pyrotechnics.

Clamped stands and electric thrust only. Launching rockets brings its own safety rules and
regulations.

## Open questions

- Why does a PID's **D** term matter so much here? What does it react to that P doesn't?
- If thrust doubles, what happens to how strongly each degree of gimbal tilts the rocket, and what
  should happen to the gains?
- A drone's attitude controller does the same job with no gimbal. What does it use for torque
  instead?

## Where this returns

Week 8 (IMU: gyro vs accel, how each fails), week 9 (PID, cascaded loops), week 18 (state
estimation), and the aerial hooks in [ta-notes/observations.md](../ta-notes/observations.md) 09-27.
