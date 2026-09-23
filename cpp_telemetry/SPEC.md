# Week 3 deliverable — telemetry in C++

Written 2026-09-23 by Claude, from the session that finished week 3's checklist. This is the
scope contract, not the design. The design is Chris's.

The README for this project is his to write when it works — what it does, how to run it, what he
learned, what broke. This file only says where the edges are.

---

## Why this exists

Week 3's six checklist items are all covered, but every line of C++ so far lives in a scratch
`cpp_test/` directory whose entire job is printing `welcome` and `goodbye`. Nothing has been
written that has a reason to exist, and nothing consolidates until something does.

The domain is deliberately one he already knows cold. Porting a problem he solved in Python in
week 2 means all the difficulty lands on the language rather than the problem. That's the point —
this is a C++ exercise wearing a telemetry costume.

**Expect it to take several evenings.** The Python version was one. That ratio is the lesson, not
a failure signal.

---

## In scope

- Read a CSV of the shape in [`../telemetry/data/sample_telemetry.csv`](../telemetry/data/sample_telemetry.csv):
  `timestamp,robot_id,velocity,battery,temperature`
- Parse rows into `Reading` objects
- Skip malformed rows and count them
- Per-robot min / max / mean temperature
- Print a human-readable summary to stdout
- CMake build
- Compiles clean under `-Wall -Wextra`

## Out of scope — explicitly

These are all things the Python version does, or that the boss fight raised. None of them are
this week's skill, and week 2 ran ~2.5x budget by growing exactly this way.

- JSON output
- The error taxonomy / exception hierarchy
- CLI flags or configurable thresholds
- Tests — week 5 is testing; retrofit then
- Anything from the `boss-fights/01-telemetry/NOTES.md` findings list
- Anything from the `telemetry/` README's "What's next"

If something feels like it wants to be added, write it down instead of building it.

---

## The three design questions

To be answered — out loud, as rubber-ducking — **before** any code is written. They are the
generative part, and per the working hypothesis in
[`../docs/ta-notes/estimates.md`](../docs/ta-notes/estimates.md) the generative hours are the
valuable ones.

1. **What owns the collection of readings?** How do per-robot stats accumulate, and what happens to
   a `Reading` after it has been parsed?

2. **Which functions take `const Reading&`, which take `Reading&`, and which take values?**
   Justify each one individually. This is 2026-09-23's material applied directly, and it's the
   checkable part.

3. **Where do malformed rows go?** With exceptions out of scope, what is the signature of the parse
   function? This one is genuinely hard in C++ and has no obviously correct answer — the first
   instinct is what's wanted, not the right answer. It's also the question C++ answers very
   differently from Python, where raising was free.

---

## Definition of done

- `cmake --build` produces a binary from a clean tree
- Running it on the sample CSV prints a summary whose numbers match the Python version's
- `-Wall -Wextra` is silent
- A README exists, written by him, including what broke
- The three design questions have answers he can defend, not just code that runs
