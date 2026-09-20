# Union-typed fields, and who owns exception context

**Week 2, boss fight #1** · deliverable requirements §5 (warnings name the robot and the timestamp)
and §6 (rejected rows carry reasons) · [syllabus](../../SYLLABUS.MD)

Two design questions raised at the end of the fight, both of which produced code its author
correctly described as gross. They look unrelated. They are the same question: **where does
knowledge live?**

---

## Question one: a row has five fields of three different types

A reading holds a `datetime`, a `str`, and three `float`s. Modelled as a dict:

```python
self.fields: dict[str, datetime | str | float]
```

Now every consumer of a field gets a union back, and functions that compare floats do not accept
`datetime | str | float`. mypy is right to complain. The fix applied under time pressure:

```python
value=value if isinstance(value, float) else -1,
timestamp=(timestamp if isinstance(timestamp, datetime)
           else datetime.now().astimezone(UTC)),
```

This silences the type checker by **inventing data**. A fabricated `-1` battery is below the 20%
threshold, so it emits a warning — stamped with the moment the report ran — for a reading that never
existed, into a ticket a vendor engineer reads. Unreachable today, because validation guarantees
the types. Which is exactly why it would survive to the day something changes.

### The one-sentence version

**A union type is a record of information you had and threw away. The `isinstance` check downstream
is you buying it back, and a fallback value is you giving up and forging it.**

### Where the information was lost

At parse time, each field's type was *known* — the validator that produced it knew. Storing all five
in one `dict[str, <union>]` erases that, because a dict has one value type for every key. The type
checker is not being pedantic; it is reporting a real loss.

The alternative is a record with named fields of concrete types:

```python
@dataclass(frozen=True)
class AcceptedReading:
    timestamp: datetime
    robot_id: str
    velocity: float
    battery: float
    temperature: float
```

Then `reading.battery` is a `float`, full stop. No narrowing, no fallback, nothing to fabricate.
This is the **parse, don't validate** idea: the output type of parsing should make the invalid state
unrepresentable, so downstream code cannot ask a question that has already been answered.

### The tradeoff, stated honestly

The dict is not stupid. It buys genuine things:

- **Iteration over fields.** `for header, part in fields.items()` with a `HEADER_VALIDATORS` lookup
  is a real design, and it means adding a sixth column touches config and one dict, not five
  modules. A dataclass makes that loop clumsy.
- **Column-order independence** falls out for free, which §9 flags as undecided and which the dict
  handles correctly.

So the shape is: **a dict is right for the parsing stage, and wrong for everything downstream of
it.** The heterogeneous dict is scaffolding for the loop that builds the record. It should not
be what the loop returns. Convert at the boundary — parse into the dict, construct the typed record
from it, and let everything after that see only the record.

### The counter-argument, which is half right

The author's reason for the dict, stated afterwards: *a reading shouldn't know exactly what it is
carrying other than that it carries a list of fields — `reading.battery` feels too absolute when
headers could change.*

That is a real design position, and where the column set is genuinely open it wins: a new column
touches config and one lookup table instead of five modules.

It does not win **here**, and the reason is worth seeing. The column set is not open. Four other
places already know the fields by name:

- `validate_velocity`, `validate_battery`, `validate_temperature` — named functions per field
- `EXPECTED_HEADERS` — five members, each with its own type and range
- `DEFINED_WARNINGS` — battery and temperature, explicitly
- `validate_header_parts` — **rejects** any unrecognized column as `InconsistentHeaderError`

An unknown column is a hard error, not a passthrough. So a new column cannot arrive without someone
writing a validator, a range, and a decision about whether it warns. The dict buys flexibility that
the surrounding design has already spent, and charges a union type for it.

The distinction that resolves it: **open at the edges, closed in the core.** Parsing is the edge —
iterate the header, look up a validator, stay data-driven. But a row that has been *accepted* has a
known schema by definition, because it passed a check that enumerates the fields. A typed record
isn't claiming the columns can never change; it is the record of a row that matched the schema in
force when it was parsed.

There is also a shape that satisfies both positions, because the union comes from three *types*
sharing one dict, not from the fields being named:

```python
timestamp: datetime
robot_id: str
values: dict[str, float]   # still header-driven, still generic
```

`values["battery"]` is a `float` with no narrowing and nothing to fabricate, and a new numeric
column still touches only config. The two fields kept separate are the two that are structural
rather than measured — the ones every consumer special-cases anyway.

### The requirement nobody asked about

The stated motivation was "headers could change," traced back to §9: *"Can columns be reordered? We
have only ever sent them in the order above. We have not promised that."*

That is a question about **order**, not about which columns exist. It was read as a hint to
generalize over the header set, which is a different and much larger claim — the customer has said
nothing about adding or removing columns. §9's whole instruction is *"Ask us before assuming an
answer to these."*

