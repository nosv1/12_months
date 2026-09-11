# Week 1 20260909 - 20260913 — <topic>

**Built:** what exists now that didn't before  

- ~/12_months on wsl
- uv project initialized
- published to github

**Broke:** what went wrong, and the actual root cause  

- `*` in filenames was a fail -- wanted to show which files AI created
- 12_months as a package name is illegal for python -- shoulda known that
- git add * doesn't touch `.` files, also it helps when you're not in a sub-directory lol -- use `git add -A` as well as `git status` and `git dif --cached`

**Learned:** the thing you'd tell past-you  

- **pip is an installer**. You say "install numpy," it resolves and installs numpy. That's it. It has no concept of your project's intended dependency set. requirements.txt is a text file you maintain by hand or by pip freeze, and freeze dumps your entire environment including transitive deps you never asked for, at whatever versions happened to land.
- **uv is a project manager** that also happens to be a very fast installer. It maintains the distinction between what you declared (pyproject.toml: "I need numpy >= 2.0") and what you got (uv.lock: "numpy 2.1.3, and here are the 14 things it pulled in, with hashes"). Reproducibility comes from that split.
- `git add -A`, `git dff --cached`, and un-anchoring in `.gitignore` `telemetry/.venv/` -> `.venv/`
- commit messages answer **what chnaged and why**, not **when** -- phrase the first bit as a command, *the developer did this*, only need a body when the *why* isn't obvious

**Stuck on:** open questions carried forward  
**Hours:** actual, not aspirational  
20260909 2103 - 2200 (1 hour)
20260910 1753 - 2000 (2 hours)
20260911 1613 - 1823 (2 hours)
