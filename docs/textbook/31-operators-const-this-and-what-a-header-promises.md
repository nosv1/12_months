# 31 — Operators, `const this`, and what a header promises

**Week 5.** Syllabus items: *`vector`* (its `==`), *Build a small library*
(declarations vs definitions across files). Also revisits `const` correctness from
[21](21-values-references-pointers-and-const.md) and the one-definition rule from
[20](20-the-four-stages-of-a-build.md).

Prompted by writing the first order test for `IMUBuffer` in `labs/w05-sensor-processing/`. Four
errors hit in a row, each one teaching one rule.

---

## 1. `EXPECT_EQ` needs `==`, and `vector` already has one

`EXPECT_EQ(a, b)` compiles to `a == b`. `std::vector` defines `==` as same length and each
element equal to the one at the same position, **in order**. So comparing two vectors of
readings works with no loop, provided the element type has `==`.

Sets were the Python instinct ("in python we compared sets"). A set discards order, and order was
exactly what the test was checking (`get_ordered_readings()`). Use a list in Python, and a vector
here.

C++ doesn't generate `==` for your structs. (C++20 can with `bool operator==(const X&) const =
default;`, but the project is on C++17.) An `IMUReading ==` has to be written, and it recurses:
it needs `==` on `Timestamp`, `Acceleration` and `Gyro` too.

On floating-point equality: exact `==` is correct here, because the values are copied in and read
back, never computed. The "never `==` doubles" rule is about computed values. It will apply to the
running average: use `EXPECT_DOUBLE_EQ` or `EXPECT_NEAR`.

## 2. "No match for `operator==`" when one exists

```
error: no match for 'operator==' (operand types are 'const IMUReading' and 'const IMUReading')
```

```cpp
bool operator==(const IMUReading& other);          // what was written
bool operator==(const IMUReading& other) const;    // what was needed
```

The error states it outright: **both** operands are `const`. `vector`'s `==` compares through
const references. `const IMUReading& other` covers the right-hand side. The left-hand side is
`this`, and only a `const` **after the parameter list** promises not to modify it. A non-const
member function can't be called on a const object, so the candidate was silently discarded and
the compiler reported no match.

It cascades. Inside a `const` member function every member is const, so the `==` calls on
`timestamp`, `accel` and `gyro` need `const` versions too. The same applies to `to_string()`. Put
`const` on the declaration **and** the definition, or they're two different functions.

Rule of thumb: any member function that doesn't modify the object gets `const`. Leaving it off
doesn't show up until someone holds a `const&`, and then it shows up everywhere at once.

## 3. `operator<<` can't be a member

With no way to print an `IMUReading`, gtest dumped raw bytes on failure:

```
56-byte object <8D-BC 9A-4D BB-05 00-00 | 00-00 00-00 00-00 10-40 | 00-00 ... >
```

That's still readable in a pinch: 8 bytes of timestamp, then `accel.x` as a little-endian double.
`00 00 00 00 00 00 10 40` is `0x4010000000000000`, or 4.0, so that's reading `u`.

gtest prints any type that has `std::ostream& operator<<(std::ostream&, const T&)`. That has to
be a **free function**, because for a member operator the object is always the **left** operand,
and in `std::cout << reading` the left operand is the stream. A member of `IMUReading` would only
make `reading << std::cout` compile. Being a free function, it takes both operands explicitly and
returns the stream, so that `<<` chains.

`friend` declared inside the class is still a free function. `friend` only grants access to
private members. For a struct with public fields it isn't needed.

## 4. Defined, but invisible, then defined twice

The first attempt put the definition in `imu_reading.cpp` only. It compiled and linked, and gtest
**still printed bytes.** The test file is its own translation unit and sees only what its
`#include`s declare. gtest checks whether an `operator<<` exists for the type, finds none, and
falls back quietly. There's no error, because the fallback is by design, and no link error,
because nothing calls the function.

The next attempt, with the body in the header, gave "multiple definition" at link time: every
`.cpp` that includes the header compiles its own copy.

The split that works is the same one every member function already uses:

| Where | What | How many allowed |
| --- | --- | --- |
| `imu_reading.h` | **Declaration**: signature ending in `;` | As many as you like (every includer) |
| `imu_reading.cpp` | **Definition**: signature plus `{ body }` | Exactly one in the program (ODR) |

The declaration only needs the type `IMUReading` to be known, so it goes below the struct. It
doesn't need `to_string()` to exist yet; only the definition calls that. (`inline` is the one
exception that allows a body in a header, and it isn't needed here.)

## What came out green, and what it hides

The order test passed once `get_ordered_readings()` walked from the oldest slot and wrapped with
`%`. It also caught a return of the raw vector instead of the ordered one: "this is why we have
tests."

Open: both tests overfill the buffer. The case of a buffer not yet full (capacity 3, two pushes) is
untested. Trace the first `i` against `size()` before writing it.

## Where this returns

- Every message type you'll compare or log in ROS 2. Generated message structs come with `==`,
  and your own types won't.
- `const` member functions are the norm in any library API you'll read; `rclcpp` is full of them.
