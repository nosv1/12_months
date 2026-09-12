# Logging

**Week 1** · checklist item: `logging` (not `print`) · [syllabus](../../SYLLABUS.MD#L108)

Came up while replacing the `print` diagnostics in `telemetry/src/telemetry/main.py`.

---

## The mental model

`logging` separates four concerns that `print` fuses into one:

| Concern | Question it answers | Example |
| --- | --- | --- |
| **Logger** | *Who* is talking | `telemetry.main`, `telemetry.validator` |
| **Level** | *How important* | `DEBUG` … `CRITICAL` |
| **Handler** | *Where* it goes | stderr, a file, syslog, nowhere |
| **Formatter** | *What* it looks like | timestamp + level + module + message |

`print` hardcodes all four: an anonymous speaker, at one severity, to stdout, with no metadata.
Every benefit of `logging` comes from unbundling those.

---

## The rules

### 1. One logger per module, named `__name__`

```python
import logging

logger = logging.getLogger(__name__)
```

At module top, once. In `telemetry/validator.py` this auto-names it `telemetry.validator`, which
gives free per-module control — silence the parser's chatter, keep analysis at `DEBUG` — without
touching any call site. `getLogger` returns the *same object* for the same name, so this is not
expensive and not a new allocation per import.

### 2. Never call `logging.info(...)` — call `logger.info(...)`

The module-level functions (`logging.info`, `logging.warning`, …) operate on the **root logger**
and implicitly configure it on first use. Calling them inside a package hijacks logging
configuration for everyone who imports it, and loses the module name in the output.

This is the single most common logging mistake.

### 3. Libraries log; applications configure

Only the entry point — the `if __name__ == "__main__"` block, or the `main()` an installed script
points at — calls `logging.basicConfig(...)` / `dictConfig(...)`. Nothing in `validator.py`,
`analysis.py`, or the parser ever configures anything; they only emit.

The payoff: import `telemetry` from a notebook or another program and *that caller* decides where
the logs go.

### 4. Levels mean "who needs to act", not "how bad it feels"

| Level | Meaning |
| --- | --- |
| `DEBUG` | Tracing for the developer. Off in normal runs. |
| `INFO` | Normal progress a user might want confirmed — "parsed 412 readings from 3 robots". |
| `WARNING` | Something is off, the program handled it and continues. **A malformed input row is this.** |
| `ERROR` | An operation failed — the program may continue, but something the user wanted did not happen. |
| `CRITICAL` | Cannot continue. |

**The default level is `WARNING`.** So `logger.info(...)` with no configuration produces
*silence*. That surprises everyone once. It is not a bug.

### 5. Logging goes to stderr by default — and for a CLI that is the whole point

Results to stdout, diagnostics to stderr. That separation is what makes this work:

```sh
uv run telemetry data/sample_telemetry.csv out/ > results.json
```

— a clean JSON file, with the warnings still visible on the terminal. `print` fuses the two
streams and makes the program un-pipeable.

### 6. Pass arguments; don't f-string

```python
logger.warning("line %d missing data: got %d fields", i + 1, len(parts))   # yes
logger.warning(f"line {i + 1} missing data")                               # works, but no
```

Two reasons, one weak and one strong:

- *Deferred formatting* (weak): the `%s` form doesn't build the string unless a handler actually
  accepts the record, so a `DEBUG` call in a hot loop costs almost nothing when `DEBUG` is off.
  Negligible outside hot paths.
- *Structured data* (strong): the arguments stay discrete values on the `LogRecord`. That's what
  structured logging and log aggregators consume. An f-string has already destroyed the structure.

The f-string style is common in real code. Pick one and be consistent.

### 7. In an `except` block, use `logger.exception(...)`

Logs at `ERROR` **and** attaches the traceback automatically. Only valid inside an active
exception handler. Elsewhere: `logger.error("...", exc_info=True)`.

### 8. Log it or raise it — not both

The anti-pattern is catching, logging, and re-raising at every layer, so one failure prints five
times with five tracebacks. Decide where the **error boundary** is — the place that actually
handles the failure — and log *there*, nowhere deeper. See [exceptions and error
boundaries](02-exceptions-and-error-boundaries.md).

### 9. Let the user set the verbosity

`-v` / `--verbose` or `--log-level`, mapped to `basicConfig(level=...)`. This is why `logging` and
`argparse` are naturally one task and not two.

### 10. Never log secrets, credentials, tokens, or personal data

Logs get shipped, aggregated, and read by people who were never meant to see them. Irrelevant to
robot telemetry; critical the moment there's an API key.

### 11. Watch volume in loops

One line per bad row is fine for a 400-row sample and a catastrophe for a 10M-row file where every
row is bad. Usual answer: log each occurrence at `DEBUG`, and one summary count at `WARNING` at
the end.

---

## `print` is not always wrong

"No `print`" gets over-applied. **`print` for the program's actual output is correct** — a CLI
writing its results to stdout is what stdout is *for*, and routing that through `logging` would be
wrong.

The distinction:

- `print(json.dumps(report))` — **output**. Keep it.
- `print("WARNING: line 14 was missing data")` — **diagnostic**. This is what `logging` replaces:
  it needs a level, a destination that isn't stdout, and the ability to be silenced without
  silencing the results.

Same function, two different jobs.

---

## Open questions (decide per project)

- Is a bad input row `WARNING` or `INFO`? What would you want to see by default on a 400-row file?
  On a 10M-row file?
- Does the *count* of bad rows belong in the log, the report, or both?
