# Circular imports and dependency direction

**Week 2** · deliverable requirement: "clean module boundaries" · [syllabus](../../SYLLABUS.MD#L132)

Came up moving `ParsedLine` into its own `parser.py`. Putting the "turn a `ParsedLine` into a
`Reading`" function in `validator.py` produced `ImportError: cannot import name ... (most likely due
to a circular import)` — "partially initialized module". The fix that shipped was making it a
`validate()` method on `ParsedLine`, which he didn't like.

---

## The one-sentence version

An `import` **runs the module** top to bottom, so if `a` imports `b` and `b` imports `a`, one of
them gets handed a module that has only run halfway.

The error is a mechanics problem. The *cycle* is a design signal.

## Mechanics: what `import` actually does

`from telemetry.validator import validate_velocity` does roughly this:

1. Is `telemetry.validator` already in `sys.modules`? If so, use it — **even if it hasn't finished
   running.**
2. If not, create an empty module object, put it in `sys.modules` *immediately*, then execute
   `validator.py` line by line, filling it in.
3. Look up `validate_velocity` on the module object.

Step 2 registering the module *before* running it is what makes cycles fail in a confusing way.

## The failure, traced

The layout that broke:

```text
parser.py     from telemetry.validator import validate_velocity, ...
validator.py  from telemetry.parser import ParsedLine
```

Running `uv run telemetry` → `cli.py` imports `parser`:

1. `parser` registered in `sys.modules`, empty. Line 1 of `parser.py` runs: import `validator`.
2. `validator` registered, empty. Line 1 of `validator.py` runs: import `ParsedLine` from `parser`.
3. `parser` **is** in `sys.modules` — step 1 put it there — so Python uses it. But `parser.py` is
   still stuck on its first import line. `ParsedLine` hasn't been defined yet.
4. `ImportError: cannot import name 'ParsedLine' from partially initialized module
   'telemetry.parser'`.

Note it's not "Python can't handle cycles." `import telemetry.parser` (the module, not a name from
it) often *succeeds* in a cycle and fails later, at attribute access. `from x import name` fails
early because it needs the name to exist *right now*.

## Three ways out

| Fix | What it does | Cost |
| --- | --- | --- |
| **Move the function** so only one module imports the other | Breaks the cycle | Requires knowing where it belongs — the actual design question |
| **Move the shared type** (`ParsedLine`) to its own module both can import, like `reading.py` | Both arrows point at a leaf | One more small module |
| **`if TYPE_CHECKING:` import** | Import only for mypy; with `from __future__ import annotations`, annotations aren't evaluated at runtime, so nothing runs | Works whenever the other module needs the name *only as a type hint*. Silences the symptom; the modules still depend on each other conceptually |

What shipped — a method on `ParsedLine` — is the first fix: validation-of-a-line moved into
`parser.py`, so `validator.py` never imports `parser`. It works. His discomfort is legitimate: a
data holder that also knows every validation rule has two jobs.

## The design signal: draw the arrows

Write each module and an arrow to what it imports. Healthy code usually looks like a pipeline or a
tree: **arrows point one way**, towards small modules with no imports of their own (`reading.py`
imports nothing from the package — that's why everyone can import it safely).

A cycle means two modules each need something from the other. Usually one of these is true:

- A function lives in the wrong module.
- A module is doing two jobs, and the two halves want different neighbours.
- There's a shared concept (a type) with no home of its own.

The README draws `parser → validation → analysis → report`. Code whose import arrows match the
architecture diagram is what "clean module boundaries" means concretely.

## Open question (his to answer)

After the move, `parser.py` contains both *parsing a line* and *the loop that runs the whole
pipeline over a file* (`parse_telemetry_lines`: splitting, robot grouping, calling validation,
recording bad rows). Which of those is "parsing"? Where the loop lives determines which direction
the arrows can point — and whether `validate` needs to be a method at all.

## Gotchas

- **`__init__.py` is part of the cycle too.** `telemetry/__init__.py` imports `cli`, so importing
  *any* `telemetry.x` first runs `__init__`, which imports `cli`, which imports everything. A cycle
  can appear through the package `__init__` without two modules naming each other.
- **Tests change import order.** A test that imports `telemetry.validator` directly starts the chain
  from a different place than the CLI does. A cycle can pass one way and fail the other.
- **Moving an import inside a function** also "fixes" it (runs at call time, after everything
  loaded). Legitimate for optional heavy dependencies — it's why `matplotlib` is imported inside
  `Robot.plot()` — but as a cycle fix it hides the problem.

## Where it returns

- **C++ (week 3+)** has the same problem with `#include`: headers including each other. The fix
  there is *forward declaration* (`class ParsedLine;`) — the direct cousin of `TYPE_CHECKING`. See
  [`#include` and namespaces](06-include-and-namespaces.md).
- **ROS 2 packages** declare dependencies in `package.xml`, and `colcon` refuses cyclic package
  dependencies outright. Same rule, enforced by the build tool.

Related: [packaging and `__init__.py`](05-packaging-and-console-scripts.md).
