# 13 — Fixture resolution, and reading a pytest error from the top

**Week 2.** Satisfies *"tests from week 1"* — specifically the part where the test suite has to
actually run before it can tell you anything.

**Came from:** `pytest ./` reporting `use 'pytest --fixtures [testpath]' for help on them`, read as
"pytest can't find your conftest," when conftest had been found and the real message was two lines
higher up.

---

## The mental model

A fixture is looked up **by exact name**. When a test function declares a parameter, pytest reads
that parameter's name as a request: *find me something registered under this exact string.*

```python
def test_all_defects_caught(telemetry_lines, defined_warnings):
```

This asks for two fixtures named `telemetry_lines` and `defined_warnings`. It does not ask for
"something ending in `_lines`", and it does not ask for "`sample_telemetry_lines`, with the prefix
taken off." The parameter name and the fixture function's name must be the same string.

There is no truncation rule, no prefix-stripping rule, and no fuzzy match. This is deliberate:
fixtures are resolved at setup time from a name, and a fuzzy match would mean a typo silently
binds to the wrong fixture. A name that doesn't resolve is an error, every time.

### Where the confusion comes from

pytest genuinely does have name-prefix conventions, which makes "pytest does something with
prefixes" a plausible thing to half-remember:

| Convention | What the name controls |
| --- | --- |
| `test_*.py`, `test_*` functions | what gets **collected** as a test |
| `pytest_*` | what gets registered as a **hook** |
| `conftest.py` | exact filename — what gets **auto-loaded** |

None of these apply to fixture names. Fixtures are the one place where the name is used as a plain
key, not as a pattern.

### The one indirection that does exist

```python
@pytest.fixture(name="lines")
def sample_telemetry_lines() -> list[str]:
    ...
```

Now tests ask for `lines` and the function is still called `sample_telemetry_lines`. This exists
*because* there is no implicit rule — if the name you want to use in tests differs from the name you
want on the function, you say so explicitly.

The main real use is avoiding a shadowing problem: a fixture named `lines` in a module that also
wants a module-level `lines` variable. Reach for it when you have that problem, not as a matter of
course — two names for one thing is a cost you pay on every future read.

## How conftest.py is found

Worth knowing precisely, because "is it even being loaded?" is the wrong question more often than
it's the right one.

`conftest.py` is **auto-loaded by filename**. Nothing imports it, and it must not be imported —
pytest collects it as a plugin. Discovery walks the directory tree: for a test file at
`tests/test_parser.py`, pytest loads every `conftest.py` from the rootdir down to `tests/`, and
fixtures defined there are visible to tests **in that directory and below**.

So fixtures are directory-scoped, and scope follows the filesystem:

```
telemetry/
  tests/
    conftest.py       fixtures visible to everything under tests/
    test_parser.py    can use them; its own fixtures are visible only here
    test_validations.py
```

A fixture defined inside a test module is visible only in that module. Moving it to `conftest.py` is
how it becomes shared — that's the whole mechanism, and it's why `conftest.py` exists at all rather
than an import.

## Reading the error

The actual output:

```
file .../tests/test_parser.py, line 18
  def test_all_defects_caught(
E       fixture 'telemetry_lines' not found
>       available fixtures: cache, capfd, ..., sample_defined_warnings, sample_telemetry_lines, ...
>       use 'pytest --fixtures [testpath]' for help on them.
```

Four lines, in a specific order, and the order is the lesson:

1. **Location** — file and line of the failing signature.
2. **The failure** — `fixture 'telemetry_lines' not found`. This is the message.
3. **The evidence** — everything that *was* registered.
4. **A generic hint** — the same sentence pytest prints for every fixture problem.

The instinct is to read the last line, because it's the last thing on screen and it's phrased as an
instruction. But line 4 is boilerplate; it carries no information about *this* failure. **Line 2 is
the message and line 3 is the proof.**

Line 3 in particular answers the question that the hint sends you off to investigate. It listed
`sample_defined_warnings` and `sample_telemetry_lines` — the two fixtures from `conftest.py`. They
were registered. conftest was loaded. The only remaining possibility is that the requested name and
the registered name differ, which is visible by putting lines 2 and 3 side by side.

**General rule for tools that print a suggestion:** the suggestion is generated from the error
*category*, not from your specific case. It's the least specific thing in the output. Read up from
it, not from it.

### Error, not failure

These two showed as `ERROR at setup of test_all_defects_caught`, not `FAILED`, and the distinction
matters:

- **FAILED** — the test body ran and an assertion was false. A claim about the code was checked and
  came out wrong.
- **ERROR** — setup or teardown blew up. The body **never ran**. Nothing was checked.

A suite reporting `31 passed, 2 errors` has not told you 31 things are right and 2 are wrong. It has
told you 31 things are right and 2 are *unknown*. Before the fix, the attribution bug in
`test_all_defects_caught` wasn't being exercised at all — the red that was supposed to be tracking
it was invisible, and a red that isn't running is worse than no test, because it looks like coverage.

After the rename: `1 failed, 32 passed`. Same code, same bug — but now the bug is being asserted
against instead of skipped past.

## The naming decision

The mismatch could be fixed from either end, and they are not equivalent:

| Fix | Effect |
| --- | --- |
| Rename the **parameters** to `sample_*` | One definition stays put; the call sites move to it. |
| Rename the **fixtures** to drop `sample_` | Every current and future call site gets the shorter name. |

Taken here: rename the parameters. With one definition and two call sites, the definition wins on
churn alone.

The naming question underneath is still live, though. `sample_` is doing real work — these fixtures
are specifically the *committed sample file*, not telemetry lines in general — and a later fixture
that builds lines inline would want to be distinguishable from it. A fixture name is read at every
call site, so it's worth the same attention as a function name, and "what distinguishes this from
the fixture I'll want next month" is usually the question that settles it.

## Where this returns

Fixture scope and directory-based discovery come back as soon as there is more than one test
directory — the week 2 plan to split `test_validations.py` into parser/validator/pipeline files is
the first time it bites, since a fixture used by two of the three has to sit in `conftest.py` to be
visible to both.

The error-reading habit generalizes well past pytest. C++ template errors, ROS 2 launch failures,
and CMake in particular all bury the message under a wall of consequence and then append a generic
suggestion. Read the first specific line, and read what the tool says it *did* find.

## Related

- [11 — Writing tests: what a test claims, and why counting isn't one](11-writing-tests.md) — what
  the two errored tests were trying to claim.
- [09 — I/O at the edges, and naming the thing in the middle](09-io-at-the-edges.md) — the naming
  problem, in a different place.
- [12 — `raise X from Y`, and letting a linter teach you](12-exception-chaining-and-lint-rulesets.md)
  — also a case of a tool's output being read for the wrong part.
