# Decisions made, so they don't get relitigated

Back to the [TA notes index](../ta-notes.md). Read before proposing a process, tooling, or
repo-convention change.

## Process

- **Boss Fight #1 may spill into week 3** (2026-09-12). His goal: done by Sun Sep 20 night. Log in
  the dashboard slippage table only if it actually spills.
- **Week files follow syllabus progress; hours lines are dated by calendar day** (2026-09-12).
  Week-2 work started Sat Sep 12 evening and lives in `week-02.md`. Slippage is still judged
  against the nominal calendar (week 3 ≈ Mon Sep 21).
- **He writes his own time estimates** in the week file before starting; actuals go beside them.
  Estimates name a checkable end state, not a topic. Compare on Sundays.
- **Session goals are outcomes he can check**, phrased as the problem, not the tool (2026-09-12).
  "Every bad row has a failing-if-broken test", not "understand parametrize."
- **Ticks happen on Sunday, after review** — not when he feels done.
- **Working off days (Wed–Sat) is his call.** Accepted 2026-09-12. Revisit only if hours drop or he
  reports burnout, around week 4.
- **Toolchain prereq not added to the syllabus.** Installed and verified before week 3, so moot.

## Tooling and layout

- **uv over pip.** The lockfile is the point, not the speed. `uv.lock` committed; `.venv/` not.
- **Python 3.12**, because Noble ships it and Jazzy is built against it — not a free choice.
- **Every project gets its own directory** with its own `pyproject.toml`. The repo root is the
  curriculum, not a package.
- **Filenames stay boring:** no spaces, no glob metacharacters. An earlier `*c` suffix convention
  was reverted — `*` is illegal on NTFS and would break checkout on the Windows side of the
  planned dual-boot.

## Authorship and docs

- **Commits Claude makes are authored as Claude**, not as Chris:
  `git commit --author="Claude <noreply@anthropic.com>"`. This repo is evidence of his own work, so
  authorship has to be honest. A `Co-Authored-By` trailer alone is not sufficient — it claims he
  co-wrote it. When a file mixes his uncommitted edits with mine, stage only my hunk.
- **Textbook entries are numbered in learning order**, not syllabus order — renumbering would break
  links. Written by me, committed as Claude, whenever a real lesson is given.
- **TA notes are split into an index plus files** (2026-09-12, his suggestion — the single file got
  "chunky"). Index stays short; history goes in `sessions/`.
