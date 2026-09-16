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
| 04 | [Commits: what goes in one, and how to split them](04-commits.md) | 1 | Nine modified files that seemed impossible to split |
| 05 | [Packaging: `__init__.py` and console scripts](05-packaging-and-console-scripts.md) | 1 | `uv run telemetry/` → `Permission denied`, and a script entry that never worked |
| 06 | [`#include`, namespaces, and `using namespace std`](06-include-and-namespaces.md) | 1 | Deleting `#include <iostream>` from the first hello world |
| 07 | [Circular imports and dependency direction](07-circular-imports.md) | 2 | "Partially initialized module" moving validation out of `ParsedLine` |
| 08 | [Pipeline stages: order, provenance, and streams](08-pipeline-stages.md) | 2 | A module that wouldn't name, a rebuilt row printed as `'202Z,...'`, and a timestamp parsed twice |
| 09 | [I/O at the edges, and naming the thing in the middle](09-io-at-the-edges.md) | 2 | A test that asserted nothing, and no name for the function that runs the pipeline |
| 10 | [Exception taxonomies: base classes, blind excepts, and where to fail loud](10-exception-taxonomies.md) | 2 | A registry that never matched, a blind `except` hiding dead NaN detection, and a `del` that stopped running |
| 11 | [Writing tests: what a test claims, and why counting isn't one](11-writing-tests.md) | 2 | `assert 9 == 8`, a tautological accepts test, and a count that balanced while the wrong rows were blamed |
| 12 | [`raise X from Y`, and letting a linter teach you](12-exception-chaining-and-lint-rulesets.md) | 2 | Bugbear's B904 acted on backwards, and an editor linting rules the terminal had never heard of |

---

## Conventions for entries

- Filename `NN-kebab-case-title.md`, numbered in learning order.
- Open with the week, the syllabus checklist item it satisfies, and what prompted it.
- Lead with the mental model, then the rules, then the mechanics. Concepts before syntax.
- Keep the **actual bug or question** that prompted it. A rule without the failure it prevents is
  forgettable; "this is why the average velocity was wrong" is not.
- Record the open questions and the tradeoffs, not just the answer. The decision is the learning.
- Cross-link related entries.
- No personal pronouns. Keep the specific bug and the specific project; write the lesson
  impersonally or in the second person.
- Note where the idea returns later in the curriculum.
