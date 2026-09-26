# Week 3 — C++ that compiles

Session notes moved out of [ta-notes.md](../../ta-notes.md) once they stopped being needed every
session. Newest last.

---

## 2026-09-22 — what worked

- **He named the failure mode himself:** *"this was a teacher showing commands and their outputs and
  a student being like mmm yes, interesting, it's hard to make sense of it without a reason to make
  sense of it."* Correct, and it was the turning point of the session. Demos → a build he had to
  make work. Everything good after that came from tasks with a predict-before-you-run step.
- **"mmmm interesting" is his tell for passive watching.** He used the phrase twice; the second time
  naming it back to him converted the moment into a 30-second action. Watch for it.
- **Predict-then-run is the format that works.** Every real insight tonight came from a wrong
  prediction: the constructor undefined reference, `static` hiding the linker error, `goodbye c`
  never printing, LIFO destruction order. He is not precious about being wrong when he wrote the
  guess down first.
- **Environment papercuts: just fix them.** The Windows Caps Lock OSD was Logi Options+, found in
  30 seconds via `powershell.exe Get-Process` from WSL. He responded "omg tysm". That is the
  correct division of labor and he feels it.
- **I over-estimated the clock three times** (19:05, 19:15 when it was 19:09). Run `date`. Every
  time. Standing instruction, broken three times in one session.

## 2026-09-24 — README close-out, `explicit`

**16:11–~17:00, then dinner.**

- **I overwrote his live edits.** He was saving README changes 16:16–16:26; I did a full-file Write
  from a 16:13 read. Recovered from VS Code local history
  (`~/.vscode-server/data/User/History/`), nothing lost. Rule: **re-read immediately before any
  full-file write to a file he has open**, and prefer `Edit` for his files.
- **My opening review list was partly stale** — three items copied from last night's notes that he
  had already fixed. He asked "have you re-read readme since?" Same failure shape as the date
  misses: trusting my notes over the artifact.
- **Wrong prediction, best moment of the day.** "i hope that doesn't compile" → "well shit, it
  compiles and runs no problem." Then put `explicit` on `Reading` first — wrong place, found with a
  one-question hint. → textbook 23.
- **I pushed an explain-back three rounds; he ended it: "mate, we're moving on."** Then apologised
  for being blunt — he shouldn't have to. His one-liner was imprecise but his fix was correct and
  in the right place; the second round was already enough. Cap explain-backs at one retry.
- **The `_GLIBCXX_ASSERTIONS` reproduction worked**: comment out the size check, predict, run. He
  decoded the message with prompts (got `row` and the `<` rule; said `data[i]` for the operator
  until `_Tp` contradicted it). It also exposed that textbook 22 had quoted the wrong message.

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
