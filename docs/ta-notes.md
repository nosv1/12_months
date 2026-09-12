# TA notes

Working notes kept by Claude, in the repo so any session on any machine can pick up where the
last one stopped. Not a diary and not a progress log — those are
[00-dashboard.md](00-dashboard.md) and [background-threads.md](background-threads.md).

Read this at the start of a session. Update it at the end, and commit it.

---

## Where things stand

**Last updated:** 2026-09-12 (Saturday, end of week-1 day 4). He may return tonight or Sunday.

- Curriculum started **Wed 2026-09-09**. Weeks are **calendar-aligned (Mon–Sun)**: week 1 was a
  short week entered on Wednesday, week 2 is **Sep 14–20**, week 3 (C++) starts **Mon Sep 21**.
  He asked about this; he is not behind.
- **All ten Week-1 syllabus items ticked, and verified**: mypy clean, `uv run telemetry
  data/sample_telemetry.csv output` works end to end, logging / argparse / pathlib / exceptions
  genuinely in the code. ~8h logged over 4 days.
- Working tree clean except his `scratchpad.md`.
- **Zero tests.** `telemetry/tests/test.py` still collects nothing. Week-2 item, but also the
  CLAUDE.md "tests from week 1" convention — which did not happen.
- **C++ toolchain not installed** (`gcc g++ cmake gdb valgrind docker` all missing;
  `environment.md` toolchain checklist all unticked). Offered to write the install-and-verify
  script — that's tooling, fine to write. He may start on "prereqs" tonight.

## Day 4 (2026-09-12) — what happened

Big day. In order:

1. **Falsy-return bug fixed.** He moved from `(Validator, value)` tuples → annotating `-> float`
   while returning `None` (mypy flagged all six returns) → removed the value entirely (which forced
   re-converting every string in the parser — *he* noticed and disliked that) → validators that
   return the converted value and **raise `ValueError`**, with one `try`/`except` boundary around
   the per-row work. Chose that himself after I named two families (raise vs. result type) without
   implementing either. Said "was scared of the try catch and raising errors, but wasn't too bad."
2. `Validator` class → module-level functions. `nan` check now `math.isnan` on the value.
   `validate_velocity` gained a real rule (`abs(v) >= 2` rejected).
3. logging (`logger = getLogger(__name__)`, `%d` args), argparse with `type=Path`, pathlib
   (`mkdir(parents=True, exist_ok=True)`), `main()` function, **`main.py` renamed to `cli.py`**,
   `__init__.py` re-exports `main`, console script works. mypy moved to dev group.
4. **Warnings design re-litigated — he kept them in analysis**, with a written rationale in the
   README ("data is from a file, not live"). He also added the reading's timestamp to each warning,
   which was the real defect his instinct was detecting. Good outcome: he defended the placement
   in his own words, which is what I wanted.
