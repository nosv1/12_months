# Writing tests: what a test claims, and why counting isn't one

**Week 2** · deliverable requirement: "every way a row can be bad has a failing-if-broken test" ·
[syllabus](../../SYLLABUS.MD)

The suite at the start of this session was one assertion:

```python
assert num_bad_readings == 8
```

It was failing, correctly, because the sample file had grown a ninth defect. But it would also
have passed while the analyzer blamed entirely the wrong rows — which is exactly what it was
doing. Two and a half hours later the same test said:

```
Extra items in the left set:   (235, 'TimestampOutOfOrderError')
Extra items in the right set:  (238, 'TimestampOutOfOrderError')
```

Same bug. Same data. The difference is entirely in what the test *claimed*.

---

## The one-sentence version

**A test is a claim about a promise, not a recording of what the code does. If the expected value
came from the implementation, the test can only tell you the implementation hasn't changed.**

---

## The change-detector trap

The tempting way to write a test is to read the function, run it, see what comes out, and assert
that. What this produces is a **change detector**. It goes green when the code is wrong, because
it was derived from the code. It goes red when the code is *corrected*.

A concrete instance from this project: the velocity bound was implemented as `abs(value) >= 2`
and later corrected to inclusive, `abs(value) <= 2`, after the customer specified `[-2.0, 2.0]`.
A test written from the old implementation would have gone red on the fix and green on the bug.

So the expected value has to come from **outside** the implementation. In this project the
outside is the README ranges, the hand-authored sample file, and the customer spec.

### The tautology, which is the same trap wearing a disguise

This is easy to violate without noticing. From the first pass at the accepts tests:

```python
def test_timestamp_format_accepts(value):
    assert validate_timestamp_format(value) == datetime.fromisoformat(value)
```

`validate_timestamp_format` *is* `datetime.fromisoformat` wrapped in a `try`. The assertion
reduces to `fromisoformat(x) == fromisoformat(x)`. It cannot fail — not for a timezone bug, not
for a microsecond-truncation bug, not if the function is deleted and replaced with the stdlib
call.

The fix is a hand-written literal:

```python
datetime(2026, 9, 3, 14, 0, 0, 16000, tzinfo=timezone.utc)
```

Now the test asserts something about `Z` handling and microsecond parsing. The same applies, more
mildly, to `assert validate_velocity(value) == float(value)` — `validate_velocity` calls
`float()` internally.

**Rule of thumb:** if the right-hand side of the assertion calls anything the left-hand side
calls, look harder.

---

## Where test cases come from

Not "what could fail?" — that's unbounded, and the boring cases get missed. The generating
question is **"what did I promise, clause by clause?"**

Read the promise, not the code. `validate_velocity` promises: returns a float if `|v| <= 2`;
raises `VelocityNotANumberError` if it isn't a number; `VelocityWasNaNError` if it's NaN;
`VelocityOutOfRangeError` otherwise. Four clauses, so at least four tests. That is a checklist,
not a brainstorm.

Then three generators run over the checklist:

**Boundaries.** Every range has four interesting inputs, not one: just below, exactly at, exactly
at the far end, just above. `2.0` and `-2.0` must pass; `2.001` must raise. That single pair is
the entire content of the inclusive-bound bug.

**Shapes that aren't values.** Empty string. Whitespace. A word. `"nan"`, `"inf"`, `"-inf"`.
`float("inf")` in particular sails past a `math.isnan` check — deciding whether `inf` is
"out of range" or "not a number" is a *spec* call, and writing the test is what forces it to be
made deliberately rather than by accident.

**The happy path.** Easy to skip because it feels trivial. It is the thing that silently regresses
during refactors.

---

## Levels: unit contracts vs collector contracts

Asked to name the promises of `validate_parsed_line_values`, the first answer was a list of
per-field checks — timestamp format, velocity is a float, battery in range, and so on. Those are
real, but they are the contract of `validate_velocity` and its siblings. They belong in a
parametrized table against those functions directly.

`validate_parsed_line_values` is a **collector**, and its promises are structural:

- Every input line comes out in exactly one of the two lists. Not zero. Not both.
- `len(readings) + len(bad_readings) == len(parsed_lines)`.
- It never raises — converting exceptions into data is its entire reason to exist.
- A good row survives with its values intact.
- A bad row carries the right line number and the original text.

This distinction has teeth. The `del parsed_lines[i]` bug (see
[10](10-exception-taxonomies.md)) left rows in `bad_readings` *and* in the set feeding
`average_velocity`. Every per-field check passes with that bug in place. Only the partition
invariant catches it.

**Symptom to watch for:** a promise landing in the wrong list — "timestamp order" appearing in the
contract of a function that never checks it — usually means the stage boundaries aren't crisp yet.

---

## Identity over count

`assert 9 == 8` says a number moved. A set of `(line_number, error_name)` pairs says *which* row
and *which* error, and pytest prints the symmetric difference for free.

The identity form also catches a class of bug that counts structurally cannot. With both the
wrong-row-blamed bug and the guarded `del` in place, the totals balanced perfectly — 353 accepted
plus 8 rejected equals 361 rows in — while the innocent row (235) was discarded and the actually
out-of-order row (238) was kept and fed into the statistics. A count assertion is green for that.
A set assertion names both halves.

Two supporting rules:

- **Both directions.** Iterating over what was found and looking each one up in a table of
  expected values only asks *is everything I found expected?* It never asks *did I find
  everything?* Delete a check from the analyzer and such a test happily iterates over one fewer
  item. A set comparison asks both questions in one expression.
