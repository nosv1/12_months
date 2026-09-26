# 12 Months — Robotics + AI

A 52-week self-directed curriculum: rusty CS grad → employable robotics/AI engineer.
The plan is [SYLLABUS.MD](SYLLABUS.MD); progress is in [docs/00-dashboard.md](docs/00-dashboard.md).

## Setup

```powershell
wsl --set-default Ubuntu-24.04
```

```bash
cd ~
git clone https://github.com/nosv1/12_months.git
```

Clone inside WSL (`~/`), not `/mnt/c/` or OneDrive. Toolchain and gotchas:
[docs/environment.md](docs/environment.md). C++ toolchain: [scripts/install-cpp-toolchain.sh](scripts/install-cpp-toolchain.sh).

## Layout

Work is filed by *kind*; the week lives in the tables below, not the root.

```text
projects/      part deliverables — the portfolio pieces (one per syllabus part)
labs/          weekly exercises and test beds, named wNN-topic/
boss-fights/   blank-page rebuilds, named NN-topic/
ros_ws/        colcon workspace, from week 13 (ROS 2) — packages go in ros_ws/src/
docs/          dashboard, build log, textbook, TA notes
scripts/       machine setup
```

`labs/scratch/` is gitignored — throwaway experiments. Every other directory gets a README.

## Projects

| Project | Lang | Week | What it is |
| --- | --- | --- | --- |
| [projects/telemetry/](projects/telemetry/) | Python | 1–2 | Load a telemetry CSV; parse, validate, analyze, report. |

## Labs

| Lab | Lang | Week | What it is |
| --- | --- | --- | --- |
| [w03-cpp-telemetry/](labs/w03-cpp-telemetry/) | C++ | 3 | Scoped C++ port of `projects/telemetry` — per-robot temperature stats. A language review, not a feature extension. |
| [w04-cpp-memory/](labs/w04-cpp-memory/) | C++ | 4 | Test bed for memory lessons: leaks, ASan, RAII, move semantics. History is in the commits. |

## Boss fights

| Fight | Lang | After week | What it is |
| --- | --- | --- | --- |
| [01-telemetry/](boss-fights/01-telemetry/) | Python | 2 | Blank rebuild of the telemetry toolkit. |

## Docs

| Doc | Purpose |
| --- | --- |
| [docs/00-dashboard.md](docs/00-dashboard.md) | Weekly progress, updated Sundays |
| [docs/background-threads.md](docs/background-threads.md) | Build log, interviews, applications |
| [docs/textbook/](docs/textbook/README.md) | Write-ups of lessons from sessions |
| [docs/syllabus-revisions.md](docs/syllabus-revisions.md) | Why the syllabus differs from the first draft |
| [docs/ta-notes.md](docs/ta-notes.md) | TA session notes |
