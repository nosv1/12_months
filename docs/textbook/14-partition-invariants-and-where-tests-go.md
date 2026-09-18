# 14 — Partition invariants, and where tests actually go

**Week 2.** Satisfies *"every way a row can be bad has a failing-if-broken test"* — and corrects the
reading of that item, which turned out to be half a spec.

**Came from:** a suite of 29 green tests, none of which asserted anything about the 353 rows that
passed validation. The first test written on that side immediately found four valid data rows being
silently discarded before validation ever saw them.

---

## Part 1 — The accepts side

### The asymmetry

A validating pipeline does two things: it rejects bad input, and it *keeps good input*. Both are
claims. Only one of them is tempting to test.

The rejects side is tempting because it has a visible, enumerable answer. Nine planted defects, nine
line numbers, a set comparison, done. The accepts side has 353 rows and no interesting story, so it
reads as "the part where nothing happens."

But "nothing happens" is itself a claim, and it's the claim that a dropped row violates. A test suite
that only checks rejects cannot distinguish *rejected* from *vanished* — both look like "not in the
output," and only one of them is correct.

### Counting is not the claim

The first instinct is to compare lengths: `len(readings) + len(bad_readings) == len(lines)`. This
fails for two independent reasons, and both are worth holding onto.

**Reason one: the units don't match.** One row can be wrong in several ways at once — line 363 of the
sample carries three faults in one row. So the sample has **9 bad rows but 11 errors**. If the count
is built out of errors, it counts the wrong thing; if it's built out of rows, it has to already know
that rows and errors differ, which is the thing under test.

**Reason two, the fatal one: counts cancel.** A length equation is one number compared to one number,
and two opposite mistakes sum to zero. Drop a good row and double-count a bad one, and the total
still balances. That is precisely the failure mode [11 — Writing tests](11-writing-tests.md) recorded
for the rejects side, where the count matched while the wrong rows were blamed. It reappears here
unchanged.

A count is an aggregate. Aggregates lose identity, and identity is the whole question.

### The invariant

Every input data row ends up in **exactly one** of two places. That's a partition, and it's two
properties:

1. **Nothing vanishes.** Every data row is in the good set or the bad set.
2. **Nothing is duplicated.** No row is in both.

Neither property requires enumerating 353 expected line numbers — the objection that kills the naive
version of this test. The good side is never written down. It's `everything the file had, minus what
was rejected`, and the rejected side is already pinned to hand-written literals.

Property 1 catches a silently dropped row. Property 2 catches a row that was both kept and blamed.
The length equation catches neither reliably, because it's their sum.

**Don't derive the expected set from the output under test.** If both sides of the assertion come out
of the same call, the assertion passes regardless of what the code does. The file is the independent
source of truth for "what rows existed"; the hand-written defect set is the anchor for "which ones
were bad."

### What identity means, and where it goes

To say "no row is in both places" you need a row to be *identifiable*. That surfaced a design
question that the types had already half-answered:

```python
class Reading:                  class BadReading:
    robot_id                        line_number
    timestamp                       unparsed_string
    velocity                        exception
    battery
    temperature
```

`BadReading` carries a line number. `Reading` did not — and that was correct, not an oversight. A
`Reading` is a fact about a robot. A line number is a fact about a *file*. Provenance belongs to
whatever ingested the data, and the domain object had deliberately been kept clean of it.

Which means the partition, as first stated, didn't typecheck: the good side had no identity to
compare.

Three doors:

| Option | Cost |
| --- | --- |
| Put `line_number` on `Reading` | Cheap now. Couples the domain object to file provenance. |
| Assert the partition at the `parse_lines` boundary, where both sides are `ParsedLine`/`BadReading` and both carry numbers | No type change. Tests one stage, not the pipeline. |
| Give readings a neutral source identity, not a line number | Most work now, least later. |

**Taken:** `line_number` on `Reading`, revisit in week 11. One construction site, and the toy problem
is getting rebuilt from scratch shortly anyway.

The tradeoff to have gone in knowing: what replaces this later is not a validity marker — validity is
already expressed by `Reading`-vs-`BadReading`. It's a *source* identity. File and line now; topic
and sequence number when readings arrive off a ROS 2 topic; sensor and capture time after that. A
field typed as `line_number: int` makes that a rename plus a type change at every read site. A field
shaped more neutrally makes it a change at the one place that constructs it. Either is defensible;
choosing by default is not.

### The bug it found immediately

The first run of the partition test left `{1, 2, 3, 4, 5}` unaccounted for. Line 1 was the header —
expected, since the header is consumed to derive the column count and never becomes a row. Lines 2–5
were four ordinary, valid data rows.

```python
header_parts = list(lines)[0].split(",")
headers_count = len(header_parts)      # 5 — a count of COLUMNS
for i, line in enumerate(lines):
    if i < headers_count:              # used as a count of ROWS
        continue
