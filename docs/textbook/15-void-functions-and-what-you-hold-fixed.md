# Testing void functions, and noticing what you hold fixed

**Week 2** · syllabus: "`pytest`: fixtures, parametrize, what's worth testing" ·
[syllabus](../../SYLLABUS.MD)

`validate_timestamp_order` used to end with `return True`. A commit removed it as redundant — the
function's whole job is to raise, and nothing ever looked at the return value:

```python
def validate_timestamp_order(timestamp: datetime, prev_timestamp: datetime) -> None:
    if timestamp < prev_timestamp:
        raise TimestampOutOfOrderError(timestamp, prev_timestamp)
    if timestamp == prev_timestamp:
        raise TimestampIdenticalError(timestamp)
```

That turned the suite red, because the accepts test still read:

```python
assert validate_timestamp_order(timestamp, prev_timestamp)   # assert None -> AssertionError
```

The obvious repair is `assert ... is None`. mypy rejects that too:

```
error: "validate_timestamp_order" does not return a value (it only ever returns None)
       [func-returns-value]
```

It rejects **both** forms — `assert f()` and `assert f() is None` — because the objection isn't to
the comparison, it's to reading a value that does not exist. With the `assert` treated as
non-negotiable, the only remaining move is to give the function something to return, and three
commits later it was back to returning `True`, now annotated `Literal[True]`.

The suite went green. Nothing was learned, and a constant had been added to the production
signature to satisfy a test.

---

## The one-sentence version

**A function that communicates by raising has nothing to assert on; "it returned normally" *is* the
assertion.**

```python
def test_timestamp_order_accepts(timestamp: datetime, prev_timestamp: datetime) -> None:
    validate_timestamp_order(timestamp, prev_timestamp)   # no raise == pass
```

Clean under mypy and under ruff. And it tests strictly more than `assert ... is True` did, because
`Literal[True]` can only ever be `True` — asserting it proves the function reached its last line,
which reaching the next line of the test already proved.

---

## Why a test with no assert is still a test

pytest decides pass/fail on exactly one question: **did an exception escape the test function?**

`assert` is not special to pytest. It is special because a false `assert` *raises*
`AssertionError`. So there are three shapes, all the same rule:

| Shape | Fails when |
| --- | --- |
| `assert x == 3` | the comparison is false, so `AssertionError` propagates |
| `f(bad_input)` inside `pytest.raises(E)` | `E` does **not** arrive |
| `f(good_input)`, bare | anything at all propagates |

The third is the right shape whenever the unit under test signals failure by raising. Adding an
`assert` to it can only weaken it — either it asserts a constant, or it invents a return value that
production code has to carry forever.

The smell to recognise: **an `assert` with nothing satisfying to put after it.** That is usually
the code saying there is no value here, not an invitation to manufacture one.

---

## The larger lesson: name what you're holding fixed

The type checker was right, and it was answered backwards. Its complaint was "there is no value
here to inspect," and there are exactly two ways to agree with it:

1. **Manufacture a value** — change the function so there is something to read.
2. **Stop needing one** — change the test so it doesn't read anything.

(1) got picked, not after weighing it against (2), but because the `assert` was never up for
reconsideration. Every fix that kept the `assert` was tried in turn, and the one that survived the
linters won by elimination.

That is the general failure mode. When a tool refuses a change, the instinct is to search the space
of edits that leave the current shape intact. The useful question is the other one:

> What am I treating as unchangeable here, and did I ever decide that?

Often the unchangeable thing is the newest, least-considered part of the design — here, one line of
a test — while the thing being bent to accommodate it is a public signature.

This has a tell in the git history. Four commits in ~25 minutes ending back where they started,
plus a change to production code, is a loop rather than progress. A production signature that moved
so a test would compile is worth re-reading the next morning.

---

## Consequences worth knowing

- **`-> None` is a real contract.** It tells callers there is nothing to check and the only
  outcomes are "returned" or "raised." `Literal[True]` claims a caller might branch on the value.
  No caller does, so the signature now describes a use that doesn't exist — see
  [10 — exception taxonomies](10-exception-taxonomies.md) for the cost of signatures that overstate.
- **Consistency cuts the other way here.** The four field validators return the parsed value, and
  that value is *used* — `validate_velocity` hands back the float that goes into `Reading`.
  `validate_timestamp_order` is relational: it compares two already-parsed values and produces
  nothing new. Looking like its neighbours is not a reason to invent a return.
- **`func-returns-value` is in mypy's default rule set.** It fires on any use of a `-> None` call's
  result — in an `assert`, an assignment, an `if`, an f-string. It is one of the cheapest bug
  catchers mypy has, because the usual cause is a function that forgot to return.

---

## Open questions

- Does the bare-call test need a comment? `# no raise == pass` is three words, and a reader who
  knows the rule doesn't need it. A reader who doesn't will otherwise assume the test is unfinished.
- Should a test named `..._accepts` exist at all for a void function, when the rejects tests already
  pin both raising branches? It pins the *absence* of a spurious raise on the happy path, which the
  rejects tests cannot — so yes, but it is the weakest test in the file, and that is fine.

---

## Where this comes back

Every `void` C++ function, from week 3 on. Also every ROS 2 callback from week 11 — callbacks return
nothing by contract, so the only way to test one is to call it and inspect what it *did* to the
world (a publisher, a member, a mock), never what it handed back. The habit of asking "what does
this function's failure look like?" before asking "what does it return?" is the transferable part.

Related: [11 — writing tests](11-writing-tests.md) on tautological assertions,
[12 — exception chaining and lint rulesets](12-exception-chaining-and-lint-rulesets.md) on acting on
a linter's message backwards.
