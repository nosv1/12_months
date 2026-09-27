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
