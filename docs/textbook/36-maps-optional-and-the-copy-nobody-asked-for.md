# 36 — Iterators, maps, `optional`, and the copy nobody asked for

**Week 5.** Syllabus items: *Iterators + `<algorithm>`*, and *vector, unordered_map, string_view,
optional*. Prompted by `analysis::temperature::mean`, then a `Robot` holding named temperature
buffers. Related: [34](34-constructors-enforce-invariants.md) (NaN for an empty mean),
[30](30-templates-vs-abstract-classes.md) (why one map can't hold both buffer types).

---

## Iterators: a position, not an address

An iterator promises three things: `*it` gets the element, `++it` moves to the next one, and `==`
compares positions. `v.begin()` is the first element; `v.end()` is **one past the last**, so the
range is half-open, `[begin, end)`, and an empty container has `begin() == end()`.

*"begin and end are just addresses yes?"* For `vector`, basically: its elements are contiguous, so
the iterator is usually a wrapped pointer. For `std::list`, `++it` follows a `next` pointer to a
node somewhere else in memory. For `unordered_map`, it walks hash buckets. The interface is the
same in every case, so one algorithm works on any container. That's the same idea as
`SensorBuffer<T>`: code written once against an interface.

What the "just an address" model gets wrong:

- **`end()` is not an element.** Dereferencing it is undefined behaviour.
- **Iterators go stale.** When a `vector` grows past its capacity, it moves everything to a new
  block of memory, and every iterator into the old block dangles. That's one more reason for the
  `reserve()` in `SensorBuffer`'s constructor.

## `std::accumulate`

```cpp
#include <numeric>   // not <algorithm>
double sum = std::accumulate(readings.begin(), readings.end(), double{0},
    [](double acc, const TemperatureReading& r) { return acc + r.temperature.degrees_c; });
```

This is `functools.reduce(op, v, init)`. **The type of `init` is the type of the result.** With `0`
instead of `double{0}`, the running total is an `int`, and every temperature gets truncated to a
whole number. The existing tests (1, 2, 3) wouldn't have caught it, because they're whole numbers
already. The range-for loop was replaced by this with both mean tests unchanged. That's what tests
are for: the refactor was checked by tests that already existed.

## `unordered_map` without a default constructor

```cpp
imu_sensors[imu_location] = SensorBuffer<IMUReading>(imu_buffer_size);
```

failed with `no matching function for call to 'SensorBuffer<IMUReading>::SensorBuffer()'`, pointing
deep inside `<tuple>`. How to read it: find the line that names **your** file (`main.cpp:16:31:
required from here`). Everything in `/usr/include` is library internals reached from that line. The
`()` with nothing in it means something tried to call the **default constructor**, which
`SensorBuffer` deliberately doesn't have (see 34: capacity is required).

`operator[]` works in two steps. It finds the key missing, **default-constructs** a value there,
and only then does `=` overwrite it. That first step can't compile. The map methods:

| Call | Missing key | Needs a default constructor |
| --- | --- | --- |
| `m[key]` | inserts a default-constructed value | yes |
| `m.at(key)` | throws `std::out_of_range`; never inserts | no |
| `m.find(key)` | returns `m.end()` | no |
| `m.emplace(key, args...)` | constructs the pair; may build it before noticing the key exists | no |
| `m.try_emplace(key, args...)` | checks the key first, then constructs the value from `args` | no |

`emplace` works best with **constructor arguments**, `emplace(name, capacity)`. Passing
`SensorBuffer<...>(capacity)` builds a temporary and then moves it into the map, which misses the
point.

## `optional` holds by value, so returning the buffer returned a copy

The first lookup:

```cpp
std::optional<SensorBuffer<TemperatureReading>> get_temperature_sensor_buffer(const std::string&);
```

It didn't compile at first (`->add_readings`, not `.add_readings`: an optional has to be unwrapped).
Even with that fixed, **the mean test would have seen NaN**. The optional holds the buffer *by
value*, so the return statement **copied** the robot's buffer. The test added readings to that
copy, which was thrown away at the end of the statement.

In Python, `robot.get_buffer("battery").add(...)` modifies the real buffer, because Python passes
references to objects around. C++ copies unless asked not to, and **`optional` can't hold a
reference** (`optional<T&>` isn't allowed before C++26). The ways out:

1. Return the **statistic** (`optional<double> mean_temperature(name)`), so the caller never gets
   the buffer.
2. Return a **pointer**, `nullptr` when missing. That's the traditional "maybe a reference".
3. Return a **reference**, and let a missing name **throw**. This is what was built:

```cpp
SensorBuffer<TemperatureReading>& Robot::get_temperature_sensor_buffer(const std::string& name) {
  return _temperature_sensor_buffers.at(name);
}
```

`at` returns a **reference, not a pointer**. A reference can't be null, so when there's nothing to
refer to, `at` throws. The not-found test is `EXPECT_THROW(..., std::out_of_range)`.

**The caller-side trap:** `auto buf = robot.get_temperature_sensor_buffer("battery");` still
**copies**, because a plain `auto` drops the reference. Write `auto& buf`. Similarly, a leftover
bare call to the getter *outside* `EXPECT_THROW` let the exception escape into the test body, and
the test failed.

### Unwrapping an `optional`

| Syntax | If empty |
| --- | --- |
| `*opt`, `opt->member` | undefined behaviour |
| `opt.value()` | throws `std::bad_optional_access` |
| `opt.value_or(fallback)` | returns `fallback` |

In tests, use `ASSERT_TRUE(opt.has_value());` before `*opt`. `ASSERT` stops the test when it fails;
`EXPECT` keeps going into the dereference.

### Two kinds of "nothing"

"No such sensor" (the question is wrong) and "the sensor has no readings yet" (the question is
valid but has no answer yet) are different, and a caller may want to tell them apart. For example,
`nullopt` for the first and NaN for the second. Or, as built, a throw for the first and NaN for the
second.

## Defaults worth keeping: `const`, `explicit`, and passing by value

*"I kinda just sent it on explicit and const… only don't use them if something breaks."* That's a
sound default, with three refinements:

- **`explicit` matters mostly on one-argument constructors**, the ones C++ silently uses as
  conversions (`SensorBuffer<IMUReading> b = 5;`).
- **Small types go by value.** `const std::size_t&` passes an address to an 8-byte number. That's
  no cheaper than copying the number, and it adds an indirection. Cheap types (`int`, `size_t`,
  `double`, pointers, `string_view`) go by value; `std::string`, `std::vector` and readings go by
  `const&`.
- **`const` member functions.** Without `const` after the `()`, `get_ordered_readings()` can't be
  called through a `const SensorBuffer&`. Added this session.

## Using a tool vs finding a place for one

`optional` was learned, then dropped: `at` plus a throw fit the problem better. The frustration
("I just learned optional then ditched it because it's irrelevant to the application") is a fair
criticism of **inventing requirements to tick off checklist items**. Knowing *when not* to use a
tool is the more valuable half. The proposal: when an application doesn't naturally need a
feature, do a separate short drill instead of bending the design around it.

## Open

- **`string_view`** isn't used yet. On a map keyed by `std::string`, `find`/`at` with a
  `string_view` doesn't compile in C++17 (it does in C++20 with a transparent hash); convert with
  `std::string{sv}`.
- Different sensor types in one map is a real design problem: `std::variant` (a closed set) vs
  base class + `unique_ptr` (an open set; the base can't declare `get_ordered_readings`, because
  its return type depends on `T`) vs one map per type. This is Boss Fight #2's question, so it's
  deliberately left open.

**Returns in:** week 7 (serialisation code takes `string_view` naturally; "no reading yet" is a
real `optional`), Boss Fight #2 (the different-sensor-types question).
