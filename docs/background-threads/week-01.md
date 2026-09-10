## Week 1 20260909 - 20260913 — <topic>

**Built:** what exists now that didn't before  
- 20260909: 
* ~/12_months on wsl
* uv project initialized

**Broke:** what went wrong, and the actual root cause  

**Learned:** the thing you'd tell past-you  
### pip vs uv
- **pip is an installer**. You say "install numpy," it resolves and installs numpy. That's it. It has no concept of your project's intended dependency set. requirements.txt is a text file you maintain by hand or by pip freeze, and freeze dumps your entire environment including transitive deps you never asked for, at whatever versions happened to land.
- **uv is a project manager** that also happens to be a very fast installer. It maintains the distinction between what you declared (pyproject.toml: "I need numpy >= 2.0") and what you got (uv.lock: "numpy 2.1.3, and here are the 14 things it pulled in, with hashes"). Reproducibility comes from that split.

**Stuck on:** open questions carried forward  
**Hours:** actual, not aspirational  
20260909 2103 - 2200