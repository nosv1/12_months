# TA notes

Working notes kept by Claude, in the repo so any session on any machine can pick up where the
last one stopped. Not a diary and not a progress log — those are
[00-dashboard.md](00-dashboard.md) and [background-threads.md](background-threads.md).

Read this at the start of a session. Update it at the end, and commit it.

---

## Where things stand

**Last updated:** 2026-09-09 (end of day 1)

- Curriculum started **Wed 2026-09-09**. Day 1 landed on the syllabus's designated *off* day, so
  don't infer the current week or day-of-rhythm from the calendar — check the dashboard or ask.
- Repo is a git repository on branch `dev`. First commits are in.
- Part 1 deliverable lives at `telemetry/` — uv project, src-layout (`telemetry/src/telemetry/`),
  no dependencies yet, still the `uv init` scaffold.

## Open thread — owed before code is written

Chris is to bring **module boundaries** for the telemetry pipeline:

```
raw data → parser → validation → analysis → report
```

The question is not "what files" but **what each stage hands to the next, and what each one
refuses to know about**. Probe already put to him: *if your parser knows what a warning
threshold is, you've already lost.*

My job there is to poke holes in his design. Not to produce one.

Remaining week 1 checklist items — type hints + mypy, dataclasses, logging, argparse, pathlib,
exceptions — are meant to be exercised *while building this*, not studied as separate topics.

**Boss Fight #1** (week 2) is a blank-page rebuild of this toolkit. Strictly hands-off once it
starts — see CLAUDE.md.

## How to work with him — learned, not in CLAUDE.md

**Verify before advising.** When he reports something done, check the actual state with bash
first. On day 1 every such report was partially incomplete:

| Reported | Actually |
|---|---|
| "git init done, dev branch created" | no commits, no `.gitignore` |
| "committed" | only `telemetry/` — syllabus, docs, `.gitignore` left untracked (`git add *` from a subdirectory; the shell expands `*`, skipping dotfiles) |
| "`.gitignore` fixed" | patterns path-anchored, so nested `__pycache__/` wasn't matched |

None of this is carelessness — it's the small tooling detail that never announces itself, which
is exactly the gap Part 1 exists to close. He responded well to each catch and fixed them
himself. **Name what's wrong and why it matters; don't fix his repo for him.** Tooling,
environment, and docs files are the stated exception.

He is on limited evening hours. Lead with the answer.

## Decisions made, so they don't get relitigated

- **uv over pip.** The lockfile is the point, not the speed. `uv.lock` is committed; `.venv/` is
  not.
- **Python 3.12**, because Noble ships it and Jazzy is built against it — not a free choice.
- **Every project gets its own directory** with its own `pyproject.toml`. The repo root is the
  curriculum, not a package.
- **Commits Claude makes are authored as Claude**, not as Chris:
  `git commit --author="Claude <noreply@anthropic.com>"`. This repo is evidence of Chris's own
  work, so authorship has to be honest about who wrote what. A `Co-Authored-By` trailer is not
  sufficient — it claims he co-wrote it.
- Filenames stay boring: no spaces, no glob metacharacters. An earlier `*c` suffix convention
  was reverted — `*` is illegal on NTFS and would break checkout on the Windows side of the
  planned dual-boot.
