# 28 — Ring buffers: move the index, not the data

**Week 5.** Syllabus item: *`vector`, `unordered_map`, `string_view`, `optional`* (`vector` in
depth, `optional` raised). Also introduces `class`, access control, and invariants, which the
syllabus assumes rather than lists.

Prompted by `labs/w05-sensor-processing/`: an `IMUBuffer` that keeps the newest N readings. It
began as a public `vector` with `erase(begin())`, and went through array, linked list, map, and
back to `vector` in one evening.

Follows [24 — RAII](24-raii-and-ownership.md), where the class existed to guarantee a rule
(the memory gets freed). The buffer is the same kind of class with a different rule.

---

## The first version, and what it got wrong

```cpp
struct IMUBuffer {
  std::vector<IMUReading> imu_readings;
  const u_long MAX_READINGS = 100;
  int add_reading(const IMUReading& imu_reading);   // always returns 0
};

int IMUBuffer::add_reading(const IMUReading& imu_reading) {
  if (size(this->imu_readings) > this->MAX_READINGS) {
    this->imu_readings.erase(this->imu_readings.begin());
  }
  this->imu_readings.push_back(imu_reading);
  return 0;
}
```

"It's just a wrapper for a vector" was his description the day before. The reply: **the capacity
policy is the class.** Without it, this is a `vector`. Everything wrong above is about that policy:

1. **Anyone can break it.** `imu_readings` is public, so `buf.imu_readings.push_back(x)` skips the
   check entirely.
