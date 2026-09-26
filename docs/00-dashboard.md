# Dashboard

Single source of truth. Update every Sunday.

**Started:** Wed 2026 Sep 9   **Current week:** 4   **Hours logged:** 46.00

---

## Parts

| Part | Weeks | Focus | Status |
| --- | --- | --- | --- |
| 1 | 1–2 | Reactivation | ✓ |
| 2 | 3–7 | C++ + Linux systems | ☐ |
| 3 | 8–12 | Components + robotics fundamentals | ☐ |
| 4 | 13–17 | ROS 2 | ☐ |
| 5 | 18–21 | Navigation | ☐ |
| 6 | 22–24 | Physical robot | ☐ |
| 7 | 25–28 | Perception | ☐ |
| 8 | 29–31 | Deep learning | ☐ |
| 9 | 32–35 | AI + robotics | ☐ |
| 10 | 36–40 | Manipulation + behavior | ☐ |
| 11 | 41–42 | Modern robot learning | ☐ |
| 12 | 43–45 | Systems engineering | ☐ |
| 13 | 46–52 | Capstone + career | ☐ |

## Weeks

```
01 [x]  02 [x]  03 [x]  04 [ ]  05 [ ]  06 [ ]  07 [ ]  08 [ ]  09 [ ]  10 [ ]
11 [ ]  12 [ ]  13 [ ]  14 [ ]  15 [ ]  16 [ ]  17 [ ]  18 [ ]  19 [ ]  20 [ ]
21 [ ]  22 [ ]  23 [ ]  24 [ ]  25 [ ]  26 [ ]  27 [ ]  28 [ ]  29 [ ]  30 [ ]
31 [ ]  32 [ ]  33 [ ]  34 [ ]  35 [ ]  36 [ ]  37 [ ]  38 [ ]  39 [ ]  40 [ ]
41 [ ]  42 [ ]  43 [ ]  44 [ ]  45 [ ]  46 [ ]  47 [ ]  48 [ ]  49 [ ]  50 [ ]
51 [ ]  52 [ ]
```

## Boss fights

The real progress metric. Each is a blank-page rebuild — no tutorial, no copying prior work.

| # | Week | Challenge | Passed |
| --- | --- | --- | --- |
| 1 | 2 | Rebuild telemetry analyzer from empty dir | ✓ |
| 2 | 7 | Add a sensor type without touching the core | ☐ |
| 3 | 12 | Drive forward → detect obstacle → stop | ☐ |
| 4 | 17 | Three-node ROS system, correct interfaces | ☐ |
| 5 | 21 | Navigate past random obstacles | ☐ |
| 6 | 24 | Diagnose and write up the sim-to-real gap | ☐ |
| 7 | 28 | Locate an object in the robot's frame | ☐ |
| 8 | 31 | Unfamiliar dataset → trained model | ☐ |
| 9 | 35 | Find the named target among distractors | ☐ |
| 10 | 40 | Recover from deliberate failures | ☐ |
| 11 | 42 | Policy survives environment change | ☐ |
| 12 | 45 | System survives a killed component | ☐ |
| 👑 | 52 | Ambiguous brief, empty repo, one week | ☐ |

**#1, 2026-09-19/20 — built in 9h38m against a 6h estimate. Passed 2026-09-24, with gaps on record.** Rebuilt from an empty
directory: reader, parser, validator, grouper, report, console script, 38 tests. §1-§6 largely hold,
including multi-error rows and correct unattributed rejects. Open against the contract: the shipped
artifact is a stale `uv tool install` copy that prints a dict repr rather than JSON (§8), a bad
header silently discards the whole file, and the `20`/`60` thresholds still require a source edit
plus reinstall (§5). The report also omits `robot_id` per robot (§7). Called a pass because the
fight tests blank-page design and build, which held; the gaps are first-release defects, not
missing capability. Not being rebuilt. Review in
[boss-fights/01-telemetry/NOTES.md](../boss-fights/01-telemetry/NOTES.md).

## Deliverables

- [ ] Telemetry toolkit (wk 2)
- [ ] Sensor simulator (wk 7)
- [ ] Bench rig: real IMU on the sensor bus, PID motor (wk 9)
- [ ] Simulated robot (wk 12)
- [ ] ROS robot system (wk 17)
- [ ] Autonomous navigation (wk 21)
- [ ] **Physical robot** (wk 24)
- [ ] Perception pipeline (wk 28)
- [ ] Vision model, own dataset (wk 31)
- [ ] Vision-guided robot (wk 35)
- [ ] Pick-and-place task system (wk 40)
- [ ] Learned policy (wk 42)
- [ ] Production stack (wk 45)
- [ ] Capstone (wk 50)

## Portfolio

- [ ] **Autonomous Mobile Robot (physical)** — lead with this one
- [ ] Vision-Guided Robot
- [ ] Autonomous AI Robot
- [ ] VLA paper reimplementation

## Background threads

See [background-threads.md](background-threads.md).

- [ ] Build log started (wk 1) — current streak: ___ weeks
- [ ] Interview problems (from wk 20) — total: ___
- [ ] Applications (from wk 24) — sent: _**· screens:**_ · onsites: ___
- [ ] Open-source PR merged (by wk 40)

## Career

- [ ] Résumé rewritten around systems built
- [ ] GitHub profile + 3 pinned projects
- [ ] LinkedIn
- [ ] Mock interviews (3+)
- [ ] Bench kit ordered — **by wk 6**, for Part 3 components weeks 8–9
- [ ] Robot BOM ordered — **do this in Part 5, wk 18–21, or shipping blocks wk 22**
- [ ] Native Ubuntu dual-boot — target wk 8, required by wk 22

## Open decisions

- [x] ROS 2 distro → **Ubuntu 24.04 + Jazzy** (settled Sept 2026)
- [ ] Robot chassis / BOM finalized
- [ ] Capstone scope

---

## Slippage log

Weeks missed and why. Not for guilt — for spotting patterns before they become a missed month.

| Week | What happened | Recovered? |
|---|---|---|
| 2 | Ran 10 days instead of 7 and 27.3h against a 10-12h budget (~2.5x). Boss Fight #1 took 9.65h vs a 6h estimate; the rest went to first-time engineering setup — pytest suite, GitHub Actions, `pyproject.toml`, `py.typed`, `uv tool install`, first debugger session. Calendar slip: 3 days. | Partially — hours are above budget, not below, so the deficit is output per hour, not effort. Watch whether week 3 also lands near 1.6x before treating it as a trend. |
