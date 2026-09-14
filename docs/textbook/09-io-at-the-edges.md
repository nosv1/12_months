# I/O at the edges, and naming the thing in the middle

**Week 2** · deliverable requirement: "tests from week 1" / "clean module boundaries" ·
[syllabus](../../SYLLABUS.MD)

This started as a complaint about tests:

> "problem is if stuff is still moving it's annoying writing and rewriting tests"

True, but not uniformly true — and the exception is the whole lesson. Two of the three tests in
`test_validations.py` had survived a parser redesign, a circular-import fix, and the stage
restructure with zero rewrites. The third couldn't even be finished:

```python
def test_all_defects_caught():
    cur_dir = Path.cwd()
    telemetry_main(cur_dir / "data/sample_telemetry.csv", cur_dir / "output")
    # work in progress
    pass
```

It ran the entire program and asserted nothing. It passed whether the analyzer found 8 defects,
2, or none — including through a regression the day before that silently dropped truncated rows.

---

## The one-sentence version

**Churn cost tracks how much structure a test reaches through, not how much testing you do.**
Push I/O to the edges and the logic into a pure middle, and the tests that matter stop breaking
when you refactor.

## Why one test churned and two didn't

| Test | Reaches through | Rewrites so far |
| --- | --- | --- |
| `validate_velocity("0.0") == 0.0` | one pure function | 0 |
| `validate_velocity("nan")` raises | one pure function | 0 |
| `test_all_defects_caught` | argparse → file read → whole pipeline → JSON layout → disk | never finished |

The first two test a pure function against a settled contract. The third reaches through
everything, so *any* change anywhere breaks it.

The instinct "don't write tests while the design is moving" is the right observation with the
wrong conclusion. The question isn't *when* to test, it's *what has stopped moving.*

## Something has always stopped moving: the requirement

> Given `sample_telemetry.csv`, all 8 defects get reported.

That sentence was true before the stage redesign and after it. It will be true after the stage
*order* is fixed. It is the sentence Boss Fight #1 is graded against — the only thing that says a
blank-page rebuild is correct rather than merely running.

Requirements are stable. Structure is not. **Test the requirement, and don't let the test reach
through the structure to do it.**

## The test was failing because of the design, not because of testing

Try to write that test and you hit this:

```python
def main(telemetry_file_path: Path, output_dir: Path) -> None:
```

`None`. The only way to see what it computed is to `mkdir`, run it, read `output.json` back off
disk and parse it — so a test of a *stable requirement* gets dragged into coupling with an
*unstable output format*. That's why it stayed `pass`.

A test that's hard to write is evidence about the code, not about testing. Here it was pointing
at `main` doing four jobs:

1. build config (`defined_warnings`)
2. read a file — **I/O in**
3. parse → group → validate → analyze — **pure computation**
4. write JSON and print — **I/O out**

(3) is untestable because it's welded between (2) and (4).

## "Why would main ever return anything?"

A fair objection, and correct. An entry point returning a value so a test can inspect it is a
test warping the design.

The resolution is that `main` shouldn't return anything *and* shouldn't compute anything. Returning
`None` was never the problem; doing four things was. Compare with the split already made one level
up: `cli()` does argparse and hands off, `main` does the work. Same move again, one level down.

```text
cli()        argv → calls main.                 I/O (arguments)
main()       reads file, calls core, writes.    I/O (disk). Returns None. Thinks about nothing.
<the core>   data in → data out.                No Path. No mkdir. No print. Pure.
```

This has a name: **functional core, imperative shell.** Every outer layer is thin and dumb; the
core is pure and therefore trivially testable. It's the same property that kept
`validate_velocity`'s tests alive through three redesigns.

The test calls the core. It never touches disk, never sees the JSON layout, doesn't care what the
output directory is called, and does not break when the stage order changes — because the stage
order is *inside* the core.

## Naming a composition

Entry 08 gives verbs for naming a *stage*. It doesn't cover naming the function that runs all of
them, which is the thing you actually need a name for:

> **A stage is named for what it does. A composition is named for what it returns.**

Stages get verbs: `parse`, `validate`, `group`, `aggregate`. The composition gets its name from
its return type. Returns a `Report` → `build_report`. Returns an `Analysis` → `analyze`.

**Don't call it `pipeline`.** That fails 08's own test: it names the mechanism, not what the
caller gets. Every one of these is a pipeline; `run_pipeline(lines)` says nothing a reader
couldn't already see.

Two conventions, both common:

- **Module named for mechanism, function named for domain.** `telemetry/pipeline.py` containing
  `analyze_telemetry()` is idiomatic. The module may say "this is the wiring"; the function must
  say what you get back. So `pipeline` isn't a bad name — it's a bad *function* name.
