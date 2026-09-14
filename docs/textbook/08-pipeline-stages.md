# Pipeline stages: order, provenance, and streams

**Week 2** · deliverable requirement: "clean module boundaries" · [syllabus](../../SYLLABUS.MD)

This started as a naming problem: what to call the module holding `parse_telemetry_lines`, the
loop that turns file lines into `dict[str, Robot]`. `preprocessing`, `processor` and `reader` all
failed. Splitting the loop into stages (parse → validate → group) produced the name, and three
bugs followed from the split:

1. The per-robot timestamp check ran before grouping. "Previous reading" then meant the line
   above, and robots' rows interleave in the file.
2. Rejected rows were stored as strings, but the timestamp check only had a `Reading`. The raw
   text was rebuilt from the `Reading`, and the report printed `'202Z,amr-03,1.241,73.9,55.5'`.
3. Grouping moved earlier to fix #1, and then the timestamp *format* was parsed twice. One
   malformed timestamp could produce three `BadReading`s.

All three have one root cause: **the stages weren't ordered by what each one needs.**

---

## The one-sentence version

Write every stage as `input type → output type`. A stage has to come after every stage that
produces what it consumes. If a later stage needs something an earlier stage threw away, the
stages are in the wrong order.

## A name that won't come is a design signal

`processor` and `preprocessing` describe *where* the code sits: "a step in the middle." Every
module is a step in the middle. A good name says what the caller gets back.

`reader.read_file(path) → dict[str, Robot]` failed a different way. The name said "read," but
the function also parsed, validated and grouped. A caller couldn't guess that rows get thrown
away inside something called *read*.

When no name fits, a common reason is that the code does more than one job. The test is to write
a one-sentence docstring. If it needs "and," it's two jobs. This loop needed three.

Standard stage verbs, which make good names: **read, load, ingest, parse, validate, transform,
group, aggregate, analyze, report.**

Those verbs name a *stage*. Naming the function that runs all the stages is a different rule —
see [I/O at the edges](09-io-at-the-edges.md#naming-a-composition).

- **group**: puts items into buckets by key. SQL `GROUP BY`, pandas `groupby`.
- **aggregate**: reduces a bucket to a value: sum, max, mean. That's `Analysis`, not grouping.

## Draw the type chain before writing code

```text
list[str] → ??? → dict[str, list[???]] → ??? → dict[str, Robot]
```

Every arrow is a function and every `???` is a decision. Mark where rejected rows leave at each
arrow. If the types connect, the design works. If an arrow needs a value that isn't in its input
type, it has found a missing dependency.

Two things this caught:

- **A value that changes type changes name.** `{id: list[ParsedLine]}` and `{id: Robot}` are
  different things. Calling both `robots_dict` hides the step that converts one into the other.
- **Lines that fail to parse have no robot.** `robot_id` comes *from* parsing. So a rejected
  unparseable line can't go into any per-robot structure. It needs its own list. The old
  `"unknown"` robot was a workaround for that missing list, and it leaked into the report as a
  robot with `max_temperature: -Infinity`.

## Order comes from dependencies

List what each check consumes and what it produces:

| Check | Consumes | Produces | Needs other rows? |
| --- | --- | --- | --- |
| field count | `str` | `ParsedLine` | no |
| float / NaN / range | `ParsedLine` | `float` fields | no |
| timestamp format | `timestamp_str` | `datetime` | no |
| timestamp **order** | two `datetime`s, **same robot** | ok / reject | **yes**: the previous *good* row of that robot |

Three constraints fall out of the table:

- Order checking needs `datetime`, which is only produced by format checking. So format checking
  comes first. Bug #3 was the order check running first and having to re-parse the format itself.
- Order checking needs "same robot," so grouping has to happen before it. That was bug #1.
- Order checking needs the previous *good* row. If it runs on rows that haven't had their values
  checked, a `nan` row with a future timestamp can get the valid row after it rejected.

**Symptom to watch for:** a stage redoing an earlier stage's work (like `fromisoformat` in two
places) is a sign that the stages are out of order.

