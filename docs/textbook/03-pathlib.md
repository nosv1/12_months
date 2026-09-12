# pathlib

**Week 1** · checklist item: `pathlib` · [syllabus](../../SYLLABUS.MD#L110)

Came up replacing the `os.path` calls in the telemetry CLI's `report()`.

---

## The one-sentence version

`pathlib` gives you a **`Path` object** that knows it is a filesystem path, instead of a **string**
that happens to contain one.

That's the whole idea. Everything else follows from it.

## Why a string is the wrong type

`os.path` is a library of *string manipulation functions*. `os.path.join("output", "output.json")`
returns a string, and a string has no idea what it is. Consequences:

- **The knowledge is scattered** across `os.path`, `os`, `shutil`, and `glob`. "Does it exist" is
  `os.path.exists`; "make it" is `os.makedirs`; "list it" is `os.listdir`; "delete the tree" is
  `shutil.rmtree`. Four modules, no discoverability.
- **No type safety.** Nothing stops a path being passed where a robot ID goes — both are `str`, so
  mypy cannot help.
- **You do the separator bookkeeping.** Forget it and you get `outputoutput.json`; hardcode `/` and
  you have made a platform assumption.

With `Path`, operations are **methods on the thing itself** and the type says what it is.

## Mechanics

```python
from pathlib import Path

output_dir = Path("output")
```

### Joining uses `/`

```python
output_dir / "output.json"          # Path('output/output.json')
```

`Path.__truediv__` is overloaded. Correct separators on every platform, and it reads like a path
rather than a function call.

### Questions are methods

```python
p.exists()      p.is_file()      p.is_dir()
p.mkdir(parents=True, exist_ok=True)
p.unlink()                              # delete a file
p.iterdir()                             # list a directory
p.glob("*.csv")     p.rglob("*.csv")    # rglob is recursive
```

### Parts are properties

Where it decisively beats string slicing:

```python
p = Path("data/sample_telemetry.csv")
p.name                    # 'sample_telemetry.csv'
p.stem                    # 'sample_telemetry'    <- no extension
p.suffix                  # '.csv'
p.parent                  # Path('data')
p.parents                 # all ancestors
p.with_suffix(".json")    # Path('data/sample_telemetry.json')
p.resolve()               # absolute, symlinks resolved
```

`p.stem` is how you name an output after its input without writing `s.rsplit(".", 1)[0]`.

### Reading and writing

```python
p.read_text()                  # whole file as str; also read_bytes()
p.write_text(content)          # also write_bytes()
with p.open("w") as f: ...     # identical to open(p, "w")
```

`read_text` is for when you don't need streaming. The telemetry parser takes an open file object
and iterates it, which is the right call for data files of unknown size.

## Applied to the telemetry CLI

Before:

```python
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
...
with open(os.path.join(output_dir, "output.json"), "w") as output:
```

After:

```python
output_dir.mkdir(parents=True, exist_ok=True)
...
with (output_dir / "output.json").open("w") as output:
```

### The LBYL → EAFP connection

`if not exists(): makedirs()` is **LBYL** — look before you leap — and it has a race: between the
check and the create, another process can create the directory, and the `makedirs` raises.

`mkdir(exist_ok=True)` is **EAFP** — easier to ask forgiveness than permission — the same shape as
the `try`/`except` in the parser. The principle generalises: **don't ask whether an operation will
fail; attempt it and handle the failure.** The check-then-act version is both longer and wrong.

See [exceptions and error boundaries](02-exceptions-and-error-boundaries.md).

### Parse at the edge

`type=Path` on an `argparse` argument converts at the boundary, so the path is a `Path` from the
moment it arrives rather than a string converted later, deeper, maybe twice.

The habit: **parse at the edge, so the interior of the program only handles real types.** Same
instinct as a validator returning a `float` rather than a validated string — and the same reason
re-converting downstream is a smell.

## Gotchas

- **`Path` is not a `str`.** `open()`, `json.load()`, `shutil`, and most of the stdlib accept it
  via the `os.PathLike` protocol, but `"prefix" + path` fails, as does anything doing string
  operations on it. Use `str(p)` only where text is genuinely required.
- **An absolute right-hand side wins:** `Path("/home/chris") / "/etc"` is `Path('/etc')`, not a
  join. Bites when joining user input.
- **`exists() == False` is not proof you can write there** — permissions, or a race.
- **`WindowsPath` vs `PosixPath`:** `Path()` instantiates whichever suits the current OS. Directly
  relevant here — WSL now, native dual-boot around week 8, same repo on both. Use `Path`, never a
  hardcoded `/` or `\`.
- `Path.cwd()` and `Path.home()` replace `os.getcwd()` and `os.path.expanduser("~")`.

## When `os` is still right

`pathlib` covers paths, not everything filesystem-shaped. Still `os`/`shutil` territory:
permissions (`os.chmod`), process-level things (`os.environ`), recursive delete
(`shutil.rmtree`), and copying (`shutil.copy`, which accepts `Path` happily).