- `run()` as the composition works in an orchestrator module (`pipeline.run`, `app.run`) only
  because the module name carries the domain. Standalone in `utility.py` it means nothing.

### When the name won't come, the return type is undecided

The composition here resisted naming because it hands back two loose values with no shared type —
an analysis dict and a separate `bad_readings` list. "The function that returns an analysis dict
and also a list of bad readings" has no name because it isn't one thing yet.

**Name the return type and the function names itself.** This is 08's "a name that won't come is a
design signal," one level up: there it meant a module doing several jobs, here it means a return
shape not yet decided.

Corollary: `utility.py` is the same failure. It means "things." Fine as a staging area for
functions that have no home yet, not as a destination.

## Extracting stages is not extracting the composition

A half-finished version of this split produced a test that passed and was still wrong:

```python
# main.py                          # and, character for character, test_all_defects_caught
telemetry_lines = read_file(telemetry_file_path)
parsed_lines, bad_readings = parse_lines(telemetry_lines, headers_count=1)
parsed_robots_dict = group_robots(parsed_lines)
robots_dict = get_robots_dict(parsed_robots_dict)
analysis_dict = get_analysis_dict(robots_dict, defined_warnings)
```

The *stages* had moved to `utility.py`, but the *assembly* still existed only inside `main`. So
the test wired up its own copy. Fix the stage order now and you either edit both or the test
silently keeps checking the old order and passes.

That is exactly the churn the session opened by complaining about, reconstructed by hand. **A
duplicated pipeline body in a test means the composition hasn't been extracted yet.**

## Test data location: cwd vs `__file__`

```python
cur_dir = Path.cwd()                          # before
file_dir = Path(__file__).resolve().parent    # after
```

Both couple the test to something. They are not the same grade of problem:

- `Path.cwd()` breaks when you `cd`. Invisible, environment-dependent, happens on an ordinary
  Tuesday, gives no hint why.
- `Path(__file__).parent` breaks when you move files in the repo — a deliberate act, performed
  while looking at the thing you're breaking.

Trading a runtime-environment coupling for a repo-layout coupling is strictly better. The
idiomatic next step is a `conftest.py` at the project root: pytest auto-discovers it, so *its*
location is definitionally the test root rather than a guess, and tests take the data directory
from it as a fixture.

The better question is whether the test needs a file at all. Once the core takes lines rather than
a path, a unit test hands it a list of strings it wrote itself and the path question disappears.
Keep one end-to-end test that reads the real sample file — that one legitimately needs the path,
because checking the analyzer against the actual data *is* its point.

## Gotchas

- **`breakpoint()` left in a test.** Locally it drops you into pdb and looks like a hang you can
  escape. In CI it blocks with no output until the runner times out, often 6 hours later.
  `PYTHONBREAKPOINT=0` disables it process-wide, which is worth knowing but is not the fix.
- **A test with no assertion is a smoke test wearing a correctness test's name.** It proves the
  code doesn't crash. It cannot fail for a wrong answer. `test_all_defects_caught` passed straight
  through the dropped-truncated-row regression.
- **Untested code rots silently, and `__main__` blocks are untested code.**
  `output_dir = (file_dir / "../output").mkdir(parents=True, exist_ok=True)` binds `None`, because
  `mkdir` returns `None`. No test covered that path and the console script doesn't use it; mypy
  was the only thing watching (`[func-returns-value]`). Anything below `if __name__ == "__main__":`
  gets no test coverage by construction — keep it to one line.

## Open questions

- Does the core return one value or two? The current pair (`analysis_dict`, `bad_readings`) has no
  shared type, and the test has to re-add counts across two different shapes to check one number.
- Does the core take `list[str]`, or a path? Lines make it pure and make the data-file coupling
  optional.
- Once serialization lives on the far side of the core/shell line, the two carried-over questions
  — `-Infinity` for a robot with no good readings, and who turns a `BadReading` into JSON — are
  both output-format questions with exactly one place left to answer them. Does that settle them?

## Where it returns

- **Week 11, ROS 2 nodes:** a node's callback is an imperative shell — it receives a message and
  publishes one. Keeping the logic in a plain function the callback calls is what makes a node
  testable without a running ROS graph. This is the single most common thing done badly in ROS
  codebases.
- **Week 12+, CI:** the pure core is the part that can run on a machine with no data files, no
  display and no hardware.
- **Boss Fight #1:** rebuild from a blank page. The layering — argv at the edge, disk at the edge,
  pure in the middle — is the part to re-derive, not the function names.

Related: [pipeline stages](08-pipeline-stages.md),
[exceptions and error boundaries](02-exceptions-and-error-boundaries.md),
[circular imports and dependency direction](07-circular-imports.md),
[packaging and console scripts](05-packaging-and-console-scripts.md).
