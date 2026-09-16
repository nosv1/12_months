# Exception taxonomies: base classes, blind excepts, and where to fail loud

**Week 2** · deliverable requirement: "every way a row can be bad is reported" / "tests from
week 1" · [syllabus](../../SYLLABUS.MD)

This started from a test that could only count:

```python
assert num_bad_readings == 8
```

Eight defects, found. But *which* eight? The only thing a `BadReading` carried about what went
wrong was prose:

```python
BadReading(line_number, line, str(ve))   # "velocity is out of maximum range [-2, 2]"
```

A test asserting on that string breaks the moment the wording changes. So the assertion counted,
because counting was the only stable thing available. The fix — distinct exception types per
failure — was proposed unprompted, and turned into a two-hour detour through most of the ways an
error taxonomy can go wrong.

---

## The one-sentence version

**"Is this one of my errors?" is a question about types. Answer it with the type system — a
common base class — not with a list you maintain by hand.**

---

## The registry that never matched

The first attempt at distinguishing known errors from unknown ones was a set:

```python
KNOWN_EXCEPTIONS: set[Exception] = {
    MissingDataError,
    TimestampOutOfOrderError,
    VelocityOutOfRangeError,
    ...
}
```

and a membership test at the catch site:

```python
except Exception as exception:
    if exception in KNOWN_EXCEPTIONS:
        bad_readings.append(handle_value_error(parsed_line, exception))
    else:
        bad_readings.append(handle_value_error(parsed_line, UnknownError(exception)))
```

That test is `False` every single time:

```
instance in KNOWN_EXCEPTIONS -> False
class    in KNOWN_EXCEPTIONS -> True
```

The set holds **classes**. The caught object is an **instance**. An instance is never equal to its
own class, so 100% of validation errors took the `else` branch and were reported to the customer as
unknown — including the ones the taxonomy had been built to name. The bucket that was supposed to
alarm at zero contained everything.

`type(exception) in KNOWN_EXCEPTIONS` fixes that one line and still doesn't work, because it can't
see subclasses. `VelocityNotANumberError` inherits from `NotANumberError`; unless it is listed
explicitly, it is "unknown."

### mypy had already said so, ten times

```
exceptions.py:87: error: Argument 1 to <set> has incompatible type
                  "type[MissingDataError]"; expected "Exception"
```

The annotation `set[Exception]` described the *intent* — a set of instances, which is what the
membership test assumed. The contents were `type[Exception]` — classes. The annotation and the
contents contradicted each other, and that contradiction **is** the bug.

Worth sitting with: a type checker found a logic error, not a typo. That is the argument for
annotating things that look too obvious to annotate. The annotation is a second, independent
statement of what you meant, and bugs live in the gap between the two.

## The base class does it for free

```python
class TelemetryException(Exception): ...

class VelocityOutOfRangeError(TelemetryException): ...
class MissingDataError(TelemetryException): ...
```

```python
except TelemetryException as te:     # known
    ...
```

The registry deletes itself. Subclasses work automatically. And a new exception class **cannot be
forgotten**, because it can't be defined without choosing a parent — the thing that was previously
a maintenance obligation is now a syntax requirement.

The general rule this instantiates: *when a fact is already encoded in the program's structure,
reading it back out at runtime is a bug waiting to happen.* A parallel list of "things that are
X" drifts from the actual set of things that are X. Inheritance can't drift.

## Why ruff hates `except Exception` — and the example that proved it

```
BLE001 Do not catch blind exception: `Exception`
```

The objection is not to having a fallback. It's that `except Exception` catches **your bugs**
alongside the data's defects. `TypeError`, `AttributeError`, `KeyError` — programming errors — get
filed as "a bad row" and reported to the customer instead of crashing where you'd see them.

That was happening, and it had eaten a whole feature:

```python
def validate_float(float_str: str) -> float:
    value = float(float_str)
    if math.isnan(value):
        raise NaNError(float_str)      # NaNError.__init__ takes (field, cause)
```

```
validate_float("nan") raised: TypeError -> NaNError.__init__() missing 1 required
                                           positional argument: 'cause'
```

NaN never raised `NaNError`. It raised `TypeError`, sailed past both `except` clauses in
`validate_velocity`, landed in the blind except, and was reported as an unknown bad reading. **NaN
detection was entirely dead**, the test still said 8, and the blind except is what hid it.

This is the concrete form of the abstract warning. A blind except doesn't just risk swallowing
bugs; it converts them into plausible-looking output.

## Fail loud or keep working: it depends who's downstream

Having removed the blind except, the catch-all question returns as a design decision. Two answers,
both correct in their place:

| | Fail fast | Fault tolerant |
| --- | --- | --- |
| On an unrecognized error | crash | quarantine the row, keep going |
| Right when | acting on bad data is worse than stopping | partial results still have value |
| Example | a control loop — a robot moving on bad data | a batch report over dirty third-party data |

The deciding question is **what the person downstream can do about it.** The customer's answer,
when asked:

> it seems better for it to still 'work' and they can put the unknown errors on the side

A warehouse shift doesn't stop because a parser met something new, and "wait for a release" isn't
an action available at 6am. So: quarantine. The side pile has a standard name — a **dead letter
queue** — and the shape recurs anywhere work arrives faster than it can be guaranteed correct.
It comes back in week 11: a ROS node that dies on one malformed message takes the graph down
with it.

