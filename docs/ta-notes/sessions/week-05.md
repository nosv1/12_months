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

## 2026-09-28 16:31–18:29 — bench kit, library split, first real tests (sign-off)

- **Bench kit.** SSH'd to `chris@rpi` (Windows `ssh.exe` only; WSL key not authorized): **Pi 4 Model
  B Rev 1.1, 4 GB**, Raspberry Pi OS trixie. Pi 5 dropped → syllabus-revisions §14 (`0a6f967`).
  Reviewed his Amazon cart. Open on it: confirm motor variant has the encoder (he saw magnet disk +
  6-pin cable, looks right; check cable ends); **DRV8825 min VMOT 8.2 V** so the AA pack can't run
  the NEMA 17 → add **12 V 2–3 A adapter + barrel-to-terminal**, drop AA holder + NiMH; **100 µF
  cap**; one ESP32 3-pack not two; ICM-20948 not on Amazon → **Adafruit/SparkFun order: ICM-20948,
  Qwiic/STEMMA-to-jumper cable, MAX31855, K-type probe**; soldering iron (unanswered). He said
  "startin to feel overwhelmed" — shrank it to a list, parked it. **Not ordered. Due 10-03.**
- **Week-5 end state, finally.** His version was weeks 5–7 (threads, backpressure, new sensor
  without touching core). Mapped each to its week. Accepted: *a gtest pushes known IMU and temp
  sequences through the same `SensorBuffer<T>` (library linked from exe + test), a processor
  computes a statistic, test asserts the exact value; capacity 0 has a defined, tested failure.*
  "Temperature threw me off" — it was his own 09-26 plan.
- **Templates vs abstract classes** taught (textbook 30). Explain-back: said "size unknown". Half
  right; corrected with the same-`sizeof` counterexample. Unrelated types is the root.
- **`add_library`** his. Put flags `PRIVATE` on the lib → ASan undefined refs at the exe link.
  Explained compile vs link jobs of `-fsanitize`; he chose `INTERFACE`. Good.
- Tests: first capacity test "no output" = only built; running showed it failing (readings never
  added). Then: renamed `get_readings` → `get_ordered_readings` (answered the order question by
  naming it). `operator==` without `const` → he learned `const this` ("const on the right side").
  `operator<<` defined in .cpp only → invisible to gtest; body in header → multiple definition;
  then declared correctly. Implemented ordered read; **both tests green**, all committed by him
  (`061790f`..`0476f5c`).
- **Review finding, not yet told as a fix:** `get_ordered_readings` starts at `(_tail_idx+1) % N`
  — for an under-full buffer (N=3, push 2) that's index 2 of a size-2 vector → `_GLIBCXX_ASSERTIONS`
  abort. Asked him to write the under-full test first.
- Tooling (mine, `050bfe1`): gdb launch configs + Debug build/test tasks. He'd meant his own
  `debug.sh` (build + run both); suggested shebang + `set -e`.
- Asked for gtest fixtures → explained `TEST_F`, protected members, init in declaration (no default
  ctors), fixed timestamps. He paused: **"remind me of this when we resume."**

## 2026-09-29 18:00–19:33 — fixtures, the under-full bug, `SensorBuffer<T>` (sign-off)

- Did not come back 09-28 evening. Nothing to log for it.
- **Asked "are we not ahead anymore?"** Yes, ~11 days ahead: calendar week 3 day 7, curriculum week
  5. Lead comes from ~18 h/week against a 10–12 budget, not faster weeks. My "tight but doable"
  measured against the 7-day week length, which isn't a deadline. **Relabelled the opener field.**
- **Fixtures:** generic `Point`/`PathTest` example. He converted his tests, fixed timestamps, later
  moved the buffer into the fixture too.