```

`headers_count` is the number of columns in the header. It was being used as the number of header
*rows to skip*. Five columns, so five rows skipped: the header plus the first four data rows. They
never became `ParsedLine`s, never became `BadReading`s, and never appeared anywhere in the report.

Consequences worth spelling out, because this is what silent data loss looks like from the outside:

- Average velocity, min battery and max temperature computed over 349 rows instead of 353.
- No warning, no error, no log line. The report looked completely healthy.
- **All 29 rejects tests passed.** They had to. Nothing was wrongly rejected — the rows were never
  *considered*.

This is the class of bug the accepts side exists for. The rejects side cannot see it even in
principle.

### One more thing the partition caught free

Once the header-skip stopped masking the pipeline, the accepts test turned up `assert 238 not in
{...}`: line 238 appearing as a good reading while also being in the known-bad set. That's the
already-known attribution bug — the wrong row of a swapped pair gets blamed, so the right row never
gets removed and passes as valid.

One defect, now visible from two directions: the rejects test says the wrong line was blamed, the
accepts test says the right line wasn't removed. Property 2 detected it with no new expected values
written down.

### Mechanics worth keeping

- **There is no empty-set literal.** `{}` is an empty *dict*, so `set() == {}` is `False` — an
  assertion written that way can never pass, even on success. Use `set()`, or `assert not leftovers`.
- **Prefer a set comparison to a loop of asserts.** A loop stops at the first failure and reports one
  item; `assert a == b` on two sets makes pytest print the full symmetric difference, labelled by
  direction. That one line is what produced `Extra items in the left set: (235, ...)` / `right set:
  (238, ...)` — the attribution bug stated exactly, with no message and no flag.
- **Don't build an assertion out of `and`.** `assert found and line_number is not None` can only ever
  print `assert (False)`. Two claims in one assertion means neither is legible, and here one of the
  clauses was dead — the values came from `range()` and could never be `None`.
- **`set.remove()` raises on a missing element**, so a double-accounted row fails as a `KeyError`
  traceback rather than a readable diff. Set difference gives both halves as data.
- **`--showlocals` / `-l`** prints locals at the failure. It's the right tool when an assertion is
  already too coarse to explain itself — and a signal that it is.
- **Don't assert things about the test's own scaffolding.** `len(line_numbers) == len(lines)` after
  building one from the other tests `range()` and the set comprehension, not the project.

## Part 2 — Coverage follows confidence, not risk

The suite at the point this was written:

| Function | Shape | Direct tests | Bugs found in it |
| --- | --- | --- | --- |
| `validate_velocity` | one value in, value or raise out | many | none |
| `validate_battery` | same | many | none |
| `validate_temperature` | same | many | none |
| `validate_timestamp_format` | same | many | none |
| `parse_lines` | iterable in, two lists out, stateful index | **none** | header-skip (silent loss of 4 rows) |
| `validate_timestamp_order` | two values, relational | **none** | untested at rewrite time |
| `validate_robot_timestamps` | list in, mutates it mid-iteration, carries previous row | **none** | attribution (wrong row blamed) |

Twenty-nine tests, all clustered on the four pure functions, all of which already worked. Zero tests
on the three stateful ones, which held every open bug.

### Why this happens

It isn't laziness, and "write more tests" is the wrong correction. The mechanism is specific:

**A test is cheapest to write when you already know the answer.** A parametrized accepts/rejects table
for `validate_velocity` is fast to write precisely because every expected value is obvious before
typing it. That obviousness comes from understanding the function — and a function you understand
well is a function unlikely to be wrong.

So test-writing effort flows toward comprehension, and comprehension is a map of where the bugs
*aren't*. The gap isn't random. It's the exact complement of your confidence, and it gets carved out
by the same force that makes the easy tests easy.

The stateful functions resist for the mirror reason. To write a direct test for
`validate_robot_timestamps` you must first decide what it should do about a swapped pair — which row
is at fault, whether both are, what happens to the row that was used as "previous" but never itself
checked. Those questions are unresolved. Writing the test requires answering them. So the test
doesn't get written, and the ambiguity survives in the code instead of being forced out by the test.

**That is the reason to write it first.** The test is not a check on a decision already made. It is
the thing that makes you make the decision.

### The rewrite trap

The concrete form this took: a rewrite of `validate_timestamp_order` was about to begin, with the
function having no direct tests and its only coverage being an end-to-end test that was *already red*.

Rewrite under those conditions and a green suite afterwards proves nothing. "Something changed" is
all it can mean. Worse, the sample file contains exactly one out-of-order pair and one identical
pair, so it can distinguish "strictly increasing" from "non-decreasing" only by luck — and that
distinction is one character in whatever comparison gets written.

The three tests to write before touching it:

- an ordered pair — passes quietly
- an out-of-order pair — raises
- an **identical** pair — raises, and a *different* error than out-of-order

With hand-written `datetime` literals, not values pulled from the sample. The third is the one
carrying the weight, because strict-vs-non-strict is the flip a rewrite makes silently.

### The usable rule

**Order the test list by where you are least sure, not most.**

It is deliberately uncomfortable. The first test written under this rule is the one whose expected
value you cannot predict — which is the only kind of test that can tell you something you didn't
already know. The tests whose answers are obvious still get written; they just stop being the ones
that get written *first*, and they stop being mistaken for coverage.

## Where this returns

The partition invariant is the general shape for any stage that splits a stream: accepted/rejected,
matched/unmatched, tracked/lost. It comes back in perception (detections that do and don't associate
to a track) and in navigation (goals reached vs. aborted). "Every input ends up in exactly one
bucket, and I can name which" is checkable long before the buckets' contents are.

The provenance question is deferred to week 11 by name — ROS 2 messages have no line numbers, and
whatever identity a reading carries then has to work for both a file and a topic.

## Related

- [11 — Writing tests: what a test claims, and why counting isn't one](11-writing-tests.md) — the
  rejects-side version of the counting argument; this entry is its other half.
- [13 — Fixture resolution, and reading a pytest error from the top](13-fixture-resolution-and-reading-errors.md)
  — ERROR vs FAILED, and why a red that isn't running is worse than no test.
- [08 — Pipeline stages: order, provenance, and streams](08-pipeline-stages.md) — where provenance
  and stage ordering were first pulled apart.
- [10 — Exception taxonomies](10-exception-taxonomies.md) — the `del` that stopped running, in the
  same function as the attribution bug.