## Provenance: keep the source, don't rebuild it

The customer's requirement for a rejected row (2026-09-13):

1. line number in the original file
2. the reason, in plain words
3. **the row exactly as it appeared**, for a firmware ticket

You can't rebuild #3 from a `Reading`. Converting a row loses information, and no inverse gets it
back:

- `0.70` → `float` → `"0.7"`
- `...Z` → `datetime` → `+00:00`
- trailing `\n`, stray whitespace, the exact bytes of a garbage field

`as_unparsed_line` had real bugs as well (`[:3]` sliced the whole string, `%D` is `mm/dd/yy`),
but fixing them wouldn't have helped. **Rebuilding cannot meet the requirement.**

There is also a correct design constraint in play: `Reading` shouldn't know it came from a text file.
A `Reading` could just as well come from a socket or a ROS message. The source belongs on the type
whose *name* says it came from a line: `ParsedLine` now carries `line_number` and
`original_line`.

The rule: **every stage that can reject a row must still have the row's source in scope.** You
can guarantee that by the order of stages, or by keeping the source object next to the converted
one. You cannot guarantee it by rebuilding the source later.

## Batch vs. stream, and why counting loops is the wrong worry

The objection to the split, from this session: "I absolutely despise looping this many times."

**On speed, it's the wrong measure.** Five linear passes over 400 rows take microseconds. In batch
code, clearer stages and testable seams usually win over fewer passes.

**On design, the instinct is right, for a different reason.** Batch means you have the whole file
as a list and can pass over it as often as you like. Stream means rows arrive one at a time, you
never see "the whole list," and all you can keep is state, such as each robot's last good
timestamp.

Robot data is a stream. In week 11 this telemetry arrives on a ROS topic, and a multi-pass design
over `list[str]` can't be ported to it. A design that handles one row at a time with small
per-robot state can.

That design also sidesteps the provenance problem. While you're processing row *N*, its source is
right there.

## Open questions

- **"Validate format first": an earlier *pass*, or earlier in the *same iteration*?** In one loop
  over a robot's rows, what's in scope at row *N*? Is the `ParsedLine` there? Is the previous
  good `Reading`?
- **Swapped pair semantics.** For timestamps `1, 5, 3, 4`, which rows are wrong? Walking
  forward and walking backward flag different ones. This is a requirements question; ask the
  customer.
- **Who turns a `BadReading` into JSON?** `Analysis.to_json` currently knows `BadReading`'s field
  names. It could stay there, or the type could serialize itself.
- **`-Infinity` in the report** for a robot with no good readings: not valid JSON, and the
  customer's dashboard rejects it.

## Gotchas

- **Checking every row twice.** In a pairwise loop, row *i* is `current` once and `previous`
  once. A check run on both reports the same bad row twice.
- **Ignoring a return value.** `parsed_lines, bad_readings = parse_lines(...)`, then never reading
  `bad_readings`. No crash, no type error, one defect silently dropped from the report. Only a
  test that counts rejected rows catches this.
- **Off-by-one in backward loops.** `i = len - 2; while i > 0` never checks the last element.
  Sample data with no defects at the ends of a list hides it.
- **`del` while walking backward** only stays correct because the indexes you haven't visited
  don't shift. A forward walk with `del` skips elements.

## Where it returns

- **Week 11, ROS 2 nodes:** each node is a pipeline stage, and the topic types are the type chain,
  enforced by the middleware. Messages carry provenance in `std_msgs/Header` (`stamp`,
  `frame_id`), which is the same idea as `line_number` + `original_line`.
- **Sensor fusion / state estimation:** out-of-order and duplicate timestamps are routine there,
  and deciding *which* of a swapped pair to trust is a real design choice.
- **Boss Fight #1:** rebuild this from a blank page. The table under *Order comes from
  dependencies* is the part to be able to re-derive.

Related: [exceptions and error boundaries](02-exceptions-and-error-boundaries.md),
[circular imports and dependency direction](07-circular-imports.md).
