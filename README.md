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

## Projects

One directory per project, each with its own README
([template](docs/templates/project-README.md)).

| Project | Lang | Week | What it is |
| --- | --- | --- | --- |
| [telemetry/](telemetry/) | Python | 1–2 | Load a telemetry CSV; parse, validate, analyze, report. |
| [boss-fights/](boss-fights/) | Py / C++ | — | Blank-page rebuilds of the previous weeks' work. 01: telemetry toolkit. |
| [cpp_telemetry/](cpp_telemetry/) | C++ | 3 | Scoped C++ port of `telemetry/` — per-robot temperature stats. A language review, not a feature extension. |
| [cpp_memory/](cpp_memory/) | C++ | 4 | Test bed for memory lessons: leaks, ASan, RAII, move semantics. History is in the commits. |

`cpp_test/` is a gitignored local scratch area.

## Docs

| Doc | Purpose |
| --- | --- |
| [docs/00-dashboard.md](docs/00-dashboard.md) | Weekly progress, updated Sundays |
| [docs/background-threads.md](docs/background-threads.md) | Build log, interviews, applications |
| [docs/textbook/](docs/textbook/README.md) | Write-ups of lessons from sessions |
| [docs/syllabus-revisions.md](docs/syllabus-revisions.md) | Why the syllabus differs from the first draft |
| [docs/ta-notes.md](docs/ta-notes.md) | TA session notes |
