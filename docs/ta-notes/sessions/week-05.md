# Week 5 — session log

## 2026-09-26 17:16–18:35 — `labs/w05-sensor-processing/` design

Started week 5 in the same sitting, on "still feeling good... if we're building." It turned out to be
mostly design talk, which he found tiring: *"there's a huge amount of decisions to make and im tired
of making them."* Stamina numbers from him, logged in observations.

- **"Im always on the receiving data side, never the sender."** The DS → robotics shift in one line:
  he'd been modelling Sensor → Buffer as text → parse, like telemetry. Once he saw he defines the
  reading type, `Reading` base, "parse", and `vector<vector<double>>` all fell away.
- **Decisions, his:** IMU first; ring buffer, keep newest N; Processor integrates accel → velocity,
  Statistics shows drift against simulated truth; no base class; `IMUBuffer` now,
  `SensorBuffer<T>` when `TempReading` arrives *this week* (templates tick depends on it).
- **Slicing** reasoned correctly ("buffer knows ... because we have to know the size"), not run.
- **"It's just a wrapper for a vector"** — pushed back: the capacity/drop-oldest policy is the class.
  Open: where that lives, and the cost of erasing element 0.
- Headers reviewed twice; I reviewed a stale copy once and told him to fix what he'd already fixed.
  **Re-read files before every review.**
- I wrote "18:2x" once. Broke the never-approximate rule; it was 18:26.

## 2026-09-27 07:25–08:24 — oral explain-backs, car ride

Voice-to-text from the car, on the way to a bowling tournament. His idea: "utilize the textbook a bit
more", since he rarely opens it. **Correction owed and given:** I had told him entries end with
explain-back questions. They don't. They end with Open questions / Where this returns. Offered to
add an explain-back section to each entry; not agreed yet, so not done.

**Format that worked:** one question at a time, one retry with a hint, then the answer. He asked
partway through for **concept questions, no code**, because code is hard to dictate. Keep that for
any future phone session.

Ten questions, results:

