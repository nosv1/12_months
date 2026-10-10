# Motorcycle telemetry (idea, 2026-10-10)

His bike: **2025 Honda CBR500R**. He thinks of it as a test platform, even off-track. Idea: a Pi
with sensors, logging rides. "Interesting, useful or not, probably not."

## Why it matters

The first hardware idea with a **reason built in**: a platform he cares about and rides anyway. The
kit stalled because it was buying to learn. This is buying to answer a question about his own bike.

It lines up with syllabus week 8 (compute, interfaces, sensing): IMU and GPS over I2C, SPI, and
serial; sample rates; logging. It also lines up with the telemetry work he's already done and the
race engineer (same analysis skills, a real vehicle).

## Real-world lessons it would force

Vibration, power loss corrupting the SD card, GPS dropouts, mounting, heat, rain. These are exactly
what simulation leaves out.

## Safety rules (non-negotiable)

- **Self-contained and battery-powered first.** Don't splice into the bike's wiring.
- Mount it so it can't come loose into anything that moves.
- No screens and no fiddling while riding. Review the data afterwards.
- Leave the bike's own electronics alone until he's researched them. It may have a diagnostic port;
  read-only, and only once he knows what it does.

## Open question (his)

What would he want to see after a ride? Lean angle, braking and acceleration g, speed over a GPS
trace? That answer defines the first build.

Design and parts are his. Flight-instructor terms.