5. README rewritten: setup/run first, input format, architecture, design decisions.
6. Asked whether the syllabus needs changing. **My answer: no structural change.** Week 1
   confirmed revision #1 (Python was never the gap; every time sink was engineering practice).
   Two recommendations he received well:
   - **Week 2 is overloaded** (pytest + CI both new, plus finishing the deliverable, plus Boss
     Fight #1 rebuilding all of it). Recommended deciding *now* that the boss fight may spill into
     week 3's first session, logged in the slippage table. **Not yet decided by him.**
   - **Add "toolchain installed and verified" as a Week 3 prerequisite.** Not yet edited into the
     syllabus — his call.

### Outstanding critique — not yet addressed

- README: "Timestamps should be in the future" is wrong (literally rejects historical data; real
  rule is *later than that robot's previous reading*). "Drop and record bad rows" and "LESSONS"
  are empty headers. The "Must have:" line is still the syllabus talking to him.
- CLI logs `Line 39 had a value error.` — the message omits *which* error. `str(ve)` is recorded
  in `bad_readings` but not logged.
- `cli.py` `main()`: `Path(args.x)` wraps a value `type=Path` already converted.
- `analysis.py` still uses `__`-mangled dataclass fields. (Divide-by-zero **is fixed** —
  `average_velocity` is `None` for a robot with no good readings.)
- `robot.plot()` now uses pathlib but is still commented out of `cli.py`. `import matplotlib` sits
  at the top of `robot.py`, so every run — and every test that imports `Robot` — pays for it.
  Every robot would also overwrite the same `plot.png`. WIP; don't review until he picks it up.
- **The truncated row is logged but never reaches the report** — it has no usable `robot_id`, so it
  goes nowhere. The unresolved "which list does it go in" question from day 2, still unresolved.
- Exceptions short-circuit, so `bad_readings` holds the *first* reason per row. He made that
  choice implicitly; never asked him to defend it.
- `Warning` still shadows the builtin. Dropped — flagged three times, his call.

### Next session

0. **`5af71c1` introduced a bug, pushed as he signed off.** The truncated-row branch in `cli.py`
   appends to `robot.bad_readings` *before* `robot` is assigned for that line — so it files the row
   under the **previous line's robot** (wrong robot, silently), or raises `NameError` if the first
   data row is truncated. mypy reports 1 error. Pointed at the line and the ordering only; the fix,
   and the day-2 question of where an unattributable row belongs, are his.

1. If he's doing prereqs: toolchain install script (I write it) → have him verify with a
   hello-world compile.
2. **First test ever.** The obvious first one: `validate_velocity("0.0") == 0.0` — the two-day bug
   as an assertion. Then arrange/act/assert, `test_*.py`, `pytest.raises`, `parametrize` over the
   planted defects. `main(argv)` taking an argument list makes the CLI testable.
3. Ask whether he's decided on the boss-fight spill policy.
4. README critique above, when he's in it.

## Boss Fight #1 — rules as stated to him (2026-09-12)

He asked "all code and everything, not just setup and paste in code?" Told him:

- **From an empty directory, all of it** — including `uv init`, `pyproject.toml`, layout, console
  script, `__init__.py`. Packaging was a week-1 time sink, so it's half the test.
- In scope: everything the finished deliverable has, including tests (and CI if week 2 landed it).
- **Allowed:** official docs, searching error messages, `sample_telemetry.csv` and the customer
  spec (they're input, not solution), me as rubber duck only.
- **Not allowed:** the old `telemetry/` directory or its README, copy-paste, me designing anything.
- **Grey area left to him:** the textbook. Recommended *not* opening it, because
  `02-exceptions…` contains his actual `validate_battery` fix and parser `try` block.
- Suggested its own directory (e.g. `boss-fights/01-telemetry/`) with commits as he goes.

During the fight: strictly hands-off per CLAUDE.md. Rubber-duck only.

## Telemetry — design history

Settled, by him:

- **`main`/`cli` orchestrates** (parse → analyze → report). His original blocker was picturing
  stages as separate programs passing files; explained in-process stages pass return values.
  Revisit at week 11 (ROS nodes *are* separate processes).
- **Bad rows dropped and recorded** on the `Robot` as `(line, message)`, fed into the report.
- **Warnings: Strategy pattern** in `warning.py`, detected in `analysis.py`, now carrying the
  reading's timestamp. Considered moving detection to the parser on day 4 and kept it in analysis
  with a batch-vs-live rationale.
- **Validation raises**; one error boundary per row in the parser.

### The sample data — I play the customer

I generated `telemetry/data/sample_telemetry.csv` (committed as Claude, `94b4543`) and gave a
customer-voice spec: ISO 8601 UTC, m/s, battery %, °C; **warn battery < 20%, temperature > 60 °C**.
I answer requirements questions in character — not design questions.

Deliberate defects — **still don't tell him; the boss fight reuses this file**:
`nan` velocity, blank battery, battery `104.2`, temperature `-273.2`, two amr-03 rows swapped
(per-robot timestamp regression), one exact duplicate row, one truncated row (4 fields),
velocity `ERR`. By design: amr-02 battery drops to ~16%, amr-03 overheats to ~66 °C, amr-01 parks
(v=0) ~12 s. Cross-robot timestamps interleave — normal.

**As of day 4 his code catches every planted defect.** One caveat: the swapped amr-03 pair only
ever flags the *second-arriving* row of the pair (the regression), never both. Whether that's
correct is a legitimate requirements question — if he asks, answer as the customer.
Verified run: 7 rows in `bad_readings` (−273.2, `ERR`, `nan`, duplicate, blank battery, 104.2,
swapped pair) + the truncated row logged only = all 8.

## Environment — verify block run 2026-09-10

OK: Ubuntu 24.04, RTX 5080 visible (driver 591.86), uv, git identity. **Missing:** `gcc`,
`cmake`, `gdb`, `valgrind` (needed before C++ starts), Docker (needed for CI/containers), no
`~/.ssh` (fine if pushing over HTTPS). PyTorch not yet checked. The toolchain checklist in
`environment.md` is still all unticked.

**Re-checked 2026-09-12: still missing** `gcc g++ cmake gdb valgrind docker clang`. Week 3 starts
Mon Sep 21.

**Boss Fight #1** (week 2) is a blank-page rebuild of this toolkit. Strictly hands-off once it
starts — see CLAUDE.md.

## How to work with him — learned, not in CLAUDE.md

**Verify before advising.** When he reports something done, check the actual state with bash
first. On day 1 every such report was partially incomplete:

| Reported | Actually |
| --- | --- |
| "git init done, dev branch created" | no commits, no `.gitignore` |
| "committed" | only `telemetry/` — syllabus, docs, `.gitignore` left untracked (`git add *` from a subdirectory; the shell expands `*`, skipping dotfiles) |
| "`.gitignore` fixed" | patterns path-anchored, so nested `__pycache__/` wasn't matched |

None of this is carelessness — it's the small tooling detail that never announces itself, which
is exactly the gap Part 1 exists to close. He responded well to each catch and fixed them
himself. **Name what's wrong and why it matters; don't fix his repo for him.** Tooling,
environment, and docs files are the stated exception.

He is on limited evening hours. Lead with the answer.

**Day 2 observations:**

- He was hesitant to ask "check my work" every step. I told him review at *decision points* is
  the high-value work — keep inviting it.
- He takes design pushback well and changes course (warnings → analysis) but defends first,
  sometimes with a weak reason ("flexibility", "perhaps"). Name the weak reason plainly; the
  interview framing ("could you defend this?") lands.
- Moves fast and edits documents piecemeal, which produces self-contradicting designs. He vented
  about it ("maybe I'm rushing"). Answered with accuracy, not reassurance: yes a little; reread
  top-to-bottom; move to type-checked code. That's the confidence-gap pattern from CLAUDE.md.
- Formatting markdown is fine for me to do (tooling). Suggested the markdownlint extension.
- Commit-message question: explained what/why over when. Watch whether commits get smaller.

**Day 4 observations:**

- Ticks run slightly ahead of evidence (ticked git before asking how to structure a commit; ticked
  pathlib while `robot.plot()` used `os.path.join`). Fixed fast both times — not dishonesty. Told
  him to tick on Sunday after review. Watch it.
- Works the syllabus off days (Wed, Thu, Fri, Sat this week). Raised it; his answer: he gets busy,
  so he uses time when he has the energy. **His call — accepted.** Revisit only if hours drop or he
  reports burnout, around week 4.
- He now asks *why* a design is the way it is before accepting it (warnings placement). That is
  the thing to encourage.
- He responds well to "you're allowed to overturn my earlier pushback if your reason is better."
- Asked mechanics questions directly (exception messages, `__init__.py`) — answered those outright
  as language mechanics, kept design decisions his.
- Commits still bundle ideas (`384a15d`: exceptions + logging + argparse in one). Taught `git add
  -p` *after* that commit; see whether week 2's commits change.

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
- **Textbook entries are numbered in learning order**, not syllabus order — renumbering on
  out-of-order arrival would break links. Written by me, committed as Claude, whenever a real
  lesson is given (standing instruction, now in CLAUDE.md).
- Filenames stay boring: no spaces, no glob metacharacters. An earlier `*c` suffix convention
  was reverted — `*` is illegal on NTFS and would break checkout on the Windows side of the
  planned dual-boot.
