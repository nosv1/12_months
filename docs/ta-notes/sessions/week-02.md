# Session log — week 2 (started Sat Sep 12, 2026)

Archive. Back to the [TA notes index](../../ta-notes.md). Append one section per session.

---

## Sat Sep 12, ~20:30–22:45 — parser redesign (2.25 h)

Opened by discussing his scratchpad (he asked to):

- **Asserts vs `(bool, value)`** — already settled day 4 (raise). Noted `python -O` strips asserts.
- **0–10 rating** — offered per-skill with repo evidence, re-run at boss fights. Not taken up.
- **Sessions feel unproductive without code** → agreed: each session produces a committed artifact;
  goals are checkable outcomes phrased as the problem; he writes estimates. He noticed his own
  "checklist as fast as possible" drift.

Week 2 walk-through: pdb item needs real use to tick; I/O-in-logic question left for him to find
by trying to test `parser` vs `report`; README "stranger test" (fresh clone, follow literally) —
I hold a gap list to compare after; CI after tests, not a tutorial knock-out.

Work, his:

1. Split the try/except test into two; found `pytest.raises` himself. Wrote `debug.sh`.
2. `parser(TextIO)` → `list[str]`, then I caught the silent header skip. Proposed per-line parsing
   himself → `ParsedLine` + validator taking `prev_reading` + loop function. Found `Iterable`
   after I gave the search term.
3. `BufferError` misuse → custom `MissingDataError`; `ParsedLine` → dataclass; moved to `parser.py`.
4. Circular import (validator ↔ parser). First fix: `validate()` method on `ParsedLine` — disliked
   it. Then found the loop was the cycle; moved it to `cli.py` "for now" (`3aff0b7`). → textbook 07.
5. Naming the loop's module: `preprocessing`, `processor` — both too broad. Parked; he was tired.

Verified at close: 2 tests pass, mypy clean, 8 defects caught. **I wrongly claimed input was
streamed** at sign-off — `readlines()` still in `main`; corrected before he left.

Estimate: tests 1h → 2h "and parser redesign" (his edit).

## Sun Sep 13, 12:17–15:30, break 14:01–14:38 — pipeline stages (2.5 h)

Work, his:

1. **Naming the loop** is still stuck. I gave three methods: write the call site, a one-sentence
   docstring with no "and", standard stage verbs. He proposed `reader.read_file(path)`. I pointed
   out it returns `dict[str, Robot]` (says less than it does) and that `reader.py` sits next to
   `reading.py`.
2. **He split the loop into stages himself** (parse → validate → group). I flagged that the
   per-robot timestamp check can't run before grouping; sample lines 3–4 interleave.
