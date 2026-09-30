# 32 — Debugging an abort: read the backtrace first

**Week 5.** Syllabus item: *vector* (in depth: `size` vs `capacity`, what `operator[]` promises).
Also the week-3/4 debugger habit, applied to a real bug for the first time.

Prompted by the first under-full test on the ring buffer (N=3, push 2, expect `[r, s]`). It
aborted with:

```text
stl_vector.h:1128: ... operator[](size_type) ...: Assertion '__n < this->size()' failed.
```

Print debugging went nowhere ("i feel like a fool tryna print debug this"), and the guess was
that the bug was in `add_reading`. It wasn't.

Related: [22](22-parsing-input-that-fights-back.md) (first gdb, `catch throw`), [28](28-ring-buffers-and-class-invariants.md) (the ring buffer),
[29](29-testing-cpp-with-googletest.md) (gtest).

---

## Why prints failed here

`std::cout` is **buffered**: output collects in memory and is written out later. A failed assert
calls `abort()`, which kills the process **without flushing** that buffer. So the prints nearest
the crash, the ones that matter most, are the ones most likely to vanish.

Not a skill problem, a wrong-tool problem. If you must print near a crash, use `std::cerr`, which
is unbuffered. Better: don't print at all.

## The rule: after a crash, backtrace first

A debugger stops on the abort by itself (it's a `SIGABRT`); no breakpoint needed.

```bash
ASAN_OPTIONS=detect_leaks=0 gdb ./build/sensor_processing_test
(gdb) run
(gdb) bt            # the call stack at the moment of death
(gdb) frame N       # jump to a frame
(gdb) info locals
(gdb) p _imu_readings.size()
```

In VS Code: F5 on the test launch config, then the Call Stack panel.

The backtrace for this bug, trimmed:

```text
#0-#4  pthread_kill, raise, abort          <- libc: how it died
#5     __glibcxx_assert_fail               <- libstdc++: who noticed
#6     vector<IMUReading>::operator[] (__n=2)
#7     IMUBuffer::get_ordered_readings ()   imu_buffer.cpp:45   <- first frame that's yours
#8     ..._IMUBufferNotFullTest_Test::TestBody ()               <- who called it
```

**Read from the top, skip library frames, stop at the first frame you wrote.** That's the line.
One frame below is the caller. The bug was in `get_ordered_readings`, not `add_reading`. The
backtrace settled in seconds what guessing hadn't.

## The bug: where the oldest element is

The ordered read started at `(tail + 1) % N`. That's the oldest slot **only when the buffer is
full**. Under-full, `size() < N`, the oldest is at index 0, and `(tail + 1) % N` with tail=1, N=3
is 2, one past the end of a size-2 vector.

First fix: a branch (start at -1 if under-full, else at tail). Correct, but it felt gross, and the
feeling was right: two cases where one would do, and a `-1` sentinel flowing into unsigned
arithmetic that only works because `-1 + 1` hits 0 before the conversion.

Final fix: take the modulo by `size()`, not `N`.

```cpp
i = (i + 1) % size(_readings);
```

Under-full, tail is always the last element, so `tail + 1 == size()` and it wraps to 0. Full,
`size() == N`, so nothing changes. One expression, both cases.

It moves the danger rather than removing it: `% size()` on an empty buffer is `% 0`, undefined
behaviour. It's safe only because the loop guard (`0 < 0` is false) never enters the body. That
reasoning is invisible in the code, which is exactly why the **empty test** exists: it pins the
guarantee against a future refactor that computes the start index before the loop.

## `size` vs `capacity`

The next instinct was "how do I get the capacity, not the size." Two reasons that's a dead end:

| | `size()` | `capacity()` |
| --- | --- | --- |
| Means | elements that exist | memory allocated |
| After `reserve(3)` | 0 | **at least** 3, implementation's choice |
| Safe to index below it | yes | **no** |

1. `capacity()` isn't the buffer's N. The standard only guarantees it's ≥ what was reserved. The
   logical N is a member you own (`_buffer_size`).
2. `operator[]` requires `i < size()`. Slots between size and capacity are raw memory with no
   object in them. `_GLIBCXX_ASSERTIONS` exists to catch exactly that.

## Two ways to be lied to by your own build

Both happened during the `SensorBuffer<T>` refactor the same evening:

- **A stale binary.** The build failed (`main.cpp` still included `imu_buffer.h`) but running
  `./build/sensor_processing_test` directly showed "5 PASSED": the old executable. A green result
  means nothing unless the build that produced it succeeded. `set -e` in a build-then-run script
  gives you this for free.
- **A precompiled header.** `sensor_buffer.h.gch` appeared from running `g++` on the header. GCC
  prefers a `.gch` over the `.h` beside it, so header edits can be silently ignored. Never compile
  a header directly; delete any `.gch` you find.

## Open

- The order test ends with the tail at index 0 for both 4 and 7 readings into 3. No test ends with
  the tail mid-array (5 readings → `[t, u, v]`).
- `IMUBuffer(0)` / `SensorBuffer(0)`: `_insert_idx` does `% _buffer_size`, so a zero-capacity
  buffer is `% 0` on the first overwrite. This is the week's exceptions item.
