# Debugging with `pdb`: stop the world and look

**Week 2** · syllabus checklist item *"Debugging with `pdb` / debugger — not print statements"* ·
[syllabus](../../SYLLABUS.MD)

No bug prompted this one, and that's worth recording. The item came up for ticking on 2026-09-21
and nothing in the notes showed it had ever been used. The working knowledge turned out to be
`breakpoint()`, then `n` to step, then typing variable names at the prompt. That's the core, and it's
also where most people stop. This entry covers the three things beyond it that make a debugger worth
reaching for before `print`.

---

## The one-sentence version

**`print` makes you decide in advance what you'll want to know; a debugger lets you stop the
program and ask whatever you like, in any frame on the stack, after you've seen what went wrong.**

Every `print` is a guess about where the bug is and which variable matters. A wrong guess costs
an edit and a rerun. At a breakpoint you can inspect every live variable, call functions, and walk
up to the caller, all at the same stop.

---

## Getting in

| How | When |
| --- | --- |
| `breakpoint()` in the source | You know roughly where to stop |
| `uv run pytest --pdb` | A test fails, and you want to stop **at the failure** with nothing to edit |
| `uv run python -m pdb -m telemetry.cli data/sample_telemetry.csv out` | The script crashes; pdb stops at the start, `c` runs it, and a crash drops into post-mortem |
| `uv run pytest --trace` | Stop at the *start* of each test |

`--pdb` is the most useful of these. It's **post-mortem** debugging: the program has already failed,
the stack is still intact, and you inspect it. You didn't have to predict where to stop.

---

## The commands

| Command | Does | Note |
| --- | --- | --- |
| `n` | next line, **stepping over** calls | the one already known |
| `s` | next line, **stepping into** a call | use when the bug is inside the function being called |
| `r` | run until the current function returns | the way out after an `s` into something boring |
| `c` | continue to the next breakpoint | |
| `w` | where: print the call stack | you are at the arrow |
| `u` / `d` | move **up** to the caller / back **down** | variables now resolve in that frame |
| `p x`, `pp x` | print / pretty-print an expression | `pp` for dicts and lists |
| `l`, `ll` | list code around here / the whole function | |
| `b file.py:60, cond` | breakpoint, optionally conditional | see below |
| `interact` | a full Python REPL in the current frame | for multi-line exploration |
| `q` | quit | |

### `n` vs `s`

`n` on `parsed_lines.append(parse_line(line, line_number, len(header_parts)))` runs `parse_line`
to completion and stops on the next line. If the bug is *inside* `parse_line`, `n` walked straight
past it. `s` goes in. Then `r` gets you back out.

### `w`, `u`, `d` are what `print` can't do

Stopped inside a validator, holding a bad value, the question is usually *who passed this in?*
`w` shows the stack; `u` moves one frame up, and now `p line` shows the **caller's** `line`. No
edit, no rerun. With `print` you'd have to guess the caller, add a print there, and run it again.

### Conditional breakpoints

Row 302 is the one with four columns. A `breakpoint()` in the parse loop stops 361 times.
Instead:

```text
(Pdb) b src/telemetry/parser.py:60, line_number == 302
(Pdb) c
```

It stops once, on the row you care about.

---

## Gotchas

- **A variable named like a command.** Typing `n` at the prompt *steps*; it doesn't print your
  variable `n`. Same for `c`, `l`, `s`, `r`, `p`. Use `p n`, or `!n` to force Python.
- **`breakpoint()` left in the code.** Locally it looks like a hang. In CI there's no terminal, so
  pdb reads end-of-file from stdin and the run errors out. Ruff's `T10` rule
  ([textbook 12](12-exception-chaining-and-lint-rulesets.md)) catches it before commit.
  `PYTHONBREAKPOINT=0` disables every `breakpoint()` process-wide, which is useful to know but
  doesn't fix the leftover call.
- **pytest captures output**, but it knows about `breakpoint()` and suspends capture when one is
  hit. No `-s` needed.

---

## The VS Code debugger is the same thing with buttons

| VS Code | pdb |
| --- | --- |
| click in the gutter | `breakpoint()` / `b` |
| right-click breakpoint → condition | `b file:line, cond` |
| Step Over / Into / Out | `n` / `s` / `r` |
| Continue | `c` |
| Call Stack panel | `w`, `u`, `d` |
| Variables panel, Debug Console | `p`, `interact` |

The GUI is nicer for browsing big structures. pdb works anywhere there's a terminal, including a
robot over SSH. If you know pdb, the GUI takes minutes to learn; knowing the GUI doesn't teach you pdb.

---

## Open questions

- **When is `print` still right?** Probably for timing- and concurrency-dependent bugs, where
  stopping the world changes the behaviour, and for anything running unattended. That's what
  `logging` is for. A debugger answers "what is the state *now*"; a log answers "what happened
  over time". Part 2's threading work will test this.

---

## Where this returns

**Week 3 onward, as `gdb`.** Nearly the same vocabulary: `next`, `step`, `continue`, `bt` for `w`,
`up`/`down`, `print`, `break file.cpp:60 if i == 302`. Post-mortem there means a **core dump**:
the C++ equivalent of `--pdb`, and the tool for segfaults, where a `print` often never runs
because the crash happens first.

Related: [11](11-writing-tests.md) for what a failing test is claiming before you debug it, and
[13](13-fixture-resolution-and-reading-errors.md) for reading the error from the top before
stepping through anything.