3. **Rebuilt the raw string** from a `Reading` for `bad_readings` → `'202Z,...'`. He had the right
   constraint (Reading shouldn't know about lines). I pointed at where the source is lost, not at a
   fix. He noted loop count; I said speed isn't the reason, streams (week 11) are.
4. **Asked the customer** what a rejected row needs. Answered in character (telemetry.md):
   line number, reason, exact original row, no invented robot, `-Infinity` breaks JSON.
5. Built `BadReading`, `ParsedLine.original_line`/`line_number`, grouping on `ParsedLine`s,
   `main(path, out)` as only function calls, `cli()` split out. Set comprehension with `(k: v)`
   syntax → explained the bracket table.
6. **He spotted the double timestamp-format parse himself.** I explained it's a dependency-order
   symptom and gave a hint only (pass vs same iteration). Also flagged: truncated row dropped
   (unused return value; he fixed), last-row off-by-one (he fixed), bad row as "previous" (open),
   malformed timestamp reported 3× (open).

Committed `b830018` (his). Verified at close: 8 defects, console script, mypy, 3 tests. One test
(`test_all_defects_caught`) has no assertion. → textbook 08.

Me: wrote CLI output to `~/claude-scratch-out` (outside repo) by mistake mid-session; deleted, told
him. Use the scratchpad dir.

---

## 2026-09-14 (Mon) 1637–1829, 1.75 h

Opened asking whether to finish Sunday's work or switch gears. Said finish, pointed at
`test_all_defects_caught` asserting nothing.

1. **"Annoying writing and rewriting tests while stuff is moving."** Answered with his own
   evidence: two of three tests had survived three redesigns with zero rewrites, the third
   couldn't be finished. Churn tracks how much structure a test reaches through. The requirement
   ("8 defects in the sample file") is the stable thing.
2. **"Why would main ever return anything tho, that feels wrong."** He was right and I'd framed it
   badly. Reframed: `main` should return `None` *and* compute nothing — the problem was four jobs,
   not the return type. Functional core / imperative shell. He did the whole split himself,
   including inventing the `Analysis` wrapper type.
3. **First attempt extracted the stages but not the composition** — the test ended up with a
   character-for-character copy of `main`'s body. Pointed at it as the churn he'd complained about
   an hour earlier, rebuilt by hand. He then extracted `analyze_telemetry`.
4. **Naming.** He'd gone to the textbook looking for a name for the composition, found 08's stage
   verbs, and it didn't answer him. Rule given: a stage is named for what it does, a composition
   for what it returns — and the name wouldn't come because the return type wasn't decided. He
   named the type, then the function named itself. His words: "as soon as i figured out what that
   pipeline returned i could name it." → textbook 09, and 08 now cross-links to it.
5. **Code review, two rounds.** Round 1 caught: `print` left inside the pure `build_report`; a
   `__main__` block that crashed on a wrong relative path *and* littered `src/output/` (I deleted
   that; my run created it); the return still a loose 2-tuple; `run_pipeline` as a name. He fixed
   all of it. Round 2 findings are in ta-notes *Next session* — the big one is that
   `analyze_telemetry` now lives in `analysis.py`, so a stage imports its siblings.
6. **Explained `conftest.py`** end to end (auto-import, fixtures, scoping/stacking, hooks,
   rootdir/`sys.path` caveat, gotchas). Not built yet.
7. **`assert == 8`.** He said it felt wrong and he "got lazy." Reframed: not lazy, but it tells
   you nothing on failure. His proposed fix — enumerate the validations and compare — walks into a
   self-fulfilling test; expectation has to come from the data file, not the code. Gave: set of
   line numbers (pytest prints the symmetric difference), plus `parametrize` per defect kind.
   He came back with distinct exception types per failure, unprompted, which is the piece that
   makes `(line_number, kind)` assertable.

Asked at close whether he's behind. He isn't on hours; the boss fight is the exposure.

Mine: wrote textbook 09, retrofitted pronouns out of 07/08/09 at his request, added it to the
entry conventions. His code is uncommitted — left it alone.

## 2026-09-15 (Tue) 1706–1901, 1.9 h

All on the exception taxonomy — his idea from the night before. Wrote all of it himself.

1. **Chose distinct exception classes in a new `exceptions.py`.** Confirmed no stdlib collision
   (`exceptions` was a Python 2 module, gone in 3; absolute imports make it moot anyway).
2. **`BadReading` now holds the exception object** rather than `str(err)`. Flagged the two
   consequences: `json.dump` can't serialize it, and exception objects retain `__traceback__` →
   frames → locals. He landed on emitting both a class name and a message — which is also what
   the customer asked for, arrived at independently from both ends.
3. **Chose `Exception` over `ValueError` as the parent.** Warned that `except ValueError` would
   stop catching and the CLI would crash loudly — good failure, let him hit it.
4. **Naming.** His draft was `ERRAsFloatError`. Rule given: names the input and the mechanism;
   test is "could this name survive a rewrite of the code that raises it?" Stdlib convention is
   subject + what's wrong with it.
5. **First attempt was a `KNOWN_EXCEPTIONS` set + `except Exception`**, which ruff hit with
   BLE001. Three findings, all verified by running it: the membership test was instance-vs-class
   so it was `False` 100% of the time and everything became `UnknownError`; mypy had already said
   so ten times via `set[Exception]` vs `type[...]`; and the blind except was hiding a `TypeError`
   from `NaNError(float_str)` that meant **NaN detection was entirely dead**. Answer given: a base
   class, not a registry. He implemented `TelemetryException` and deleted the set.
6. **Result verified at close:** ruff clean, mypy clean on 15 files, all 9 defects caught with
   correct kinds and readable messages. Big step up from `== 8`.
7. **Two bugs left in `validate_robot_timestamps`**, both found by running it, both in the rewrite
   he'd already said was coming: attribution moved to `prev_parsed_line` so it blames the innocent
   earlier row (235/261 instead of 238/262); and `del parsed_lines[i]` is now **unreachable**
   because its `except ValueError` is dead — flagged rows stay in the valid set and feed
   `average_velocity`. Report contradicts itself; ruff, mypy and the test all stayed green.
8. **Fail-fast vs fault-tolerant**, asked as the customer. He reasoned it out himself — crashing
   means the customer waits for a release, quarantining means they keep working. Correct call;
   gave him the vocabulary (dead letter queue) and the caveat that it's one boundary with loud
   logging, not a return to scattered blind excepts.

**Customer answers given (new spec, not previously stated):** velocity `[-2.0, 2.0]`, temperature
`[-40, 150]`, battery `[0, 100]`, **all inclusive**; sub-zero temperatures are valid (cold-storage
aisles at −20 °C). Errors per row are a **list**, always. Report carries both a stable error name
and a plain-words message. `UnrecognizedError` bucket with a count that should always be zero.

**Mine:** appended line 363 to `sample_telemetry.csv` — `2026-09-03T14:02:00.018Z,amr-01,4.812,
118.4,-41.0`, three faults in one row, appended so nothing renumbers. He asked for it. Wrote
textbook 10. His code is uncommitted — left it alone.

Closed saying he's not burnt out and looks forward to the evenings, but can't do more than ~2 h of
"constant thought" at a stretch.

---

## 2026-09-16, 1614–1840 (2.4 h) — the test suite got built

Opened with "WEDNESDAY CLAUDE WOO" on an off day. Went from one assertion to 29 tests.

1. **He asked for the testing mindset outright** — "think of something that could fail and see if
   it does? also check expected values are as they should be?" Both half right. Answer given: a
   test is a claim about a promise, not a recording of behavior; expected values must come from
   outside the implementation; cases come from the spec clause by clause, then boundaries, then
   non-value shapes, then the happy path. Written up as [textbook 11](../../textbook/11-writing-tests.md).
2. **Asked him to name the promises of `validate_parsed_line_values`.** He returned the eleven
   per-field checks — right list, wrong function. Used that to separate unit contracts from
   collector contracts (partition, never-raises, values intact). The partition invariant is the
   one that catches the `del` bug; none of his eleven do. He also filed "timestamp order" under a
   function that doesn't check it — flagged as a sign the stage boundaries still aren't crisp.
3. **He fixed the `del` bug himself** before I raised it, with a guard comparing
   `bad_readings[-1].line_number` to the current row. Verified by running the partition: 361 in,
   353 good, 8 bad, no overlap. Told him *how* it's true — the guard fires a lap late because the
   order handler attributes to `prev`, and the backwards walk makes the off-by-one cancel. It
   works but is load-bearing coupling to the attribution bug.
4. **Named the loop he was stuck in** — wants to write tests, keeps getting reminded the order
   function is wrong, wants to fix that first. Answer: write the failing test, let it stay red.
   Two arguments: it gets the bug out of his head into an artifact, and it gives him a definition
   of done other than reading log output and squinting. He took it.
5. **He proposed a dict of known errors keyed by `(error_name, line)`** and hand-rolled `__eq__`
   and `__hash__` on `BadReading` to support it. Four problems given: the loop only asserts one
   direction; `__hash__` returned a tuple (mypy had said so); `__eq__` compared an exception name
   to `"BadReading"` so it was always False; and test pressure was leaking into a domain class.
   Offered `@dataclass` vs a projection to `(int, str)` tuples as the two roads. **He took the
   projection** and the test now reads as a set comparison with a symmetric-difference diff.
6. **"The output shows memory locations"** — `__repr__`, explained. Used it to reinforce the
   projection choice: tuples print themselves.
7. **ruff rule sets.** He didn't know `B` or `C4`. Explained prefixes, `--select` to trial,
   `ruff rule <code>` to learn one, `[tool.ruff.lint] select` to persist, `# noqa: CODE`.
   **Finding: there is no ruff config in the repo at all** — `uv run ruff check .` says "All
   checks passed" while his editor extension was firing BLE001 and T100. Editor and terminal
   disagree; CI would agree with neither. Told him to fix it before CI exists. Not done yet.
8. **He turned on `B`, acted on B904, and got `from` backwards** — `raise ve from NotANumberError(...)`
   in all five sites. Two tests went red instantly. Gave the rule (`raise NEW from OLD`), the
   out-loud check, and the note that `from` never changes which exception propagates. Registered
   with him that the tests had just earned their keep on a five-site mechanical change.
   [Textbook 12](../../textbook/12-exception-chaining-and-lint-rulesets.md).
9. **My `set({...})` remark misfired** — said the `set()` wrapper was redundant, he deleted the
   braces instead and got `TypeError: set expected at most 1 argument, got 8`. My wording, not his
   error. Worth being literal about which half to delete next time.
10. **Taught `parametrize` and fixtures.** Parametrize: argnames string, tuple list, one reported
    test per case, `pytest.param(..., id=...)` for boundary readability, exception classes in the
    table, accepts and rejects as separate functions, stacking multiplies. Fixtures: explained,
    then told him **not to write one yet** — the trigger is a second test needing the same setup,
    not test count. Named `tmp_path`, `capsys`, `caplog`, `conftest.py`.
11. **Customer answer: `ColumnCountError`.** He decided to bucket wrong-column-count rows into one
    error and asked the customer to name it. Gave the name, the message shape ("Expected 5 columns,
    found 4." — counts, because it goes in a firmware ticket), and two facts: a header is always
    present and a missing one should fail loudly; and **a vendor firmware update once appended a
    column and rejected 40,000 rows**, which justifies checking against the header rather than a
    constant. He then moved `NUM_COLUMNS` out of `ParsedLine` and derived it in `parse_lines`.
    Told him what the change actually bought: appended columns now work, **inserted** columns now
    silently corrupt instead of loudly failing. His call, made knowingly.

**Review findings given on his code, all his to act on:** `lines[0]` on an `Iterable[str]` (mypy
flagged), read before the `headers_count` check so `headers_count=0` would take column count from
a data row, `IndexError` on an empty file, stale `"was missing data"` log string after the rename,
`test_incorrect_column_counts` missing `-> None`, and **two tautological accepts tests** —
`validate_timestamp_format(v) == datetime.fromisoformat(v)` cannot fail.

**He decided `inf` is `OutOfRange`, not `NotANumber`** without remarking on it. Pointed out that's
a spec call and his tests now lock it in.

Ended at "askl;dfjas; im past my time limit" — one-word-reply territory, parked the accepts-side
assertion for tomorrow. Suite closed at **1 failed, 28 passed**, the failure being the deliberate
235/238 red.