- **A `KeyError` is not an assertion failure.** The dict-lookup version died on the first
  surprise and reported nothing about the other eight. `assert found == expected` reports the
  whole difference.

---

## The question that finds missing tests

**If I broke this line on purpose, would something go red?**

Applied to the unreachable `del`: ruff green, mypy green, tests green. Nothing went red, because
every assertion in the suite was about the *rejected* side of the ledger and the bug lived on the
*accepted* side. The diagnosis isn't "add more cases" — it's "an invariant I care about is
unobserved."

---

## Test-first, minus the dogma

A recurring stall this session: wanting to write tests, being reminded a known bug exists, wanting
to fix the bug first, and looping.

The resolution is to **write the failing test first** — not as ceremony, but because:

1. It gets the bug out of your head and into an artifact. pytest remembers that 238 is the real
   offender so you don't have to.
2. It gives you a definition of done. Otherwise the fix is verified by reading log output and
   squinting; with the test, the fix is done when it goes green.

That is most of what "test-first" usefully means. Not a rule about writing tests before all code —
just: when you know something is broken, encode the brokenness before touching it.

---

## Mechanics: `parametrize`

One test function, many cases, each reported separately:

```python
@pytest.mark.parametrize("value, expected_error", [
    ("2.001", VelocityOutOfRangeError),
    ("ERR",   VelocityNotANumberError),
    ("nan",   VelocityWasNaNError),
])
def test_velocity_rejects(value, expected_error):
    with pytest.raises(expected_error):
        validate_velocity(value)
```

- First argument: a string naming the parameters, which become the function's arguments.
- Second: a list of tuples, one per case, positions matching the names.
- pytest runs the function once per tuple and reports each as its own test.

That last point is the reason to prefer it over several `assert`s in one function: the first
failure doesn't hide the remaining cases.

**Readable ids.** Auto-generated ids get unreadable fast, and `[2.0]` versus `[2.001]` is exactly
the pair you least want to squint at:

```python
pytest.param("2.0", id="at-upper-bound")
```

**Exception classes are ordinary objects** and go in the table like anything else.

**Keep accepts and rejects in separate functions.** They have different shapes — one expects a
return value, the other an exception — and merging them forces a `None` column and an `if` in the
test body. A branch inside a test means the test is deciding at runtime what it's testing.

**Stacked `parametrize` decorators multiply.** Two of them produce the cartesian product.
Occasionally intended; usually a surprise.

---

## Mechanics: fixtures

A function that produces something a test needs, requested by **name**:

```python
@pytest.fixture
def sample_lines():
    return read_file(Path(__file__).resolve().parent / "../data/sample_telemetry.csv")


def test_something(sample_lines):
    ...
```

pytest sees the parameter name, finds the matching fixture, calls it, passes the result in. It
reads as magic once; it's a name lookup.

- **Teardown** uses `yield` instead of `return` — everything after the yield runs when the test
  finishes, pass or fail. This is what a plain helper function can't do.
- **Scope** (`@pytest.fixture(scope="module")`) builds once per module instead of per test. A
  shared *mutable* fixture lets one test corrupt another; default per-test scope unless there's a
  reason.
- **`conftest.py`** in the tests directory publishes fixtures to every test file with no import.
  It is the one Python file you never import from — pytest finds it by filename.
- Built-ins worth knowing early: **`tmp_path`** (a fresh temp directory, so output-writing tests
  don't pollute the repo), **`capsys`** (captures stdout/stderr), **`caplog`** (captures log
  records).

**When to extract one:** not at "I have several tests" but at **"a second test needs the same
setup."** Written before that, you're guessing at the shape; written at that point, you're
extracting a duplicate you can see, and two call sites tell you what it should return.

One joint to be aware of when the time comes: a fixture returning the finished `Analysis` makes
every test one line, but bakes the warning thresholds in, so a test wanting different thresholds
can't use it. Returning the raw lines keeps that open and costs a line per test.

---

## Open questions carried forward

- No assertion yet on the **accepted** side — the 353 good rows. Highest-value missing test.
- `validate_timestamp_order` has no unit tests; it is covered only by the integration test, which
  is currently red for unrelated reasons — and it is the next function scheduled for a rewrite.
- The empty string `""` isn't in any reject table, despite being the actual defect on line 97 and
  the most common malformed value in real CSV data.
- Multi-error collection will change the expected shape from `line → error` to `line → {errors}`.
  Line 363 carries three faults deliberately; the current set-of-pairs table cannot express it.
- The sample file has no malformed-timestamp row, so end-to-end coverage of `TimestampFormatError`
  is absent. Fixture gap, not a code gap.
- `test_validations.py` now tests the parser too. The split into `test_parser.py` /
  `test_validator.py` / `test_pipeline.py` is cheapest before it grows further.

---

## Where this returns

Week 12 adds ROS 2 node testing, where the collector-contract idea reappears as "did every message
published get handled exactly once." The partition invariant is the same claim with a different
noun. The `tmp_path` habit matters from the first time a node writes a bag file.

Related: [09 — I/O at the edges](09-io-at-the-edges.md) is what makes any of this testable —
`analyze_telemetry` takes an iterable of strings and returns a value, so the whole pipeline can be
asserted on without touching a disk. [10 — Exception taxonomies](10-exception-taxonomies.md) is
what makes the assertions *stable*: `(302, "ColumnCountError")` survives a reworded message,
`"Data was missing from the input."` does not.
