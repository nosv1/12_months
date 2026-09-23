# TA notes

Claude's working notes, in the repo so any session on any machine can pick up where the last one
stopped. Not a progress log — that's [00-dashboard.md](00-dashboard.md) and
[background-threads.md](background-threads.md).

**At session start read this file only.** Open the others when the situation calls for them. At
session end: update *Where things stand* and *Next session* here, append to the week's session
log, commit as Claude. **Keep this file short** — when something here stops being needed every
session, move it out.

He reads these notes too. Write them so that's fine.

| File | Open when |
| --- | --- |
| [ta-notes/observations.md](ta-notes/observations.md) | pushback or confidence conversations; Sunday review |
| [ta-notes/telemetry.md](ta-notes/telemetry.md) | reviewing telemetry code; answering as the customer; Boss Fight #1 rules |
| [ta-notes/decisions.md](ta-notes/decisions.md) | before proposing a process, tooling, or convention change |
| [ta-notes/estimates.md](ta-notes/estimates.md) | giving any time estimate (log it); sign-off (fill actuals); Sunday review (ratios) |
| [ta-notes/sessions/](ta-notes/sessions/) | a thread from a past session comes back up (`week-NN.md`) |

---

## Where things stand

**Updated 2026-09-23 16:50.**

- Started Wed 2026-09-09. **43.16 h logged.** Three sessions today: 08:32–09:37, 10:58–13:07,
  15:29–16:49. **4.56 h today**, his longest day of the year.
- **`cpp_telemetry/` meets every SPEC item except the README.** Verified from a clean tree: zero
  warnings under `-Wall -Wextra`, 359 good / 3 rejected, and all nine per-robot stats exact against
  ground truth I computed independently from the CSV. The 3 rejects are the only 3 malformed rows
  and cover two distinct failure kinds.
- **Remaining: the README.** I wrote a skeleton (headings + prompts only, no content); the prose is
  his. He said he'd fill it next session. **Do not let week 3 be ticked until it exists.**
- **He updated the SPEC design answers post-hoc**, unprompted, at 16:47 — including where he changed
  his mind. That was the thing I asked for and the most valuable artifact of the day.
- **Total C++ to date: ~6.6 h over two days**, from `hello.cpp` to a six-TU CMake project. I said
  "six days ago" at one point; he corrected me. Third time-approximation miss on record — the
  standing instruction is to run `date`/check `git log`, not estimate.
- **My deliverable estimate was ~2x too high** (~6–9 h against 3.5 h actual). His own "the next
  steps seem simple" was accurate. Logged in `estimates.md`; the pattern of me over-estimating his
  C++ now has three entries.
- **Boss Fight #1 still ◐ on the dashboard**, still neither accepted nor disputed.

## Next session

1. **Log hours:** run `date` at the opener. Log any estimate given in `estimates.md`.
2. **README first**, then week 3 closes. Skeleton is at `cpp_telemetry/README.md`; he was resistant
   to the "what broke" section ("everything broke mate") and accepted the filter *what would break
   someone else, or what changed how you think*. Four items named for him: most vexing parse,
   unchecked `operator[]`, the identical-min/max/avg bug, and the latent `numeric_limits::min`.
3. **Latent bugs still in the code** — raise only if he doesn't put them in "Known issues":
   `numeric_limits<double>::min()` as the max seed (wrong for all-negative data; may be fixed since
   I flagged it), and `stod` accepting trailing junk (`"1.5kg"` → 1.5).
4. **Then tick week 3 on the dashboard and syllabus** — six checklist items plus a working
   deliverable with a README he wrote.
5. **Week 4 is memory and ownership.** Today set up three callbacks to use: `unique_ptr` (he reached
   for it for the wrong reason and changed his mind), lambda capture-by-reference dangling, and
   `-fsanitize=address` (already mentioned, not yet used).

## 2026-09-23 — what worked

**Third session, 15:29–16:49. Full day: 4.56 h.**

- **Verifying his "that completes the spec" caught two real bugs.** Clean build + run + ground truth
  computed independently from the CSV showed min/max/avg identical per robot. He'd have shipped it.
  Computing the oracle myself (20 lines of Python over the same CSV) is cheap and should be the
  default whenever he says a numeric deliverable is done.
