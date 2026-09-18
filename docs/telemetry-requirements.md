# Telemetry Toolkit — Requirements

**From:** the customer (fleet operations)
**Status:** the agreed contract as of 2026-09-17. Supersedes anything said in conversation.

This is the requirements document, nothing else. It says what the tool must do, not how to build
it. Every statement here was asked for and answered; anything not stated here is not yet decided,
and the open questions are listed at the bottom.

Permitted reading during Boss Fight #1, alongside `sample_telemetry.csv`.

---

## 1. What we have

We run a fleet of autonomous mobile robots in warehouse aisles. Each robot writes a telemetry row
periodically. At the end of a shift those rows arrive as one CSV covering the whole fleet.

We need a tool that reads one of those files and tells us two things: which robots had a problem
during the shift, and which rows of the file we can't trust.

This is batch work, run after the shift. It is not a live monitor.

## 2. The input file

CSV. A **header is always present as the first line, no exceptions.** The columns are:

```
timestamp,robot_id,velocity,battery,temperature
```

A file with no header is a broken export from our side. **Fail loudly on it.** Do not parse it with
a data row standing in for the header — we would rather be told the export is broken than get a
report that silently lost a row and mislabeled every field.

| field | meaning | units |
| --- | --- | --- |
| `timestamp` | when the reading was taken | ISO 8601, UTC |
| `robot_id` | which robot | our identifier, e.g. `amr-01` |
| `velocity` | ground speed, signed | metres per second |
| `battery` | charge remaining | percent |
| `temperature` | motor controller temperature | degrees Celsius |

Rows from different robots are interleaved in the file. That is normal and not a fault.

### Column count

Check each row's field count **against the header of the file being read**, not against a number
written into the tool. We were burned by this: a vendor firmware update appended a column, our old
tooling was hardcoded to the old count, and it rejected all 40,000 rows of a shift.

When the count is wrong, the message must carry **both** numbers, e.g. `Expected 5 columns, found
4.` — that text gets pasted into a firmware ticket, and the ticket is useless without both.

About half of these rows are truncated writes and about half are duplicated delimiters, so don't
tell us *why* the count is wrong. Just tell us it is, and what the two counts were.

Gracefully absorbing *new* columns is **not required yet**. We are asking you not to build
something that makes it impossible later.

## 3. Valid ranges

All bounds are **inclusive**. A value outside its range is a rejected row.

| field | valid range | why this range |
| --- | --- | --- |
| velocity | `-2.0` to `2.0` m/s | the drive firmware hard-caps at 2.0. Reverse is the same magnitude — the robots back into docking stations. |
| battery | `0` to `100` % | it's a percentage. |
| temperature | `-40` to `150` °C | the rated range of the motor controller's sensor. Outside it, the number means nothing. |

**Sub-zero temperatures are valid readings, not faults.** Two of our sites run cold-storage aisles
at −20 °C ambient, and a controller parked overnight reads near that. What we don't accept is a
number the sensor cannot physically produce: `-273.2` is a broken sensor, not a cold aisle.

A field that is not a number at all — blank, `ERR`, a word, anything — is a rejected row. `NaN` is
not a valid reading either; it means the sensor returned nothing and something downstream papered
over it.

## 4. Timestamps

**Per robot, timestamps must strictly increase.** A row that goes backwards relative to that
robot's previous row is a fault, and so is a row with the *same* timestamp as the previous one —
duplicates mean something replayed a buffer, and we need to know.

Ordering is **per robot only**. Two robots reporting the same instant, or a later amr-01 row
sitting above an earlier amr-02 row in the file, is normal.

## 5. Warnings

These are not bad data. They are real conditions we want flagged on a healthy robot:

- **Battery below 20%** — it did not get back to the charger in time.
- **Temperature above 60 °C** — the motor controller is running hot.

A warning must tell us **which robot** and **the timestamp of the reading that triggered it**, so we
can line it up against the aisle schedule.

Both thresholds will change. We have already talked about running the cold-storage sites at a
different battery threshold, so don't bury `20` and `60` somewhere we have to come to you to
change.

## 6. Rejected rows

A rejected row is one we can't trust. Drop it from the analysis — don't guess at it, don't repair
it — and report it.

Each rejected row must carry:

1. **The line number in the original file.** Not the index after filtering. We open the file at
   that line.
2. **The reason in plain words.** This goes into a firmware ticket that a vendor engineer reads.
3. **The row exactly as it appeared in the file.** Not rebuilt from parsed fields — if it round-trips
   through your parser we no longer know what the robot actually wrote, and that's the whole
   evidence for the ticket.

Group rejected rows **under the robot** when we know which robot it was. When the row is so broken
we can't tell — that's what a truncated row looks like — list it **separately**. **Never invent a
robot** to file it under, and never file it under a guess.

### Errors are a list

Every rejected row carries a **list** of errors, always, even when there is only one. One row can be
wrong in several ways at once, and we want all of them in the one ticket rather than finding the
second fault after the vendor has already closed the first.

Each error in that list needs both:

- a **stable name** we can filter and count on across shifts, and
- a **plain-words message** for the ticket.

Both. The name lets us say "out-of-range battery is up 30% this month." The message is what the
vendor engineer actually reads.

### Unrecognized failures

If the tool hits a failure it doesn't have a category for, put it in an **unrecognized** bucket
with a count, and report that count every time — it should always be zero, and the day it isn't we
want to see it in the report rather than hear about it from a shift lead.

**Quarantine the row, don't crash.** A shift cannot wait for a release. One unexpected row must
never cost us the other 40,000.

## 7. The report

Machine-readable output (JSON is fine), because it feeds our dashboard.

One constraint from that dashboard: **`-Infinity` breaks it.** If a computed value has no meaningful
answer — an average over zero readings, say — do not emit an infinity. Say the value is absent, or
say the count was zero, but don't hand us a token our parser dies on.

The report needs, per robot: its warnings, and its rejected rows. Plus the rejected rows that
couldn't be attributed to any robot, and the unrecognized-failure count.

## 8. How we run it

We run this at the end of a shift, on the ops box — not on your laptop, and not from inside your
source tree. Whoever is on shift types one command, points it at the file, and gets the report.
They are not going to activate a virtual environment, set `PYTHONPATH`, or remember which
directory to stand in.

So: it installs, and installing it puts a command on the path. Install it, type its name, hand it a
file. If the answer to "how do I run it" is "cd into this folder and run python on that file", that
doesn't work for us.

Nothing here is about which tool you use to build it. That's yours.

*Asked and answered 2026-09-18.*

## 9. Not yet specified

Ask us before assuming an answer to these. We haven't decided, and a wrong guess is cheaper to fix
now than after it ships.

- **Can columns be reordered?** We have only ever sent them in the order above. We have not promised
  that.
- **When two rows are swapped, should both be flagged, or only the one that arrives out of order?**
  Currently only the second-arriving row looks wrong, and it isn't obviously the guilty one.
- **What should happen when a new column appears?** See §2. Not required yet, deliberately.
