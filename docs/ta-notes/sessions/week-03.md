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
