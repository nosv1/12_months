# Textbook

Lessons from TA sessions, written up so they're referenceable later — and so the explanation
outlives the chat window it was given in.

**Not** a progress log ([00-dashboard.md](../00-dashboard.md)), **not** a build log
([background-threads.md](../background-threads.md)), **not** session state
([ta-notes.md](../ta-notes.md)). This is the *why it works that way* material.

New entry whenever a real lesson gets taught in a session. Numbered in the order they were
learned, not in syllabus order — the sequence is the actual path through the year.

---

## Contents

### Part 1 — Reactivation (weeks 1–2)

| # | Entry | Week | Came from |
| --- | --- | --- | --- |
| 01 | [Logging](01-logging.md) | 1 | Replacing `print` diagnostics in the telemetry CLI |
| 02 | [Exceptions and error boundaries](02-exceptions-and-error-boundaries.md) | 1 | The falsy-return bug that silently dropped a parked robot's readings |
| 03 | [pathlib](03-pathlib.md) | 1 | Replacing the `os.path` calls in the CLI's `report()` |

---

## Conventions for entries

- Filename `NN-kebab-case-title.md`, numbered in learning order.
- Open with the week, the syllabus checklist item it satisfies, and what prompted it.
- Lead with the mental model, then the rules, then the mechanics. Concepts before syntax.
- Keep the **actual bug or question** that prompted it. A rule without the failure it prevents is
  forgettable; "this is why the average velocity was wrong" is not.
- Record the open questions and the tradeoffs, not just the answer. The decision is the learning.
- Cross-link related entries.
- Note where the idea returns later in the curriculum.