- **Under-full test aborted** (`operator[]` `__n < size()`). "Feel like a fool tryna print debug":
  abort doesn't flush `cout`. Taught backtrace-first; I reproduced but didn't name the line. He
  found it in `get_ordered_readings` (he'd guessed `add_reading`). Asked for `capacity()` — told
  why not (not N; `[]` needs `< size()`). "0 holds the oldest" — his. Branch fix with `-1`
  sentinel, "gross flag"; hinted `tail + 1 == size()` when under-full → he found `% size()`.
  Empty case: reasoned the loop guard protects `% 0`; wrote the test anyway.
- **My error:** said the 7-into-3 test wasn't saved without reading the file. He'd edited the
  order test in place. Read before claiming.
- **Templates:** "which parts depend on IMU?" → "none, just holding readings". Conflated with
  textbook 30's `unique_ptr<Shape>`; separated. Requirements: said "a copy" for all three; split
  into copy-construct / copy-assign / `==` (tests only). Wrote bodies as `SensorBuffer<IMUReading>::`,
  then `SensorBuffer<TempReading>::` — **same misconception twice**; landed on "bodies once, in `T`"
  on the third pass. Also hit: stale binary showing PASSED over a failing build; a `.gch` from
  compiling the header. "Where does TempReading get declared" → at the use site.
- **`TempReading` read as "temporary".** My shorthand. Renamed `TemperatureReading`.
- TemperatureReading review: .cpp not in `add_library`, `operator<<` declared not defined,
  tautological test, CapacityTest lost overflow. He fixed all; replaced the tautological test with
  a temperature **order** test. 7 green. Commits `b6d638f`, `d60126c`, `40926aa`, `39a8cb6`, his.
- Textbook 32 (backtrace, size/capacity, stale build) and 33 (class templates) written.

Open: no test ends with tail mid-array; `_`-prefixed test locals; `uint` (POSIX, not standard) for
indices; `const size_t&` params; bench kit; build log.

### After sign-off, 19:33–19:42 (chat, not logged as hours)

- **"Raspberry Pi robotics kit"** from his brother. Bench kit: no — hobby car kits lack quadrature
  encoders and hide the hardware behind a vendor library, so the week-9 PID step response can't be
  done. Week-22 robot: maybe, if it has encoders, room to self-mount RPLIDAR/camera/IMU, is driven
  by his own code, and fits $250–400 incl. the Pi/IMU he has. TurtleBot 4 as the reference point
  (over budget, integration pre-done). **He used TurtleBots in the grad robotics class** — that's
  the Gazebo exposure; résumé-worthy. Offered to vet a specific kit when he names it; decision is
  Part 5.
- **Soldering makes him nervous** ("am i gonna have to solder too???"). Accurate answer: probably
  one row of header pins on the MAX31855; IMU is Qwiic, no soldering; motor/driver via cable and
  breadboard. Week 22 may add battery/motor leads. Recommended temperature-controlled iron +
  practice kit, first 20 joints on the practice board. Ventilation, stand, wash hands if leaded.
- Bench-kit energy is low ("will try to find the mental energy... soon tm"). Most decisions are
  already made (09-28 list); remaining work is cart edits.

## 2026-09-30 (Wed, off day) — 07:58–08:54, 09:15–11:36 (3.28 h)

Week 5 went from 2.0/5 to 4.5/5. Only `string_view` + `optional` remain.

- **`SensorBuffer(0)`**: found the `% 0` himself, and **argued fail-fast in the ctor unprompted**.
  Picked `length_error`, then `domain_error`; I rejected both, and he pushed back hard ("MATE you
  said… pick one that seemed right"). **He was right**: I invited picking by name, then graded by
  convention. Owned it. Landed on `invalid_argument`. He wrote the throw before the test (not test
  first), then replaced both old capacity-0 tests with a single `EXPECT_THROW` and argued correctly
  that the add case was unreachable.
- **`mean`**: proposed an `Analysis` struct holding a `TemperatureAnalysis` struct; took the
  namespace instead. NaN on empty (his choice over `optional`). Hit NaN ≠ NaN, then `std::` on
  `isnan`. ODR: body was in the header, moved to `analysis.cpp`. Loop → `accumulate` with
  `double{0}` (he avoided the int trap). Spotted the `get_ordered_readings` copies himself.
- **Consumer**: needed the configure command; quoted `add_subdirectory` args. Include dir first
  put in the consumer (worked "by luck"), moved into the library as `PUBLIC`. Said
  `CMAKE_SOURCE_DIR` would be the consumer's **before** hitting it. Did the `include/`+`src/` move
  himself with `git mv`. Explain-back of PUBLIC/INTERFACE was **backwards** (INTERFACE = "only
  local"); corrected with a table and a deliberate break — saw the error. "Consumer only needs the
  library bit" → EXCLUDE_FROM_ALL + PROJECT_IS_TOP_LEVEL; target-order errors while moving blocks.
  The ASan/-Wall flags ended up inside the guard; told him -Wall needn't be. Unresolved.
- **Robot + map**: wanted a map of mixed sensor types → laid out variant / base+`unique_ptr` /
  map-per-type, flagged Boss Fight #2, **no design input**. He scoped down: "was just tryna find a
  reason to use a map." `operator[]` default-ctor error → `emplace`. `optional<SensorBuffer>`
  returned a copy → I listed 3 options; he, low on patience, chose a reference via `at` + throw.
  Made member functions `const`. 11 tests green, all committed by him (`980c806`…`2c6e1bd`).
- **My errors today**: said "it's 09:52" without running `date`; told him to wrap a declaration
  in parens inside `EXPECT_THROW` (invalid C++); the "think back to INTERFACE" hint sent him to
  the wrong line. All three corrected when he hit them.
- Tooling (mine, `5432980`): compile_commands.json + cpptools setting after IntelliSense lost
  `include/`. Per-week path in `.vscode/settings.json`.
- Mood: "woke up on wrong side", "one day i'll understand this shit", "running outta patience".
  Answered the second with the specific list of things he derived unaided today.
- **His critique, unanswered**: mixing app requirements with checklist learning is annoying —
  "learned optional then ditched it cause irrelevant." I agreed it's partly my framing and
  proposed: count learned-not-used, do short standalone drills for items the app doesn't need.
  **He hasn't said yes.** Don't record it in decisions.md until he does.
- Textbook 34, 35, 36.

## 2026-10-01 (Thu) 16:11–16:38, 0.45 h

- **Opened on motivation, not code.** Less enthused than weeks 1–2. Data: hours logged every day
  09-10 → 09-30, no off days, ~19 h/week vs the 10–12 plan. The 09-12 "revisit around week 4"
  decision triggered. Fri 10-02 off (bench kit order only), back Saturday.
- **His diagnosis, and it's partly mine**: "always something to fix" — untagged critique lists read
  as mandatory, and he can't stop at a half-fixed state; C++ is "a dark tunnel, what else is there
  before I'm out." Answered with the remaining map (wk 5 string_view, wk 6 threads, wk 7 sockets +
  Docker + BF2, wk 8 hardware). Adopted **fix now / noted / taste**, taste kept out of chat (he
  said taste still lands as fix-now). He'd already dismissed the telemetry open list himself.
- **string_view**: linter spoiled the error; predicted no-matching-call at `at()`. Why explicit:
  "not actually a string" → corrected to ownership/copy cost. Copy count: right for the
  caller-holds-a-string case, missed the literal tie. Reverted to `const std::string&`. Done.
- Drill proposal: **yes**, after sign-off. In decisions.md. string_view closed by this; optional by 09-30.
