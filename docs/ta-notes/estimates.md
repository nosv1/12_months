# Estimates vs actuals

Started 2026-09-21 at his request: *"idk if you actually have a grasp for time yet."* He's right. My
estimates are priors about generic work of that shape, not measurements of him. This file turns them
into measurements.

## Rules

- **Log every estimate when it's given**, with who gave it. His and mine are separate columns: his
  are a skill he's building (see [decisions.md](decisions.md)), mine are a tool he paces against.
- **Never edit an estimate after the fact.** The first number stands, even when it looks bad.
- **Actuals come from `date` and commit timestamps**, never from memory. Breaks excluded, same as
  the hours log.
- **Name the end state**, not the topic. "`json.tool` parses the installed tool's output from `~`",
  not "shipping".
- **Tag the kind of work.** Ratios are expected to differ by kind, so one global factor is wrong:
  `code-new` (from blank), `code-change` (modify existing), `debug`, `prose` (READMEs, requirements),
  `read` (absorb docs / textbook and use them), `ops` (install, ship, environment), `review`.
- **Ratio = actual / estimate midpoint.** Summarise per kind on Sundays in the table at the bottom;
  don't draw a conclusion from fewer than ~5 entries of a kind.

## Log

| Date | Task → end state | Kind | His est | My est | Actual | Ratio | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 09-12 | Tests: every bad row has a failing-if-broken test | code-new | 1h → 2h (added parser redesign) | — | not recorded | — | Scope merged with parser redesign and pipeline work across 09-12–09-17; no clean boundary. The "~3× out" in the 09-18 notes came from this period; its basis wasn't written down. |
| 09-17 | Multi-error collection shipped | code-change | 30–45 min | — | within estimate | ~1x | Per 09-18 session notes, once the 27-min `Literal[True]` detour is discounted. Commits 19:37–20:11 (34 min). |
| 09-19 | Boss Fight #1: §1–§8 from empty | code-new | 6h (earlier "4–6h or maybe 2h") | — | 9h38m | 1.6x | ~1h of header work beyond original scope; ~1.4x on like-for-like. |
| wk 2 | I/O separation | code-change | 1h | — | not recorded | — | Date given not recorded. Happened (textbook 09, 09-14) but not timed separately. |
| wk 2 | CI, once there's something worth running | ops | 1h | — | green 09-21 | — | Not comparable: I wrote the config, he reviewed. See the 09-20 review row. |
| wk 2 | README | prose | 0.5h | — | 62 min (done 09-21) | 2.1x | Same task as the 09-20 row below. |
| 09-20 | `telemetry/` README he'd hand a new teammate | prose | — | 45–60 min | 62 min (17:08–18:10, 09-21) | 1.2x | Also closes his wk-2 README row: 0.5h → 62 min, 2.1x. Included two review rounds from me. |
| 09-20 | Review my CI scaffold for `telemetry/` | review | — | 30 min | 19 min (18:20–18:39, 09-21, to first green run) | 0.6x | Five review questions: 4 answered, #4 (editable vs installed) answered well on the second prompt. Includes a failed run caused by my unverified `setup-uv@v10` tag. |
| 09-21 | Fight artifact shipped: installed tool's output parses as JSON from `~`, snapshot demo done | ops | — | 15 min | done before the estimate, untimed | — | Estimate was void: he'd already reinstalled after textbook 17 (09-20), checked the output in `less`, then uninstalled (shell history). I checked `uv tool list` and not history, so I gave him a task he'd already done. Snapshot demo (step 3) not done. |
| 09-21 | Review CI customer step; green run on push | review | — | 10 min | 6 min (18:46–18:52) | 0.6x | Two questions, both right in substance; corrected "more global PATH" and "separate machine". |
| 09-22 | Week 3 complete: all six syllabus checklist items | read | — | 11–13h | open | — | Given at the start of week 3, before any C++ was written. Sequenced as five steps of ~2h each. |
| 09-22 | Week 3 steps 1–4 (build stages, headers/TU/ODR, CMake, ctors/dtors) | read | — | ~7.5h (2 + 2 + 1.5 + 2) | 2.05h | 0.27x | **My estimate was 3.7x too high.** Caveat: the session was heavily guided — I diagnosed the ODR bug from his files, supplied out-of-line member syntax, and found the file-scope `static`. Not a clean measurement of him working alone. Step 5 (references/pointers/values, const) untouched, and no C++ written outside a toy. |
| 09-23 | Week 3 step 5: references/pointers/values + `const` correctness understood | read | — | 60–90 min | 63 min (08:32–09:35) | 0.84x | Predict-then-run throughout; wrong predictions on copy-ctor signature (recovered), `Reading b = a` semantics, and `r = j` rebinding. Guided, but he wrote every line and made every prediction unaided. |
| 09-23 | `cpp_telemetry/` running to spec: parses the CSV, partitions bad rows, per-robot min/max/avg matching an independent oracle | code-new | "the next steps seem simple" (13:07, for the second half) | "several evenings" (~6–9 h) | 3.5 h (10:58–13:07 + 15:29–16:47, minus README) | ~0.45x | **My estimate was ~2x too high**, second time this week I've over-estimated guided C++. His "seems simple" was for grouping + stats + output and came in at ~1.3 h — accurate. **Mislabelled as `code-new`; this was a port, not blank-page work.** His correction, 09-23: *"we're most likely fast today because the telemetry stuff is basically 'solved' in my head... there is no decision making... we're writing clean code without having to think through the whole problem."* Correct, and it was the SPEC's explicit design — a known domain so the difficulty lands on the language. So this measures C++ mechanics, not design. Do not read it as evidence about generative speed. |

## Working hypothesis — his, 2026-09-22

> *"there wasn't design decisions it was follow instructions, so we're fast at guided sessions, and
> slow at design, in relative terms"*

The five timed entries split cleanly and do not overlap:

| Character of the work | Entries | Ratio |
| --- | --- | --- |
| Reactive — review, follow instructions, absorb | `review` ×2, `read` ×1 | 0.27–0.6x |
| Generative — blank page, decide the shape | `code-new` ×1, `prose` ×1 | 1.6–2.1x |

So **`kind` is doing more work than any global factor**, which is what the column was added to
detect. Read Sunday's table through this split rather than averaging across it; a single ratio for
"him" would be meaningless at a ~3x spread.

Two consequences worth holding:

- **The slow hours are the valuable ones.** Guided work is cheap per hour *and* cheap in value —
  nothing in it was his to invent. The expensive hours are where the interface gets decided. Pace
  should be judged on what fraction of a week was generative, not on hours logged.
- **A guided session can be made arbitrarily fast by me doing more of it.** 0.27x on 09-22 partly
  measures how much I supplied. Speed on reactive work is not evidence about the boss fight.

## Ratios by kind

Fill on Sundays. Too few entries to say anything yet (2026-09-21). Split by reactive/generative
before averaging — see the hypothesis above.

| Kind | Entries | His median ratio | My median ratio |
| --- | --- | --- | --- |