| # | Entry | Result |
| --- | --- | --- |
| 1 | 25 `std::move` | Zero instructions: **held from last week.** Still thinks it returns "what x holds"; it's x as `T&&`. Called a moved-from object "null/garbage"; it's valid-but-unspecified. Said "copy and delete" for a move. **Re-check.** |
| 2 | 20 linker | Linker: right. "Where the call is looking is missing": right. Attributed pasting the includes together to the linker (that's the preprocessor). |
| 3 | 24 RAII | Leak: right. Called it a "dangling reference" (wrong term). Unwinding: got it on the retry. Reasoned on his own that a raw pointer can't free because it doesn't know if it owns the memory. Good. |
| 4 | 16 sentinel | Solid. Reminded him there's still no test for `-Infinity`. |
| 5 | 23 `explicit` | **Real gap.** Didn't know one-argument constructors are implicit conversions. Answer given; his restatement afterwards was correct and enthusiastic ("that was hot"). **Re-check cold.** |
| 6 | 21 reference assignment | Had "r is i with a new name" and didn't trust it. Got `r = j` → `i = j` after. Says "points to" for references. |
| 7 | 26 use-after-free | Tools and the glibc overwrite: right. Missed "the pointer is unchanged and the memory is still mapped, so no crash". |
| 8 | 11/14 counting tests | Solid: conservation vs classification. |
| 9 | 07 circular imports | Cycle and direction: right. Didn't know the leaf-module fix; asked, it landed ("obviously..."), then blamed himself for being lazy. Corrected that: it's the normal first layout. |
| 10 | 02 falsy return | Solid. |

**Pattern:** the ideas are there; **the vocabulary slips** (dangling vs leak, "points to" vs
"refers to", what `move` returns). That vocabulary is what interviews test. Next session, cold, no
hints: `explicit`, what `std::move` returns, leak vs dangling.

Not asked yet: all four stages of a build end to end, `raise X from Y`, why I/O belongs at the edges.

**Hours:** 0.98, logged. He said to log it how I wanted. Start is the session's creation time (12:25 UTC)
and end is the `date` output when he called the break (13:24 UTC), both converted to CDT (-0500).

## 2026-09-27 evening — aerospace conversation (car ride, not work time)

No hours. He asked about adding aerospace. My answer: fold it into existing weeks, don't add a
Part or fly a physical drone in Part 6. Mapped the hooks: wk 7 MAVLink, wk 8–9 attitude + cascaded
PID, wk 12 ArduPilot/PX4 SITL in Gazebo, wk 18 EKF, wk 20 3D planning / min-snap, wk 40 ArduPilot
PR, wk 46 capstone. If aerial becomes his lane, Part 10 is the trade, decided on Part 5 evidence.
Then the Space Force / SpaceX question; details in observations.md 09-27. **No syllabus change.**

## 2026-09-27 17:21–18:35 — Sunday review, IMUBuffer ring-buffer design (break)

**Sunday review:** both remote PRs merged cleanly into `dev`. **Textbook 27 (TVC) is stranded**
on `origin/claude/aerospace-exploration-b3o9z5` (`91d8bc6`), pushed after PR #2 merged. His to
PR or cherry-pick. **Build log Built/Broke/Learned/Stuck empty weeks 2–5**; only my Hours lines
exist. Bench kit (by wk 6, i.e. by 10-03) raised for the first time. He went straight to code.

- Mechanics answered directly: C++17 has no `operator<<` for `duration`; `.count()` +
  `duration_cast`; `steady_clock` epoch is unspecified (time since boot), deltas are what it's for.
- **IMUBuffer v1 review** (built with `-Wshadow`, runs): public vector bypasses the policy;
  `size > MAX` then push holds 101 (told him it's off by one, asked him to predict 150 adds before
  running); `erase(begin())`; non-static `const u_long` member (non-standard type, per-instance,
  kills copy assignment); `int` return always 0; `auto const` copies in the loop; parameter shadows
  member.
- Taught: gtest shape, why tests force the library/exe/test split (= the week's library item; CMake
  is his); gtest **not installed**, recommended FetchContent. `struct` vs `class` is default access
  only. Public vs private: private by default, public is a promise, test through the interface.
- **Ring buffer, his reasoning:** saw that array + shift is still O(N) → offered linked list (valid;
  rejected on per-reading allocation, cache, node overhead) → reading 5 goes in slot 1, but modelled
  slots as pointing to each other → `% N` → "just the oldest" (insufficient) → head + next-write.
  **Open: head == tail when empty and when full.** Asked twice, not answered yet.
- **Decision, his:** capacity passed to the constructor → `std::vector` sized once. Flagged: the
  `IMUReading` has no default ctor trap (`vector(n)` vs `reserve`), capacity 0 → mod by zero
  (constructor can't return an error code — the exceptions item), don't make capacity `const`.
- Owed: textbook entry on C++ testing layout + class/access (said "at sign-off"). Number it 28;
  27 is on the branch.
- He has an untracked `sensor_processing_test.cpp` — hasn't shown me.

## 2026-09-27 20:30–21:19 — ring buffer, first implementation (sign-off)

Start is his ("came back at 2030"). He merged PR #3, so textbook 27 is on `dev`.

- "Why head again?": to *read* oldest → newest after a wrap; writing only needs tail. Any two of
  {head, tail, count}. **His pick: tail + count, count = `size()`** (reserve + push_back). Flagged:
  don't read N from `capacity()`; `size_t` subtraction wraps.
- "add readings works then": **it didn't.** `tail_idx = size()` after push_back ("next") vs
  `(tail_idx + 1) % N` in the else ("last written"). N=3, r s t u → u overwrote s. Output was
  size-only with identical readings, so nothing could show it. **He fixed it** (set tail before
  push_back). Correct by my trace; **no test yet.**
- Wanted one branch instead of push_back/`[]`; floated a map. Map has the default-ctor trap too.
  Pre-fill → filler choice (default reading vs `optional`); he then weighed the size compare cost.
  Told him it's negligible, keep what he has, write the test. He took it.
- **gtest wired via FetchContent** (his, quickstart). `sensor_processing_test.cpp` is one
  `#include`; ctest: no tests. No `add_library` yet. Both uncommitted.
- Committed `8e540a6` (his). Stopped: "too tired to continue."
- Textbook 28 (ring buffers + class invariants) and 29 (gtest + library split) written.

Still open from the review: `uint tail_idx = -1`; `IMUBuffer(0)` → `% 0`; private setter in the
ctor instead of an init list; `const size_t&`; `auto const` loop copy; `add_reading` private;
non-`const` `to_string`; `Timestamp` switched to `steady_clock::duration` (asked what it bought).
