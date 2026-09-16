# `raise X from Y`, and letting a linter teach you

**Week 2** · deliverable requirement: "every way a row can be bad is reported" ·
[syllabus](../../SYLLABUS.MD)

Turning on ruff's bugbear rules flagged every re-raise in `validator.py`. Acting on the flags took
about two minutes and broke two tests instantly, because the operands went on backwards. Both
halves of that — the linter finding real work, and the fix being subtly wrong — are the lesson.

---

## The one-sentence version

**`raise NEW from OLD`. The exception that propagates goes first; `from` attaches the cause and
points backwards in time.**

---

## The bug

Before, in `validate_float`:

```python
except ValueError:
    raise NotANumberError("", float_str)
```

After adding `from`:

```python
except ValueError as ve:
    raise ve from NotANumberError("", float_str)      # backwards
```

That raises the **`ValueError`** and files the custom exception as its cause. The stdlib error
escapes, the whole exception taxonomy is bypassed, and the `except TelemetryException` boundary in
`validate_parsed_line_values` never matches. The traceback said so directly:

```
E   ValueError: could not convert string to float: 'ERR'
```

The same inversion appeared in all four field validators —
`raise nan from VelocityNotANumberError(velocity_str)` re-raises the *generic* error and files the
*specific* one as its cause. `test_nan_velocity` expected `VelocityWasNaNError` and got
`NaNError`.

Correct:

```python
except NaNError as err:
    raise VelocityWasNaNError(velocity_str) from err
```

**The check that catches it:** read the chain out loud. *"The velocity wasn't a number, **because**
`float()` raised `ValueError`."* Cause on the right. If the sentence comes out backwards, so is
the code.

And note what `from` does **not** do: it never changes which exception propagates. The original
code was already raising the right exceptions. `from` only adds the link.

---

## What the link is for

Python has two chaining slots on an exception:

- `__context__` — set **implicitly** whenever an exception is raised inside an `except` block. You
  get this for free, and the traceback prints *"During handling of the above exception, another
  exception occurred."*
- `__cause__` — set **explicitly** by `from`. The traceback prints *"The above exception was the
  direct cause of the following exception."*

So the information was never being lost — it was being reported as a coincidence rather than as a
causal chain. `from` is the difference between "two things happened" and "this happened because of
that."

There is also `raise X from None`, which deliberately **suppresses** the chain. That's the right
tool when the inner exception is an implementation detail the caller should never see — a legitimate
option for `validate_float`'s internals, and a decision worth making on purpose rather than by
omission.

---

## Linter rule sets

ruff reimplements a pile of older linters and keeps their original code prefixes, so rules stay
recognizable:

| Prefix | From | Catches |
| --- | --- | --- |
| `E`, `W` | pycodestyle | formatting and style |
| `F` | pyflakes | unused imports, undefined names |
| `B` | flake8-**b**ugbear | likely-bug patterns |
| `C4` | flake8-**c**omprehensions | clumsy comprehension and literal constructs |
| `BLE` | flake8-blind-except | bare `except Exception` |
| `T10` | flake8-debugger | stray `breakpoint()` |

Individual rules are prefix + number: `B904` is "raise without `from` inside an except", `C401` is
"unnecessary generator". A bare prefix means the whole set.

### Using them

**Try before committing to it** — nothing persisted:

```
uv run ruff check --select B .
```

**Ask what a code means.** Nobody remembers `B904`:

```
uv run ruff rule B904
```

That prints the rule name, its source linter, what it catches, why it matters, and a before/after
example. Doing this on every unfamiliar code is what turns a linter into a teacher rather than a
nag.

**Make it stick**, in `pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "C4"]
```

`select` **replaces** the default list, so the defaults have to be restated — the usual first
surprise. `extend-select` adds to them instead.

**Escape hatches**, for when a rule is wrong about a specific line:

```python
raise VelocityNotANumberError(value) from err  # noqa: B904
```

Always with the code. A bare `# noqa` silences everything on that line forever. For whole
directories, `[tool.ruff.lint.per-file-ignores]`.

**Some rules fix themselves:** `ruff check --fix` applies safe fixes; `--diff` previews them.
`--unsafe-fixes` can change behavior — not a default.

---

## The configuration trap this surfaced

Investigating which rules were active turned up the actual finding: there was **no ruff config in
the repo at all**. No `[tool.ruff]` in `pyproject.toml`, no `ruff.toml`. And:

```
$ uv run ruff check .
All checks passed!
```

Yet `BLE001` and `T100` had both fired the previous session and driven real fixes. Those came from
the **editor's** ruff extension, running its own selection.

So the editor and the terminal disagreed about what counts as a lint error, and a CI job would have
agreed with neither. Putting `select` in `pyproject.toml` is what collapses all three into one
tool. Worth doing *before* CI exists rather than debugging it after.

**Generalization:** any tool with both an editor integration and a CLI has this failure mode. The
config file in the repo is the single source of truth; if a tool is configured anywhere else, it is
configured differently for every person who checks the code out.

---

## Open questions carried forward

- No `from` on the remaining re-raises outside the field validators.
- `NotANumberError("", float_str)` — the empty first argument still has no stated purpose. It only
  works because every caller wraps and re-raises. Fixing the `from` direction made it more visible,
  not less.
- Whether `validate_float`'s internal errors should chain at all, or be suppressed with
  `from None` as implementation detail.
- `C4` and `B` are worth keeping; the rest of the default-plus set hasn't been reviewed.

---

## Where this returns

C++ (weeks 3–7) has no exception chaining, and the equivalent discipline is wrapping errors with
context while preserving the original — which is why `std::nested_exception` exists and why almost
nobody uses it. The habit that transfers is the question, not the syntax: *when this surfaces three
layers up, does the message say what was being attempted as well as what failed?*

Related: [10 — Exception taxonomies](10-exception-taxonomies.md) built the classes this chains
together; [02 — Exceptions and error boundaries](02-exceptions-and-error-boundaries.md) is where
the one-boundary-per-row rule came from.