Fault tolerance does **not** license scattering blind excepts back through the code. The
reconciliation:

- **One** catch-all, at a single deliberate boundary — here, one row — not sprinkled at every
  call site.
- It **logs loudly** even though it fails quietly in the output. Quiet for the customer, noisy for
  the developer.
- The unknown count is **in the report**, so "zero" is observable rather than assumed.

That last point is what makes the quarantine honest. A side pile nobody counts is a silence.

## Naming exceptions

PEP 8's only formal rule: exception classes are CapWords like any class, and take the suffix
**`Error`** when the thing is an error. Not `Exception`, not `Err`.

The judgment part is where a first draft went wrong. The proposed name for a `float()` failure on
the literal value `ERR` was `ERRAsFloatError`. Two faults, both instructive:

- **It names the input, not the rule.** `"ERR"` is one bad value out of infinitely many; `"abc"`,
  `""` and `"12.3.4"` all hit the same branch.
- **It names the mechanism, not the condition.** "as float" is *how it was discovered*. Swap
  `float()` for a regex or `Decimal` and the condition is identical but the name is a lie.

Useful test: **could this name survive a rewrite of the code that raises it?** If not, it's naming
the implementation.

The convention the stdlib follows is **subject + what's wrong with it**: `ZeroDivisionError`,
`UnicodeDecodeError`, `JSONDecodeError`, `KeyError`. Read as sentences about the condition. The
resulting names — "the velocity wasn't a number," "the battery was outside its range" — turn out to
be almost exactly the human-readable messages, which is not a coincidence: the name and the message
describe the same fact at two levels of detail.

## Chaining: `raise ... from`

When translating a library's exception into one of yours, say so:

```python
raise VelocityNotANumberError(velocity_str) from ve
```

- `from ve` sets `__cause__` → *"The above exception was the direct cause of the following
  exception."*
- Omitting it still chains via `__context__` (you're inside an `except`) → *"During handling of the
  above exception, another exception occurred"*, which reads like a bug in the handler rather than
  a deliberate translation.
- `from None` suppresses the chain, when the original is noise.

ruff's bugbear ruleset flags the omission as **B904**.

## The cost of holding exception objects

Once `BadReading` stores the exception rather than `str(exc)`, the test can assert on
`type(br.exception)` — stable, immune to rewording. Two consequences come with it:

**Serialization.** `json.dump` cannot serialize an exception. `to_json` has to choose what to emit,
and both options are loaded: `str(exc)` returns to prose, while `type(exc).__name__` puts an
internal class name into an external contract. The resolution here was to emit **both** — a stable
`exception` name to filter and group on, and a human `error` sentence for the ticket — because the
customer asked for both and they answer different questions.

**Retention.** An exception object holds `__traceback__`, which holds the frames it propagated
through, which hold their locals. A long-lived list of caught exceptions retains that whole chain.
Irrelevant for 9 bad rows; a slow leak for 5% of a ten-million-row dump. `traceback.clear_frames()`
exists for exactly this. The general shape — *what does this object own, and for how long* — is the
same question C++ asks about every value in week 3.

## What the migration silently broke

Moving off `ValueError` had a cost that no tool caught. This branch:

```python
except ValueError as ve:
    ...
    del parsed_lines[i]        # drop the out-of-order row
```

became **unreachable** the moment the custom exceptions inherited from `Exception` rather than
`ValueError`, and `validate_timestamp_format` began converting the stdlib error into
`TimestampFormatError`. Nothing in that `try` could raise `ValueError` any more.

The consequence was visible only by inspection:

```
amr-03 flagged: [(235, 'TimestampOutOfOrderError')]
   flagged line still in kept list? True
```

The row was reported as invalid **and** kept in the valid set, where it contributed to
`average_velocity`. The report contradicted itself. ruff and mypy both stayed green — dead code
of this kind is invisible to both — and the test only counted bad readings, so it stayed green too.

Two lessons:

- **Changing an exception's base class is a control-flow change**, not a typing change. Every
  `except` clause upstream is a decision that may quietly stop firing.
- **A test that counts rejects can't see a reject that was also accepted.** Asserting on the
  *accepted* count is the other half, and it's cheap.

## Open questions carried forward

- Where the catch-all boundary lives once ordering and value validation are one pass, and whether
  `MissingDataError` belongs under the same base as the field errors — it behaves differently, since
  a row that can't be split into fields has nothing for the other validators to run against. A
  comment can't be caught; a class can.
- Whether `validate_float` should take the field name as a parameter. The current
  `NotANumberError("", float_str)` only works because every caller wraps and re-raises with the
  real name, and nothing enforces that.
- Validity limits are magic numbers inline in the validators, while warning thresholds are
  constructor-injected (`BatteryWarning(min_battery=20)`). Same species of number, two treatments —
  and the difference wasn't decided, it fell out of the Strategy pattern happening to one of them.

## See also

- [02 — Exceptions and error boundaries](02-exceptions-and-error-boundaries.md): one error
  boundary per row, and the falsy-`0.0` bug that established it.
- [08 — Pipeline stages](08-pipeline-stages.md): the stage ordering that this entry's dead `del`
  belongs to.
- [09 — I/O at the edges](09-io-at-the-edges.md): why the test that could only count was the one
  test that reached through everything.