2. **The check is off by one.** `>` then push means it holds N + 1. (Predict the size after 150
   adds before running it. That's the first test.)
3. **Dropping the oldest is O(N).** More on this below.
4. `const u_long` as a data member: `u_long` is a POSIX typedef, not C++ (`std::size_t` is the
   standard size type); non-`static`, so every buffer stores its own copy; and a `const` member
   **deletes copy assignment**, so `a = b;` stops compiling.
5. An `int` return that is always `0` tells the caller nothing.

## `struct` vs `class`, and what goes public

**The only difference is default access.** `struct` members are public until you say otherwise,
`class` members private. Everything else, constructors, methods, inheritance, is identical.

The convention is about intent:

- **`struct`**: plain data, no rule to protect. `Acceleration` has three doubles and any values
  are legal.
- **`class`**: there is an **invariant**, a statement that must be true after every public call.
  For the buffer: *size never exceeds N, and the oldest reading is the one dropped.*

```cpp
class Counter {
 public:                       // interface first: what readers care about
  explicit Counter(int start);
  void increment();
  int value() const;           // const: doesn't modify *this

 private:                      // implementation last
  int count_;                  // trailing _ = member (Google style); m_count also common
};
```

Python enforces none of this. `_name` is a request. C++ makes it a compile error.

**How to decide what's public:**

- **Private by default.** Public is a promise: once other code uses it, changing it breaks that
  code. Private can be rewritten freely. That's exactly what let the buffer switch from
  `erase(begin())` to a ring without touching any caller.
- **Data: could a caller set this to a value that breaks the object?** `head_ = 57` on a 4-slot
  buffer, or a 101st `push_back`: yes, so private. `x_mps2 = -3.2`: no, so plain `struct` is fine.
- **Functions: public is *what* it does, private is *how*.** "Add a reading" is what. "Advance an
  index with wraparound" is how. Callers should not know it's a ring.
- **Tests go through the public interface.** If a test needs private access, the interface is
  missing something, or the test is pinning implementation.

## Why dropping the oldest costs O(N)

A `vector` is contiguous: element `i` is at `data + i`. Erase element 0 and every other element
moves down one slot to keep that true. N moves per insert once full.

His next step, correctly: *"even if we make it an array tho, we'd need to shift the whole contents
over."* Right. The container isn't the problem. **The assumption that the oldest is at index 0
is.**

## Detour: linked list

*"linked list"* is a real answer. Removing the head and appending the tail are both O(1). It loses
here on three counts:

1. **One heap allocation per reading.** At 100+ Hz that's 100+ `new`/`delete` a second, forever.
   Robotics hot loops avoid allocating because allocation takes unpredictable time.
2. **Cache.** Nodes are scattered, so walking them is a pointer chase and probably a cache miss
   per step. The Processor will walk the whole buffer.
3. **Overhead.** `next` + `prev` is 16 bytes on a ~56-byte reading.

The list gets O(1) by giving up contiguity. The ring gets O(1) and keeps it.

A `map<size_t, IMUReading>` came up later for the same reason and loses the same way, plus one
more: `map::operator[]` default-constructs a missing value, which `IMUReading` can't do.

## The ring

Bend the array into a circle. When it's full, the new reading overwrites the oldest, and "oldest"
moves forward one slot. Nothing shifts.

```text
4 slots, readings 1..6

after 4:   [1][2][3][4]     oldest = slot 0
after 5:   [5][2][3][4]     oldest = slot 1
after 6:   [5][6][3][4]     oldest = slot 2
```

Three things he had to get right, in order:

- **Slots don't point to each other.** His first description was "slot 4 now points to slot 1".
  In an array the next slot is always `i + 1`. The only non-obvious neighbour is the wrap from the
  last slot back to 0, and that's computed: `(i + 1) % N`.
- **One index isn't enough.** "Just track the oldest": after 2 readings the oldest is slot 0, and
  it's also slot 0 when empty, with 1 reading, and full. Those need different write positions.
- **Head and tail alone are ambiguous.** Empty: head = tail = 0. Add N readings: tail wraps to 0.
  Full looks the same as empty. Any two of **{head, tail, count}** determine the third, and the
  pairs with **count** resolve it.

His pick: **tail + count, with count taken from `vector::size()`.** Fill with `reserve(N)` +
`push_back`, and `size()` counts 0, 1, … N and then stays at N once writes switch to `[i] =`.

Two cautions that came with it:

- **Don't read N back from `capacity()`.** `reserve(n)` guarantees *at least* `n`. Store N.
- **`size_t` is unsigned.** `tail - count` with tail 1 and count 4 isn't −3. It wraps to about
  1.8 × 10¹⁹. Compute an "oldest" index so that subtraction can't go negative.

## The bug in the first ring

Two branches, one index, two meanings:

```cpp
if (size(v) < N) {
  v.push_back(r);
  tail_idx = size(v);              // means "next slot to write"
} else {
  uint i = (tail_idx + 1) % N;     // treats it as "slot last written"
  v[i] = r;
  tail_idx = i;
}
```

N = 3, add r, s, t, u. After t, `tail_idx` is 3. u goes to `(3 + 1) % 3 = 1`, overwriting **s**,
and r (the actual oldest) survives. The program printed `size: 3 of 3`, which is correct and
proves nothing. All four readings also had identical values, so no output could have shown it.

His fix: set `tail_idx` *before* the `push_back`, so it means "slot last written" in both
branches. u then lands in `(2 + 1) % 3 = 0`. Correct by trace. **Not yet by test.**

**Two branches weren't the bug.** He wanted one ("I wish I didn't have to use push_back if the
vector wasn't full"). Pre-filling N slots gets you one branch, but then `size()` is N from the
start, you track count yourself, and something has to fill the empty slots:

| Filler | Upside | Risk |
| --- | --- | --- |
| Default-constructed `IMUReading` | Plain `vector<IMUReading>` | Zeros look real (a sensor in free fall reads about that). A count bug integrates fake data silently, like the week-2 `-Infinity` sentinel |
| `std::optional<IMUReading>` | An empty slot can't pass for data; `.value()` on one throws | Larger slots, unwrap on every read |

With a correct count, the filler is never read. The choice is what happens when count is wrong.

The `size() < N` comparison, by the way, costs roughly nothing: one integer compare the branch
predictor learns to always guess right. The `%` next to it costs more, and that's a few
nanoseconds. Choose between designs on which makes the index mean one thing, not on speed.

## The rules

- **A class exists to hold an invariant.** If nothing can break, it's a `struct`.
- **Private by default; public is a promise.**
- **O(1) drop-oldest: move the index, not the data.**
- **Any two of head, tail, count; include count or you can't tell empty from full.**
- **One variable, one meaning.** If a name means different things in two branches, one of them is
  wrong.
- **Output that can't distinguish right from wrong isn't evidence.** Distinct values, and a test
  that checks *which* readings remain.

## Open questions

- What does a reader get? The Processor needs oldest → newest. A copy, a `const` reference, an
  iterator pair, a callback? Each exposes a different amount of the ring.
- `IMUBuffer(0)`: the mod divides by zero. A constructor has no return value, so what does it do
  with a bad argument? (The *exceptions vs error codes* item.)
- `Timestamp` moved from `steady_clock::time_point` to `steady_clock::duration`. A `system_clock`
  duration now compiles in its place. What was gained?
- When `TempReading` arrives, `IMUBuffer` becomes `SensorBuffer<T>`. What changes about where the
  code lives? (Templates are header-only.)

## Where this returns

Every sensor driver and ROS 2 subscription queue has one of these: a "keep last N" QoS depth is a
ring. Week 6 makes it harder: a producer thread writing tail while a consumer reads head is the
classic lock-free single-producer / single-consumer queue, and the head/tail/count question comes
back with atomics.