Designing for the unasked version of a requirement is how speculative generality gets in: the cost
is paid immediately, in a union type and an `isinstance` at every use, while the benefit is
hypothetical. If the answer comes back "yes, we will add columns," the dict is correct and the
typed record is the wrong call. **Ask first; the answer changes which design is right.**

### The rule worth keeping

**Never let a type-narrowing branch invent a value.** When `isinstance` fails, there are exactly two
honest moves: raise, or restructure so the check is unnecessary. `else -1` and `else now()` are
neither — they convert a type error into silent bad data, which is the most expensive kind.

---

## Question two: should a validator know which robot it is validating?

The instinct, in the author's words: *"it felt wrong sending robot id to a validate_value function —
the job of the function is to validate it, not handle the exception."*

That instinct is correct, and worth keeping. A function that answers "is this timestamp after that
one?" should not need to know about robots, fleets, or CSV files. Widening its signature to carry
context it never uses is how a general-purpose predicate becomes application-specific.

But look at what the instinct cost:

```python
def validate_timestamp_order(timestamp, prev_timestamp) -> None:
    if timestamp == prev_timestamp:
        raise TimestampIdenticalError("unknown", timestamp, prev_timestamp)
```

The exception's message wants a robot id. The validator doesn't have one, so it passes the string
`"unknown"` — and the caller then catches each error only to **rebuild the same exception** with the
real id, in a nested `try`/`try` with two branches that do identical work.

The protected purity of the validator is paid for twice at the call site.

### Naming the actual mistake

It is not "the validator should have taken a `robot_id`." It is that **the exception was given a
field it had no way to fill.** `TimestampIdenticalError.__init__` requires `robot_id`, which forces
every raise site to produce one, including sites that cannot know it. The `"unknown"` sentinel is
the tell — the same lesson as [16](16-folds-sentinels-and-where-missing-leaks.md), where a sentinel
seeded inside a loop escaped into the report. A placeholder that leaves the function that invented
it is always a design report.

Notice too that the robot id is **already known at the call site by construction**: the error is
being filed into `robots[robot_id].rejected_readings`. Its position in the output says whose row it
was. Copying that into the message is what created the need to rebuild.

### Four ways to add context to an exception

| Approach | Mechanics | Cost |
| --- | --- | --- |
| Pass context in | Validator takes `robot_id` | Couples a general predicate to this application |
| Rebuild at the boundary | Catch, re-raise a richer error `from` the original | What was written; verbose, and duplicates the raise sites |
| Attach on the way past | `err.add_note(...)` (3.11+), or set an attribute, then re-raise the **same** object | Keeps one raise site; the note is free-form text, not structured data |
| Render late | Exception carries only what it knows; the **report** composes the message from the error plus the record it is filed under | Message isn't self-contained at raise time |

The last one deserves the most thought, because it dissolves the problem rather than working around
it. If exceptions are **data** — fields, not prose — and formatting happens at the edge where the
report is assembled, then the validator raises `TimestampIdenticalError(timestamp, prev_timestamp)`
with no id at all, and the report writes "amr-02 had matching timestamps…" because it knows which
robot's list it is walking. One raise site, no rebuild, no sentinel, and §6's "reason in plain
words" is produced exactly once, at the place that has all the facts.

The cost is real: an exception that escapes to a log instead of the report prints without the robot
id, since the prose lived in the report layer. Whether that matters depends on whether exceptions
here are control flow that always terminates in the report (they are) or something that can reach a
user directly (they shouldn't).

---

## Open questions

- **Should `TelemetryException` subclasses be data-only?** Currently each `__init__` formats a
  string and calls `super().__init__(msg)`, so the fields are unrecoverable afterwards — the report
  can only re-read the rendered text. Storing `self.robot_id`, `self.value`, `self.range` and
  formatting in `__str__` costs nothing and makes the errors queryable. It would also let
  `unrecognized_failures` be counted by field rather than by `isinstance`.
- **Do the empty subclasses earn their place?** `VelocityIsNotNumberError` adds nothing to
  `ValueStrNotANumber` but its name. A name is a real thing to add — `except VelocityOutOfRangeError`
  reads better than filtering on a field — but eleven near-identical classes is a lot of surface for
  it. See [10](10-exception-taxonomies.md) for when a taxonomy pays off.
- **Where exactly is the dict → record boundary?** Probably `validate_parsed_line`, which already
  returns `AcceptedReading | RejectedReading` and is the natural funnel.

---

## Where this returns

Sensor messages in ROS 2 are typed records for this reason: a `sensor_msgs/Imu` does not hand over
`dict[str, float | Header]` and invite the subscriber to check. The same question arrives in C++ as
`std::variant` and the visitor pattern, where the compiler will not let you skip the narrowing at
all — and where a fabricated default is a much harder mistake to make by accident.

Related: [02](02-exceptions-and-error-boundaries.md) on error boundaries,
[10](10-exception-taxonomies.md) on taxonomy design, and
[12](12-exception-chaining-and-lint-rulesets.md) on `raise X from Y`, which is what makes the
rebuild-at-the-boundary option defensible when it is the right call.
