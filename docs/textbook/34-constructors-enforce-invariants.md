# 34 — Constructors enforce invariants: fail fast, pick the exception, test the empty case

**Week 5.** Syllabus item: *Exceptions vs error codes.* This came from `SensorBuffer(0)`, which was
harmless when constructed and caused undefined behaviour on the first overwrite. Related:
[32](32-debugging-an-abort-read-the-backtrace.md) (the previous `SensorBuffer` bug),
[33](33-writing-a-class-template.md).

---

## The bug

`_insert_idx()` returns `(_tail_idx + 1) % _buffer_size`. With a capacity of 0, construction
succeeds, `get_ordered_readings()` returns an empty vector, and nothing looks wrong. The failure
only happens at the first `add_readings` call, which computes `% 0`. That is undefined behaviour,
not a guaranteed crash.

The first instinct was the right one: *"throwing the error this late in the code is less than
ideal, surely we should throw as soon as we see buffer size is < 1."*

## The mental model: a constructor establishes the invariant

An **invariant** is something that is true of every object of a class for its whole lifetime. For
this class the invariant is "capacity ≥ 1". Every other member function (`_insert_idx`,
`get_ordered_readings`) is written assuming it holds.

If the constructor refuses to build an object that breaks the invariant, then **every object that
exists is valid**, and none of the other methods needs to check. If the error is thrown late,
inside `add_readings`, the broken object is already out in the program, and the failure happens
far from the line that caused it. On a robot, that could be minutes into a run rather than at
startup. This is **fail fast**.

## Why an exception, not an error code

**A constructor has no return value.** An error-code design would need something like an
`is_valid()` flag that every caller must remember to check, and that brings back the problem of
broken objects in circulation. Exceptions are the only way a constructor can say "no object".

## Which exception

`<stdexcept>` has two families:

- **`std::logic_error`**: mistakes that could have been caught by reading the code. Includes
  `invalid_argument`, `domain_error`, `length_error`, `out_of_range`.
- **`std::runtime_error`**: problems that only appear at runtime (bad input data, I/O failures).

`SensorBuffer(0)` is a programmer error, so it belongs in the logic family. Within that family:

| Exception | Conventional meaning | Fits? |
| --- | --- | --- |
| `length_error` | "exceeds `max_size()`": asked for something longer than the container can ever hold | **No.** It's what `reserve(SIZE_MAX)` throws, so reusing it for 0 would make two different mistakes look the same |
| `domain_error` | a maths input outside the function's domain (`sqrt(-1)`) | Defensible. The standard library itself never throws it |
| `invalid_argument` | the caller passed a value this function doesn't accept | **Conventional** for a constructor rejecting its argument |

**Plain-English readings don't settle this.** Zero *is* a wrong length, and it *is* outside the
domain. Each exception's meaning comes from convention, not from its name. That caused real
friction in the session: picking by name was invited, then two reasonable picks were rejected. The
lesson: when choosing an exception, ask "what would a C++ reader expect this name to mean?", not
"does this name describe my situation?"

### Standard or custom?

The telemetry library used custom exceptions. That was right there: the bad input was *data*, and
callers caught those errors, counted them and reported them by kind, so they needed to tell the
kinds apart. Here the bad input is a line of code, and nobody recovers from it at runtime. The rule:
**use a standard exception when one already names the problem exactly; write a custom one when
callers need to catch your category separately or need extra data attached to it.** Custom C++
exceptions inherit from a standard one anyway.

## `size_t` and `-1`

`std::size_t` is unsigned, so "`< 1`" is really just "`== 0`". Passing `-1` wraps around to
`SIZE_MAX` (2⁶⁴−1), and `reserve()` then throws `std::length_error`. That's an accidental guard,
with a message that doesn't say what went wrong.

## Testing it

```cpp
TEST_F(SensorProcessing, BufferSize0Test) {
  std::size_t buffer_size{0};
  EXPECT_THROW(SensorBuffer<IMUReading> buffer{buffer_size}, std::invalid_argument);
}
```

- The two earlier capacity-0 tests asserted the **old** contract: "constructing works, and `add`
  works". They weren't patched, they were **replaced**. Once construction throws, the "add to a
  capacity-0 buffer" case can't be reached, and a test of something that can't happen proves
  nothing.
- **Macro argument commas:** `EXPECT_THROW` is a macro, and the preprocessor splits its arguments at
  every comma that isn't inside parentheses. Braces and angle brackets don't protect a comma, so
  `SensorBuffer<std::pair<int, int>>` inside the macro breaks it. Wrapping a *declaration* in
  parentheses isn't valid C++ (that suggestion was wrong in session). The fixes are an expression
  instead of a declaration, `(SensorBuffer<std::pair<int, int>>{0})`, or a `using` alias defined
  outside the macro.

## The empty statistic: NaN

`analysis::temperature::mean` on zero readings returns NaN (`std::nan("")`). The alternative was
`std::optional<double>`; the tradeoff:

- **NaN** is cheap and conventional in numeric code, but it spreads silently through later
  arithmetic. Telemetry's `-Infinity` reached the JSON output the same way.
- **`optional`** makes the empty case part of the return type, so the caller can't ignore it.

Testing NaN: **NaN is not equal to anything, including itself** (IEEE 754). `EXPECT_EQ(x, nan(""))`
always fails, even when gtest prints `nan` on both sides. Ask a yes/no question instead:

```cpp
EXPECT_TRUE(std::isnan(result));
```

### Why `std::isnan` and not `isnan`

`#include <cmath>` makes the names *available*; it doesn't bring them into scope. They're declared
in `namespace std`, the same way Python's `import math` gives you `math.isnan`, not `isnan`.
`using std::isnan;` is the `from math import isnan` equivalent. Bare `nan("")` compiled only because
`<cmath>` in practice also makes the old C `math.h` names available globally, and the standard
leaves that *unspecified*.

## Open

- A reading exactly at a buffer boundary, or `-1` → `length_error`: tested only by accident.
- NaN versus `optional` for "no readings" came up again in [36](36-maps-optional-and-the-copy-nobody-asked-for.md):
  two different kinds of "nothing" can reasonably get two different representations.

**Returns in:** week 7 (the simulator's sensors rejecting bad configuration), Part 12 (systems
engineering: failing fast at startup vs degrading at runtime).
