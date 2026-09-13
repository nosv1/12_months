# TA notes

Working notes kept by Claude, in the repo so any session on any machine can pick up where the
last one stopped. Not a diary and not a progress log — those are
[00-dashboard.md](00-dashboard.md) and [background-threads.md](background-threads.md).

Read this at the start of a session. Update it at the end, and commit it.

---

## Where things stand

**Last updated:** 2026-09-12 18:30 (Saturday evening session, 17:15–18:30). He plans to start
week-2 work Sunday Sep 13.

- Curriculum started **Wed 2026-09-09**. **Week files track syllabus progress, not the calendar**
  (see Decisions): week 2 work began Sun Sep 13 and is logged in `week-02.md`. Nominal calendar
  target for week 3 (C++) is still **Mon Sep 21**. He is not behind. **9.25 h logged.**
- **Week 1 done and verified.** mypy clean, CLI runs end to end, all 8 planted defects reach the
  report (truncated row → `unknown` robot, `f97c3f9`).
- **Tests: 1 passing.** He renamed `test.py` → `test_*` himself after "no tests ran."
- **C++ toolchain installed and verified** via `scripts/install-cpp-toolchain.sh` (mine). He wrote
  `cpp_test/hello.cpp` and answered the three questions: `-o`/`a.out` right; `#include` ≈ import
  (half right, taught preprocessor copy-paste → textbook 06); namespaces "no idea" (taught).
- He called `#include` "kinda wild". Curiosity, worth feeding in week 3 (`g++ -E`, link stage).
- Evening: he pushed back that AI writes tests faster. Answered: AI types them; deciding what
  counts as wrong (the `0.0` bug) is the skill. Watch whether he engages with `parametrize` cases
  himself in week 2 or wants to hand them off.

## Evening 2026-09-12 — critique round closed

README re-read and fixed by him: timestamp rule correct, falsy-`0.0` rationale written, `unknown`
robot documented. `cli.py:61` now logs the error text (`ba2f159`). Mangled fields renamed,
matplotlib import moved into `plot()`.

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

### Still open from day 4 (minor)

- `cli.py` `main()`: `Path(args.x)` may still wrap a value `type=Path` already converted. Unchecked.
- `robot.plot()` still commented out of `cli.py`; every robot would overwrite the same `plot.png`.
  WIP; don't review until he picks it up.
- Exceptions short-circuit, so `bad_readings` holds the *first* reason per row. Never asked him to
  defend it. Good week-2 test-design question.
- `Warning` still shadows the builtin. Dropped, his call.

### Next session (Sun Sep 13 — week 2 start)

1. **Log hours:** run `date` at the opener.
2. **Tests beyond the one:** `pytest.raises` for validator errors, `parametrize` over the planted
   defects. He names the failure cases; `main(argv)` taking a list makes the CLI testable.
3. CI (GitHub Actions) is week-2 new material too. The workflow YAML is tooling, but what it runs
   (pytest, mypy) is his call.
4. Boss Fight #1: spill allowed, his target Sun Sep 20. Hands-off once it starts.

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

**I log his hours (standing, 2026-09-12).** On a session opener ("we're back" etc.) run `date` and
note the start; on sign-off run `date`, append `YYYYMMDD HHMM - HHMM (N hours -- note)` under
**Hours** in `docs/background-threads/week-NN.md`, bump **Hours logged** in `00-dashboard.md`,
commit as Claude. If he leaves without signing off, ask for the end time next session. Don't guess.

**Reformat any markdown freely (standing, 2026-09-12)**, including his READMEs. Formatting and
wrapping only; keep his wording and meaning.

**`scratchpad.md` is background, not a prompt.** Read it at session start for context on what he's
thinking. Don't raise its entries in chat unprompted; let them shape how I teach instead. (Stated
2026-09-12.)

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

- **Boss Fight #1 may spill into week 3** (decided 2026-09-12). His goal: done by Sun Sep 20 night.
  Log in the dashboard slippage table only if it actually spills.
- **Toolchain prereq not added to the syllabus**. It's already installed and verified, so moot.
- **Week files follow syllabus progress; hours lines are dated by calendar day** (decided
  2026-09-12). Week 1 is finished in his head, so Sun Sep 13 work goes in `week-02.md` under
  `20260913`. Slippage is still judged against the nominal calendar (week 3 ≈ Mon Sep 21).
- **He writes his own time estimates** in the week file before starting; actuals go beside them.
  Estimates must name a checkable end state, not a topic. Compare on Sundays.

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
