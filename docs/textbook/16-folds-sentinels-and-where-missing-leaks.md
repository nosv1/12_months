# Folds, sentinel seeds, and where "missing" leaks

**Week 2** · deliverable requirement: the report is machine-readable and must not emit an infinity ·
[syllabus](../../SYLLABUS.MD)

`RobotAnalysis` collected three statistics per robot like this:

```python
@dataclass
class RobotAnalysis:
    max_temperature: float = -float("inf")
    min_battery: float = float("inf")

# ...
for r in robot.readings:
    sum_velocities += r.velocity
    robot_analysis.max_temperature = max(robot_analysis.max_temperature, r.temperature)
    robot_analysis.min_battery = min(robot_analysis.min_battery, r.battery)
```

Correct for every robot in the sample file, because every robot there has at least one good row.
Give it a robot whose *only* row is rejected and the report says:

```json
"average_velocity": null,
"max_temperature": -Infinity,
"min_battery": Infinity
```

The customer's §7 names this exactly: *"`-Infinity` breaks it… do not emit an infinity."* Forty
green tests never saw it, because every fixture was the one sample file and every robot in it has
good rows.

`-Infinity` is also not legal JSON. It is a Python `json` module extension, which is precisely why a
strict parser on the far end dies on it. `json.dumps(obj, allow_nan=False)` raises `ValueError`
instead of emitting it — both a guard and a ready-made test oracle.

---

## The one-sentence version

**A sentinel is a private convention of a loop. The bug is never the sentinel — it is the sentinel
escaping to somewhere that doesn't know the convention.**

---

## What a fold is

A **fold** — also called a **reduce**, the two words mean the same thing — collapses a sequence into
one value by repeatedly combining a running value with the next item:

```python
running = seed
for item in items:
    running = combine(running, item)
```

All three statistics above are folds, and naming them that way makes the seed visible as a separate
decision from the combining:

| statistic | seed | combine |
| --- | --- | --- |
| `sum_velocities` | `0` | `+` |
| `max_temperature` | `-inf` | `max` |
| `min_battery` | `+inf` | `min` |

The seed has to be an **identity** for the operation: a value that, combined with anything, gives
back that other thing. `0` is the identity for `+`. For `max` over the reals the identity is `-inf`,
and for `min` it is `+inf`. That is not a trick — it is the only value that works, and it is why the
seed gets *chosen* rather than defaulted to zero.

Same idea elsewhere: `functools.reduce` is Python's generic spelling, `np.array.max()` and
`df.agg()` are folds over a column, `std::accumulate` is the C++ one (week 4), and the "Reduce" in
MapReduce is this and nothing more.

---

## Why the sentinel leaks

`0` as a seed for a sum is harmless: an empty sum genuinely *is* zero, so the seed is a real answer.

`-inf` as a seed for a maximum is not a real answer. It is a placeholder meaning *"nothing has been
seen yet."* It is only correct while it stays inside the loop, because only the loop knows the
convention. Reach the report and a consumer would have to know your seed convention to read your
data — and it can't, so it crashes.

Any sentinel needs a boundary where it converts to an honest representation of "absent":

```python
max_temperature = None if not readings else running_max
```

This is the same bug family as the falsy-`0.0` return from week 1
([02 — exceptions and error boundaries](02-exceptions-and-error-boundaries.md)): **an in-band value
standing in for "no value."** There, `0.0` meant both *a parked robot* and *no reading*. Here,
`-inf` means both *a temperature* and *no temperatures*. The fix is the same both times — get the
"absent" case out of the value's own domain.

---

## The better tool: `default=`

`max` and `min` take a `default=` keyword, returning it when the sequence is empty:

```python
max([31.2, 38.3], default=None)   # 38.3
max([], default=None)             # None
```

This deletes the seed rather than converting it, so there is nothing left to leak. It also cannot
hide a missing value mid-sequence: the default is returned *instead of* comparing, never *as part of*
a comparison.

**The gotcha**, which costs half an hour if you don't know it: `default=` exists only on the
single-iterable overload. The pairwise form has no `default`, because two arguments can't be empty.

```python
max(running, r.temperature, default=None)   # TypeError — no such overload
```

mypy reports this by listing the overloads it *would* accept. Reading that list is the skill: find
`default` in each variant and note that every one of them takes one positional `Iterable`. Diffing
your call against the listed shapes beats guessing at annotations.

So the two options are about the **form**, not the types:

1. **Keep the running variable** — one pass over the readings for all statistics, but it needs a
   comparable seed (`-inf`) and an explicit conversion at the boundary.
2. **One call per statistic over the whole sequence** — no seed, `default=` handles empty, but one
   pass per statistic.

At 363 rows the pass count is irrelevant. Pick for readability.

---

## Why `max` won't just accept `float | None`

Asking `max(None, 31.2)` to return `31.2` is asking `None` to behave as `-inf`. But `min` shares
that signature, and there `None` would have to behave as `+inf`. One value, opposite meanings, two
functions that cannot both be right.

The stronger reason is semantic. `None` means *missing*. If `max` silently let it lose, an absent
temperature mid-shift would quietly become "the coldest reading," and a missing value would have
become a data point. That is the failure the requirements reject `NaN` for — *"the sensor returned
nothing and something downstream papered over it."* A tool whose job is refusing to paper over
missing values is built on a language that refuses the same thing one level down.

Python 2 did allow it: `None < 3` was `True` and everything was comparable to everything. Python 3
removed it because it hid exactly this bug.

**The SQL/pandas instinct is not wrong, though.** SQL's `MAX()` ignores `NULL`s and pandas `.max()`
skips `NaN` by default, so years of data work build a real expectation that aggregates tolerate
missing values. The difference is that those are aggregations *over a whole column* — they see
everything at once and can define "skip the missing ones." Neither offers a pairwise `MAX(a, b)`
that guesses about `NULL`. The behaviour is real; it lives in the one-call form, which is option 2
above.

---

## Open questions

- Should `min_battery`/`max_temperature` be `None` for a robot with no valid readings, or should the
  robot be absent from the report entirely? `None` says "we saw this robot and learned nothing";
  omission says "we never saw it." Those are different facts for a shift lead, and the requirements
  don't settle it — a customer question.
- The guard and the types can each handle the empty case. Doing both means the "no readings" fact is
  represented twice; keeping one is simpler but the choice depends on which form above wins.

---

## Where this comes back

`std::accumulate`, `std::max_element` and `std::numeric_limits<T>::lowest()` in weeks 3–4 — C++ has
no `default=`, so `max_element` on an empty range hands back an end iterator and the sentinel
technique returns as the normal approach. The habit to carry over is not "avoid sentinels" but
**"name the boundary where the sentinel becomes `absent`."**

Related: [02 — exceptions and error boundaries](02-exceptions-and-error-boundaries.md) on in-band
values for "no value", [11 — writing tests](11-writing-tests.md) on why one shared fixture hides
this class of bug.
