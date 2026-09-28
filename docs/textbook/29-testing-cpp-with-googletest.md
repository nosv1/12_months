# 29 — Testing C++: GoogleTest, and why tests force a library

**Week 5.** Syllabus item: *Build a library, link it from another project*. Tests are the first
reason he has to do it. Also the repo convention: *tests from week 1*, which the C++ labs haven't
had until now.

Prompted by the question *"what's the convention for writing tests in cpp? we never covered it."*
Correct: weeks 3–4 had sanitizers and debuggers but no test suite.

Python counterpart: [11](11-writing-tests.md) / [14](14-partition-invariants-and-where-tests-go.md) (pytest, counting tests).

---

## No built-in runner

Python ships `unittest` and the ecosystem settled on `pytest`. C++ has neither. You pick a
framework:

| Framework | Notes |
| --- | --- |
| **GoogleTest (gtest)** | The default. ROS 2 uses it (`ament_cmake_gtest`). Learn this one |
| Catch2 | Popular, header-friendly, BDD-style sections |
| doctest | Very light, tests can live next to the code |

## The shape

```cpp
#include <gtest/gtest.h>

TEST(CounterTest, StartsAtZero) {      // (suite, name)
  Counter c;
  EXPECT_EQ(c.value(), 0);             // records failure, keeps going
}

TEST(CounterTest, IncrementAddsOne) {
  Counter c;
  c.increment();
  ASSERT_EQ(c.value(), 1);             // records failure, stops this test
}
```

- No `main()`. Link `GTest::gtest_main` and it provides one.
- `EXPECT_*` is the usual choice. Use `ASSERT_*` when continuing would crash, e.g. checking a
  pointer isn't null before dereferencing it.
- `ctest` (ships with CMake) runs everything registered.

## Getting gtest

It wasn't installed. Two routes:

- **`FetchContent`**: CMake downloads a pinned commit at configure time. What GoogleTest's own
  quickstart does, and what he chose. Same version on every machine.
- **`apt install libgtest-dev`** + `find_package(GTest)`: simpler, but whatever version the
  distro has.

His `CMakeLists.txt` follows the quickstart. CMake 3.28 warns about `DOWNLOAD_EXTRACT_TIMESTAMP`
(policy CMP0135) because `cmake_minimum_required(VERSION 3.16)` predates that policy (3.24).
Harmless here.

## Why tests force the library split

Everything currently compiles straight into one executable:

```cmake
add_executable(sensor_processing main.cpp imu_buffer.cpp imu_reading.cpp timestamp.cpp)
```

The test binary is a **second executable** that needs `IMUBuffer` too. Listing the `.cpp` files
twice compiles them twice and invites the lists drifting apart. The standard layout:

```text
library   imu_buffer.cpp, imu_reading.cpp, timestamp.cpp   → add_library
exe       main.cpp                                         → links the library
tests     *_test.cpp                                       → links the library + GTest::gtest_main
```

The pieces: `add_library`, `target_link_libraries`, `enable_testing()`, `include(GoogleTest)`,
`gtest_discover_tests`. That's the week's library checklist item, arrived at for a real reason.

State at time of writing: gtest fetched and wired, `ctest` reports *No tests were found*, library
not yet split. His to build.

## What to test first

The buffer's first test should be the one that would have caught the bug in
[28](28-ring-buffers-and-class-invariants.md): **N = 3, add four distinct readings, check which
three remain, and in what order.** Size alone passed while the wrong reading was being dropped.

Then the edges: empty, exactly N, 2N + 1 (wrapped more than once), N = 1.

Test only the **public interface**. A test that reaches into `tail_idx` breaks the next time the
ring is reorganised. A test that checks "the oldest three readings in order" survives it.

## The rules

- **gtest, via `FetchContent`, unless there's a reason otherwise.**
- **Code under test lives in a library.** Executables are thin shells around it.
- **A test must be able to fail.** Identical inputs and size-only checks can't.
- **Test the interface, not the internals.**

## Open questions

- `add_library` makes a static library by default (`.a`). What changes with `SHARED` (`.so`), and
  which stage of the build ([20](20-the-four-stages-of-a-build.md)) does each one affect?
- Should the sanitizer flags apply to the test binary too? Where do compile options belong once
  there's a library: on the library, or on each executable?
- `ctest` vs running the test binary directly: what does each give you?

## Where this returns

ROS 2 packages use exactly this layout via `ament_cmake` (`ament_add_gtest`), and CI runs
`colcon test`. The telemetry project's GitHub Actions workflow is the model for running these in
CI.
