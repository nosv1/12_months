# Packaging: `__init__.py` and console scripts

**Week 1** · checklist items: project layout (package vs script, `pyproject.toml`, imports that
work) and `argparse` / CLI design · [syllabus](../../SYLLABUS.MD#L106)

Came up when `uv run telemetry/` failed with `Permission denied`, and the `telemetry` command
declared in `pyproject.toml` turned out never to have worked.

---

## Reading the error

```
$ uv run telemetry/
error: Failed to spawn: `telemetry/`
  Caused by: Permission denied (os error 13)
```

`uv run X` means **"run the command `X` inside this project's environment."** It is not a path
argument. uv handed `telemetry/` to the OS as an executable; a directory isn't executable; the OS
returned `EACCES`. The trailing slash was the tell.

Three separate problems were stacked:

1. **Wrong directory.** The shell was at the repo root, which has no `pyproject.toml`. `uv run`
   finds the environment from the nearest project root — run from inside the project, or pass
   `--project <dir>`.
2. **Mistaking a path for a command.**
3. **The `telemetry` command didn't exist**, for reasons below.

## Two ways to run your code

```sh
uv run python -m telemetry.main data/sample_telemetry.csv output   # module form
uv run telemetry data/sample_telemetry.csv output                  # console script
```

`python -m pkg.mod` imports that module and runs it with `__name__ == "__main__"`, which is why an
`if __name__ == "__main__":` block fires.

A **console script** works completely differently — it never touches that block.

## Console scripts: what the line actually promises

```toml
[project.scripts]
telemetry = "telemetry:main"
```

Syntax is `command = "module:callable"`. It promises: *create a `telemetry` executable which
imports the module `telemetry`, looks up the attribute `main`, and calls it with no arguments.*

Three things must be true:

- The module path must import.
- The attribute must exist **on that module**.
- It must be a **callable**. Code in `if __name__ == "__main__":` is not callable — the script
  imports the module (so `__name__` is `"telemetry.main"`, not `"__main__"`) and the block never
  runs.

It was failing the last two: `__init__.py` was empty, and the entry logic lived in a bare
`__main__` block.

**Console scripts are generated at install time.** Editing `[project.scripts]` changes nothing
until the project is reinstalled (`uv sync`).

## The standard shape

```python
def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    ...

if __name__ == "__main__":
    main()
```

- The logic lives in a **function** — so a console script can point at it.
- The `__main__` block is a thin caller — so `python -m` still works.
- `parse_args(None)` reads `sys.argv[1:]`, but `parse_args(["data.csv", "out"])` doesn't touch
  `sys.argv` at all.

That last point is why the shape is standard: **`main()` becomes testable.** A test calls
`main(["data/sample.csv", str(tmp_path)])` directly — no subprocess, no shell. This is Week 2's
"separating I/O from logic" arriving early.

## What `__init__.py` is

**`__init__.py` *is* the package.** Not config, not a manifest. `import telemetry` executes
`telemetry/__init__.py`, and the resulting module object *is* `telemetry`. Whatever names exist in
that file become the package's attributes.

So `from telemetry.cli import main` inside `__init__.py` is exactly what makes `telemetry:main`
resolve.

(Historically the file also *marked* a directory as a package. Since Python 3.3, namespace packages
exist without one — but for an ordinary package you still want it.)

### What belongs in it

- **Re-exports that define the public API.** Callers write `telemetry.main` without knowing it
  lives in `cli.py`, so it can move later without breaking them.
- `__version__`, if you keep one.
- Ideally nothing else.

### What doesn't

- **Heavy imports.** It runs on *any* import of the package — even
  `from telemetry.reading import Reading`. Importing matplotlib here makes `--help` slow.
- **Side effects**: reading files, opening connections, calling `logging.basicConfig`. Importing
  should have no consequences.
- **Imports back into the package**, which is how circular-import errors start.

## The name collision

With `main.py` containing a function `main`, and `__init__.py` doing `from telemetry.main import
main`, the name `telemetry.main` means two things — a **submodule** and a **function** — and after
import the function shadows the submodule attribute. It works; it's also confusing.

Two normal ways out:

1. **Point the script at the module directly** — `telemetry = "telemetry.main:main"` — and leave
   `__init__.py` empty. The syntax accepts a dotted module path.
2. **Rename the module.** `cli.py` is the conventional name for the argparse-and-run layer. *(The
   choice made here.)*

## Two related things

- **`__main__.py`** is a different file with a different job: it makes `python -m telemetry` work
  (no `.main` suffix). Same pattern — a thin call to `main()`.
- **Implicit re-exports under `mypy --strict`:** `from x import y` in an `__init__.py` is flagged
  unless written `from x import y as y` or listed in `__all__`. mypy can't tell an intentional
  public re-export from a stray import.

## Dependency groups

```toml
[project]
dependencies = ["matplotlib>=3.11"]    # what users need to RUN it

[dependency-groups]
dev = ["mypy>=2.3", "pytest>=9.1"]     # what developers need to WORK on it
```

`mypy` in `[project] dependencies` makes a type checker a runtime requirement for everyone who
installs the package. Tools go in a dev group: `uv add --dev mypy`. `uv sync` installs the `dev`
group by default.

---

## Carry-forward

The same separation — importable library, thin entry point — is exactly how a ROS 2 Python package
is laid out (`entry_points` in `setup.py` → `console_scripts` → `ros2 run pkg node`). Week 11.
