# Exceptions and error boundaries

**Week 1** · checklist item: exceptions and error boundaries · [syllabus](../../SYLLABUS.MD#L112)

Came out of a two-day bug in the telemetry parser. The lesson is not "how to write `try`" — it's
**what shape a function returns when it can fail**, and where failure gets handled.

---

## The bug that motivated it

`Validator.validate_float` returned a pair: `(value, None)` on success, `(False, msg)` on failure.
Callers tested the value for truthiness:

```python
valid_float, msg = Validator.validate_float(s)
if not valid_float:      # <-- the bug
    ...
```

A parked robot reports `velocity == 0.0`. `0.0` is falsy. So ~12 seconds of legitimate readings
were **silently discarded as invalid** and the reported average velocity was wrong. No crash, no
message, no traceback — just a plausible-looking wrong number.

**Rule:** never use truthiness to test whether an operation succeeded. `0`, `0.0`, `""`, `[]`,
and `False` are all valid values *and* all falsy. Test the success flag explicitly, or — better —
use a shape where the question can't be asked wrongly.

## Why annotating the type harder doesn't fix it

The next attempt was to declare `-> tuple[Validator, float]` and keep returning
`(Validator(False, msg), None)`. mypy said, six times:

```
error: Incompatible return value type (got "tuple[Validator, None]", expected "tuple[Validator, float]")
```

mypy wasn't confused about the invariant. It was reporting that **the annotation was false at the
return statement**. Annotating the type you *wish* you returned doesn't satisfy a type checker; it
just moves where it points. The only way to quiet it is `# type: ignore`, which is asserting the
invariant by hand again.

The intermediate attempt — four `assert type(x) is float` lines at the call site to narrow the
`Optional`s — has the same character, plus `assert` is **stripped entirely under `python -O`**. A
safety check that vanishes under an optimisation flag is not a safety check.

### The real diagnosis

The invariant was *"if slot 0 says valid, then slot 1 is not None."*

That is a **correlation between two independently-typed slots of a tuple**. The type
`tuple[Validator, float]` describes each slot separately, so there is nowhere to write "slot 1's
type depends on slot 0's *value*". A pair type can only say "both always present" (false) or
"second is optional" (true, but loses the correlation at every call site).

The tell that you're in this situation: **a comment explaining the invariant in English**, because
the types couldn't say it —

```python
# at this point we KNOW all input values are valid so we can confidently
# convert the strings to proper datatypes and send them to Reading
```

— and *N* call sites all doing the same damage control for one return shape. When the refactor is
right, that comment becomes unnecessary. That's the test for whether you've landed it.

## The two fixes

1. **Take failure out of the value channel entirely.** The function returns a real `float`;
   failure leaves by a different route (an exception). No `Optional`, nothing to narrow, one
   conversion.
2. **Make success and failure two distinct types** — one object that cannot be half-filled, so the
   checker can narrow to one case and know the value is present in that branch. (A `Result` /
   `Ok`-`Err` type. Common in Rust; available in Python via a tagged union + `TypeGuard`.)

Not a fix: removing the *value* and keeping the status object. That was tried, and it forced the
parser to re-convert every string a second time — see below.

## Validation and conversion are the same operation

`float(s)` **is** the validity test. There is no way to know a string is a valid float other than
converting it.

So a validator that answers "is this valid?" without handing back the value throws away work it
already did, and the caller must convert again. Worse than wasteful: it's a second, unchecked
conversion that has to *agree* with the first. Nothing enforces that it does.

**One operation, one return.**

## What the fix looked like

```python
@staticmethod
def validate_battery(battery_str: str) -> float:
    value = Validator.validate_float(battery_str)
    if not (0 <= value <= 100):
        raise ValueError("battery is not within range [0-100]")
    return value
```

and at the boundary:

```python
try:
    timestamp = Validator.validate_timestamp(...)
    velocity = Validator.validate_velocity(...)
    battery = Validator.validate_battery(...)
    temperature = Validator.validate_temperature(...)
except ValueError as e:
    robot.bad_readings.append((line, str(e)))
    continue
```

Result: mypy clean, one conversion per field, invariant comment deleted, and the zero-velocity
rows preserved.

---

## Mechanics

### Attaching a message

The message is the constructor argument, and `str(e)` retrieves it:

```python
raise ValueError("battery is not within range [0-100]")
...
except ValueError as e:
    messages.append(str(e))
```

Builtins come with messages already written — `float("ERR")` raises
`could not convert string to float: 'ERR'`, which **names the offending value**.

### `str(e)`, not `e.args[0]`

`args[0]` assumes the exception was constructed with at least one argument. A bare
`raise ValueError()` anywhere in the call tree then throws `IndexError` *inside your error
handler*. `str(e)` is defined for every exception.

### Custom exception types

```python
class FieldError(ValueError):
    def __init__(self, field: str, msg: str):
        super().__init__(f"{field}: {msg}")
        self.field = field
```

`super().__init__(...)` is what sets `str(e)`. Extra attributes let the handler do structured
reporting (`e.field`) as well as human reporting (`str(e)`).

**Choose the base class deliberately.** `except ValueError` catches `FieldError` only if
`FieldError` subclasses `ValueError`. That choice is how you control whether callers can tell
*your* domain rules ("battery out of range") apart from Python's conversion failures ("not a
number"). Don't subclass `Exception` by reflex.

### Don't re-raise a worse message

```python
try:
    return float(float_str)
except ValueError:
    raise ValueError("ValueError - could not convert a value to float")   # information lost
```

This discards Python's message, which named the offending value, and leads with the exception's
class name — which the reader can already see. Either let the original through, or use
`raise ... from e` to add context *without* dropping the cause.

### Guard the value, not its spelling

`float_str.lower() == "nan"` catches `"nan"` and `"NaN"` but not `" nan"` — and `float(" nan")`
succeeds. Checking a value by string-matching its *spelling* has this class of hole generally.
`math.isnan` on the converted value doesn't.

---

## Error boundaries

An **error boundary** is the one place that decides what a failure *means* for the program. Below
it, code raises and doesn't apologise. At it, you catch, log, and choose: skip the row, use a
default, abort the run.

- **Log it or raise it, not both.** Catching → logging → re-raising at every layer prints one
  failure five times. Log at the boundary only. See [logging](01-logging.md), rule 8.
- **Put the boundary where the decision lives.** "One bad row shouldn't kill the run" is a
  *parser-level* policy, so the `try` belongs around the per-row work — not inside each validator,
  which has no idea what the caller wants.
- **Catch narrowly.** `except ValueError` says which failures you anticipated. Bare `except:` or
  `except Exception:` around a block also swallows typos, `AttributeError`, and `KeyboardInterrupt`
  — turning bugs into silently skipped rows, which is the original bug wearing a different hat.

## The tradeoff exceptions force

Exceptions **short-circuit**. The accumulate-messages version could report *both* a bad battery
and a bad temperature for one row; the first `raise` ends the row at the first problem.

So `bad_readings` goes from "everything wrong with line 14" to "the first thing wrong with line
14". That is a real design decision about who reads the output — not a detail. Decide it on
purpose, and make sure the type annotation still describes what you're actually storing
(`list[str]` vs `str`).

---

## Carry-forward

This same question returns whenever a component receives data it didn't produce — a ROS callback
handed a malformed message (week 11+), a driver read that times out, a sensor frame that arrives
out of order. The shapes are the same three: raise, return a result type, or drop-and-count.