- **Giving him ground truth rather than the diagnosis worked.** I printed the correct nine numbers
  and said "all three of yours equal the true minimum, that's systematic." He found the cause
  himself — "oh shit HOLD ON" — in under two minutes.
- **He took a design suggestion and improved on it.** I raised `optional<TemperatureAnalysis>` vs
  three `optional<double>` as a question; he switched, and also applied `const&` across both
  functions without being told twice.
- **"I despise writing a readme with what broke in it — everything broke mate."** Correct objection
  to a literal changelog. The reframe that landed: *what would break someone else, or what changed
  how you think* — four items, not forty. Reuse that filter.
- **He asked for a README template rather than grinding boilerplate at the end of a 4.5 h day.**
  Right call and the right thing to delegate; headings and prompts are scaffolding, the prose is the
  deliverable.
- **Third time-approximation miss.** Said "six days ago" for what was yesterday. He caught it
  immediately. `date` and `git log` exist; use them for every temporal claim, not just clock times.
- **Two of my earlier answers needed correcting in-session**: `file(GLOB)` (CONFIGURE_DEPENDS since
  CMake 3.12 fixes the staleness problem I'd cited) and the `kDataPath` naming inconsistency I
  introduced. Correcting myself promptly seems to cost nothing and he engages with the tradeoffs
  rather than just taking the ruling.


**Afternoon session, 10:58–13:07.**

- **He designed first, then coded, and it held.** The three SPEC questions got real answers over the
  haircut. His answer to #1 (vector of pointers) had the cost model inverted — "what if n is large"
  argues *for* contiguous values — and he took the correction without defending the original.
- **Strong types were his idea, from a throwaway line of mine.** I named them as an out-of-scope
  technique for the swapped-doubles hazard; he built them. First time this year he has taken a
  design idea and run with it unprompted. Worth noting on the confidence ledger.
- **`catch throw` landed the same way `breakpoint()` did.** He was hopping frames by hand and stuck
  on empty `info locals` in a constructor — `info args` was the missing half. The pdb parallel
  (textbook 19) is exact and worth naming to him next time.
- **He found the header-row bug himself** once pointed at the tool, and predicted the bad rows
  coming next. "lmao, it's the header line, forgot to skip."
- **Scope held once.** He wanted a config file; "write it down, don't build it" was accepted without
  argument. The SPEC's out-of-scope list is doing its job.
- **Frustration showed twice** — "im losing my mind" (most vexing parse) and "hard to find the
  error" (segfault). Both were genuinely hard first encounters, not him being slow. Said so, briefly,
  and moved to the mechanism rather than reassuring. Correct call; MVP defeats experienced people.
- **He called the stop himself** at 2h09m into the second session, with next steps clear. Good
  judgment, not a stall.


- **Predict-then-run, again, every time.** Every insight came from a wrong prediction written down
  first: the empty copy-constructor body, `Reading b = a` as a stored recipe, and `r = j` predicted
  as `1, 2, 2`. He is not precious about being wrong when the guess is on record. This is the format.
- **He called out my verbal tic** — "can't wait for you to say 'you're half right, but the bit
  you're wrong on will bite later'". He was right; I'd used that shape three times. Dropped it. Worth
  noticing that the framing had become a formula he could predict, which makes it stop landing.
- **Verifying his "fixed fixed" caught a miss.** He'd deleted the broken copy constructor rather than
  fixing it, which made the symptom go away and threw out the instrument. Reading the file took
  10 seconds. Keep doing this — two of Monday's misses were exactly this shape.
- **Checking GCC's actual output twice changed what I wrote.** The dangling reference segfaulted
  rather than printing stale bytes; the address turned out to be `0`, GCC having replaced the code
  outright. I had been about to tell him the stale-bytes story. Also verified the `discards
  qualifiers` wording rather than quoting from memory.
- **His Rust background is a live asset.** He reached for `mut` unprompted when explaining `const`,
  and the C++/Rust default inversion landed immediately. Use Rust as the bridge for ownership and
  lifetime in week 4; it will be cheaper than teaching from Python.
- **"goodnes so references are kinda dangerous"** needed correcting, not agreeing with. The hazard is
  lifetime, not references — a pointer dangles identically and can also be null. Left him with the
  parameter-safe / returned-or-stored-is-the-risk rule.

## Open, his — the week-2 `telemetry/` project (not the fight rebuild)

- **No test for the `-Infinity` fix.** The bug is fixed; nothing pins it. Needs a robot with zero
  valid readings — two lines of input. `json.dumps(report, allow_nan=False)` is the oracle.
- **§6's unrecognized-failure count is absent from the report.** Top-level keys are `robots` and
  `bad_readings` only. Requirements gap, not raised with him yet.
- `test_parsed_line_rejects` now pins the **count** (1 and 3) — verified to fail against a
  short-circuiting `validate_parsed_line`. Still only checks the *base* type, so three wrong error
  classes would pass. Naming the classes is the stronger version; told him, not blocking.
- **conftest runs the pipeline twice**: `sample_parsed_lines` and `sample_bad_readings` each call
  `get_parsed_lines_and_bad_readings` and discard half, so the partition test compares two
  independent runs. Passes by determinism, not construction. Told him 09-17.
- **`robot_id` has no validator at all.** Noticed 09-17, still not raised.
- Fixtures: `sample_valid_line` (09-18) is the **first hand-made input** in the suite. The rest are
  still the sample file. `parse_lines` has no test for empty or headerless input.
- Smaller, still open: `seed_max_temp` names the running value, not the seed; `list(lines)[0]`
  materialises the whole iterable; trailing `\n` in messages (arguably correct per §6); `"had a/an
  exception(s)"` log string; `",".join` with no space; `NotANumberError("", ...)` empty first arg;
  `UnknownError`/`UnrecognizedError` never raised; `build_report -> dict` untyped and untested;
  magic-number limits vs injected thresholds (same `20`/`60` duplicated in conftest); `readlines()`.
  Resolved 09-21: `pyproject.toml` description filled in; `matplotlib` and the
  dead `Robot.plot` removed.
- **Customer questions still unanswered**, §9: can columns be reordered; should a swapped pair flag
  both rows. His to ask.
- Resolved 09-18: `validate_timestamp_order` no longer returns a constant (`a57b142`, his), stray
  `Literal` import gone, `set_analysis_to_none` gone. **`py.typed` added and verified** — a consumer
  outside the tree now gets real type errors instead of `import-untyped`, and `uv build` ships the
  marker in the wheel without any `pyproject.toml` entry.

## Standing instructions

- **I log his hours.** Opener → `date`. Sign-off → `date`, append
  `YYYYMMDD HHMM - HHMM (N hours -- note)` under **Hours** in
  `docs/background-threads/week-NN.md`, bump **Hours logged** in `00-dashboard.md`, commit as
  Claude. No sign-off → ask for the end time next session. Don't guess.
- **Commits I make are authored as Claude** (`--author="Claude <noreply@anthropic.com>"`). Don't
  sweep his uncommitted edits into my commits. **Mechanism: stage explicit paths. Never `git add -A`
  or `git add .`** — a clean tree at session start is no guarantee it's clean twenty minutes later.
  Broke this 09-18 (swept his `test_validations.py` into a docs commit); he caught it.
- **Verify before advising** — his "done" and my own summaries both. Run it.
- **Never approximate a time.** Run `date`, every time. Said "~18:50" when it was 18:44 and burned
  six minutes of his evening on paper. He is pacing against these numbers. Told me 09-18.
- **Reformat any markdown freely**, his READMEs included. Formatting only; keep his wording.
- **`scratchpad.md` is background, not a prompt.** Read at session start; don't raise entries
  unprompted. Discuss when he asks.
- **Log every time estimate** in [ta-notes/estimates.md](ta-notes/estimates.md), his and mine, when
  given; fill actuals from `date`/commits at sign-off. Never revise an estimate after the fact.
  Asked for 2026-09-21: my numbers were priors, not measurements of him.
- **Textbook entry whenever a real lesson is given.**
- **I play the customer** for telemetry requirements questions — see telemetry.md.

## How to work with him — the short version

Lead with the answer. Mechanics get direct answers; design stays his. "Feels gross" from him is
usually right — ask him to name it. Name weak reasons plainly. Answer venting with accuracy, not
reassurance. One-word replies mean he's tired: park decisions. Details in
[observations.md](ta-notes/observations.md).
