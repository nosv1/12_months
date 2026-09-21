# Installed artifacts are snapshots

**Week 2, boss fight #1** · deliverable requirement §8: *"it installs, and installing it puts a
command on the path"* · [syllabus](../../SYLLABUS.MD)

Two failures from the same blind spot, four hours apart.

First, a package directory named `01_telemetry`. `uv init` in a directory called `01-telemetry`
derives the project name from the directory, and the build backend derives the module name from the
project name. Nothing complained until the first `import`, which failed as a **syntax** error —
Python identifiers cannot start with a digit, so the parser rejects `import 01_telemetry` before any
import machinery runs. No `sys.path` change can fix a name the grammar won't accept.

Second, and worse: after `uv tool install`, the command on the path printed this —

```python
{'robots': [{'warnings': [], 'rejected_readings': [...]}], 'unrecognized_failures': 0}
```

— while the same code run from the project venv printed this:

```json
{
    "robots": [ ... ],
    "unrecognized_failures": 0
}
```

Single quotes. `None` where `null` belongs. Not JSON, so §7's dashboard cannot parse it. The source
tree was correct. The installed artifact predated `print_report` and nobody had reinstalled it.

---

## The one-sentence version

**An installed package is a copy taken at a moment in time. The source tree you are editing and the
command on your path are two different programs until you make them the same one.**

---

## Three ways code becomes importable

Worth being able to name these, because they fail differently.

| Mechanism | What it does | Sees your edits? |
| --- | --- | --- |
| `cd` into the directory | CWD lands on `sys.path` | Yes, and only from there |
| Editable install | Drops a `.pth` file naming your `src/` | Yes, immediately |
| Regular install | **Copies** the built wheel's contents into a venv's `site-packages` | **No** |

`uv sync` gives the third for dependencies and the second for your own project — which is why
`pytest` picked up every edit instantly and lulled the fight into thinking the artifact was current.
`uv tool install` gives the third, deliberately: a tool is supposed to be a frozen thing that
doesn't break when you refactor.

That property is the whole point of it, and it is exactly what bit here.

---

## The rules

1. **When the requirement is "it installs and runs," the artifact under test is the built wheel,
   never the source tree.** A green test suite says the source is correct. It says nothing about
   what is on the path.
2. **Reinstall before you claim §8 passes.** `uv tool install --reinstall .`, or uninstall and
   install clean. A stale tool is silent — there is no warning that the copy has drifted.
3. **Verify from a directory that is not the project**, with no venv activated, typing the command
   by name. `cd ~ && toolname /abs/path/to/file.csv`. Anything less tests something easier than
   what the customer does.
4. **Check the output, not just the exit code.** This failure exited 0. The report was wrong in a
   way only a parser would notice, which is precisely the reader §7 names.
5. **Module names are identifiers; distribution names are not.** `telemetry-boss-fight` is a fine
   name to publish under, and an impossible name to import. `[tool.uv.build-backend] module-name`
   decouples them. Entry-point strings in `[project.scripts]` are dotted **import paths**, so they
   inherit the identifier rule too.

---

## The procedure: ship it, then test what you shipped

The rules above, in the order you actually do them. Added 2026-09-21. The rules alone weren't
enough to tell him *how* to ship and test the fight.

```bash
# 1. Ship: from the directory holding pyproject.toml
uv tool install --reinstall .       # --reinstall: take a fresh snapshot even if one exists
uv tool list                        # confirm the name and version on the path

# 2. Test as the customer: somewhere else, no venv, command by name, absolute path in
cd ~
deactivate 2>/dev/null              # harmless if nothing was active
which <command>                     # should be ~/.local/bin/<command>, not a .venv path
<command> /abs/path/to/sample.csv | python3 -m json.tool
echo "exit: ${PIPESTATUS[0]}"       # the tool's exit code, not json.tool's
```

**Pass** means `json.tool` pretty-prints the output *and* the tool's exit code is the one the
requirements specify. A `JSONDecodeError` from `json.tool` means the output isn't JSON, and that's a
real §7/§8 failure, not a tooling problem.

**Every time the source changes, step 1 runs again before anyone says "it works."** Without that,
steps 2 onward test an old copy.

To remove it: `uv tool uninstall <name>`. To see where the copy lives: `uv tool dir`.

---

## Why a smoke test is the real fix

Reinstalling by hand works exactly as long as you remember. The durable version is a test that
shells out to the installed command:

- run the console script by name, as a subprocess, with `cwd` set to a temp directory
- feed it a fixture file by absolute path
- assert the exit code, and assert `json.loads(stdout)` **parses**

That last assertion is the one that catches this class of bug. `json.loads` on a Python dict repr
raises immediately — single quotes aren't valid JSON. A test that only checked "did it print
something" would have passed against the broken artifact.

The tradeoff is honest: such a test is slow, it needs the package installed to run, and it fails for
environmental reasons that have nothing to do with your logic. That is the cost of testing a claim
about the environment. Keep one, not twenty — every other assertion belongs in a fast unit test
against the source.

---

## Open questions

- **Editable or copied for local development?** `uv tool install --editable` exists. It makes the
  dev loop pleasant and quietly destroys the property that made §8 meaningful, since the "installed"
  tool is then just a view of your working tree. Probably: copied, plus a reinstall step you run
  before claiming it works.
- **Should the install-and-run check live in CI?** Yes, eventually. CI was explicitly out of scope
  for this fight. When it lands, this is the check that most deserves to be there, because it is the
  one no local habit reliably covers.

---

## Where this returns

Every deliverable from here that ships as a command rather than a file — the ROS 2 nodes in
particular, where `colcon build` and `source install/setup.bash` are the same snapshot problem with
different spelling. An unsourced workspace and a stale `uv tool install` fail identically: the code
you are reading is not the code that ran.

Related: [05](05-packaging-and-console-scripts.md) for how console scripts are wired in the first
place, and [09](09-io-at-the-edges.md) for why the thing being installed has a clean entry point at
all.
