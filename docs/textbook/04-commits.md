# Commits: what goes in one, and how to split them

**Week 1** · checklist item: Git — branches, meaningful commits, `.gitignore` · [syllabus](../../SYLLABUS.MD#L111)

Came up when a day's work left nine modified files — a refactor, three independent week-1 items,
docs, and an unfinished feature — and "one commit per change" seemed impossible because the
changes touched each other.

---

## The unit of a commit

**One complete idea that leaves the repo working.**

Not one file, not one line, not one change. If three files only make sense edited together, that
is *one* commit, and that's correct — not a compromise.

So the real question is never "how do I split entangled changes" but "what are my actual ideas
here, and which edits does each one need?"

## Entangled vs. merely simultaneous

Most of what feels entangled is only *co-located in time*. The test, for any two changes:

> **If I committed A without B, would the repo still work?**

- **Yes** → independent. Separate commits, *even if they're in the same file*.
- **No** → they belong together.

The nine files, sorted by that test:

| Change | Files | Verdict |
| --- | --- | --- |
| `Validator` class → functions that raise | `validator.py`, `main.py`, `robot.py` | **Inseparable.** Commit `validator.py` alone and `main.py` fails at import. |
| `logging` | `main.py` | Independent |
| `pathlib` | `main.py` | Independent — different lines of the same file |
| `argparse` | `main.py` | Independent |
| Syllabus ticks, build log, scratchpad | docs | Independent of all code |
| `robot.plot()` + matplotlib | `robot.py`, `pyproject.toml` | Unrelated feature, **and unfinished** |

**Sharing a file does not make changes one commit.**

## `git add -p`: staging by hunk

Staging is per-*hunk*, not per-file:

```sh
git add -p src/telemetry/main.py
```

Walks each hunk: `y` stage, `n` skip, `s` split smaller, `e` edit by hand, `q` quit, `?` help.
Stage only the `logging` hunks → commit → stage only the `pathlib` hunks → commit. Two commits,
one file.

Staying oriented:

```sh
git diff --cached     # what I'm about to commit
git diff              # what I'm leaving for later
```

### Verify the commit, not the working tree

A staged subset has never been run. To check it stands alone:

```sh
git stash --keep-index     # tree now contains only what's staged
uv run mypy src/ && uv run pytest
git stash pop
```

## The rule that decides where you may split

**Every commit should leave the repo working.**

If a split produces a broken intermediate, don't split there — keep them together and let the body
explain both strands. One commit doing two things with an honest message beats two commits where
the first doesn't run. This matters later: `git bisect` assumes every commit is testable.

Corollary: **don't commit a half-finished feature to get it out of the way.** Stash it
(`git stash push -m "wip plot" -- src/telemetry/robot.py`) or leave it unstaged.

## The message

**Subject:** imperative mood, one idea, ~50 characters. It completes the sentence *"If applied,
this commit will…"*. If it needs "and", you are probably looking at two commits.

**Body** (blank line after the subject): *why*, then *where* if there are several strands.

```
Replace validator status objects with exceptions

The (Validator, value) tuple encoded "if valid then value is not None"
across two independent slots, which no annotation can express — so five
call sites narrowed Optionals by hand, and `if not valid_float` dropped
every 0.0 velocity as invalid.

Validation and conversion are one operation, so validators now return the
converted value and raise on failure:

- validator.py: Validator class becomes module-level functions
- main.py: one try/except error boundary around the per-row work
- robot.py: bad_readings now (line, message), one reason per row

Fixes amr-01's average velocity, which excluded ~12s of parked readings.
```

Subject says *what*. Body says *why*. Bullets say *where*.

The diff already records *what changed line by line* — a message that restates it ("changed x
to y in validator.py") adds nothing. The *why* is the only part the code cannot tell a reader, and
it's the part you'll want in six months. You've usually already worked it out; writing it down
costs a minute.

## Checklist

- [ ] Can I describe this commit in one imperative line without "and"?
- [ ] Does the repo build / type-check / test with *only* these changes?
- [ ] Is anything unfinished staged?
- [ ] Does the body say *why*?

---

## Carry-forward

Week 2's CI runs on every push, which makes "every commit works" mechanically checked rather than
aspirational. And the commit history is the evidence for the career gap — a reviewer reads it.
