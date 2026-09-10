# Environment

Machine, toolchain, and the gotchas that will otherwise cost you an evening each.

## Hardware

| | |
|---|---|
| CPU | AMD Ryzen 7 9800X3D (8C/16T) |
| RAM | 32 GB |
| GPU | **NVIDIA RTX 5080, 16 GB** (Blackwell, `sm_120`) |
| Driver | 591.86 |
| OS | Windows 11 Home |

This is comfortably above spec for everything in the syllabus, including Isaac Lab. RAM is the
only soft spot — 32 GB gets tight running Isaac Sim alongside WSL2 and Windows. Cap WSL's memory
in `.wslconfig` if you hit swapping.

## Decision: Ubuntu 24.04 + ROS 2 Jazzy

Settled September 2026.

| Ubuntu | ROS 2 | EOL | Verdict |
|---|---|---|---|
| 22.04 Jammy | Humble | **May 2027** | Dies at ~week 35 of 52 |
| **24.04 Noble** | **Jazzy Jalisco** | **May 2029** | ✅ Chosen |
| 26.04 | Lyrical Luth | May 2031 | Too new — third-party packages lag |

Jazzy is two years mature, so Nav2, `slam_toolbox`, MoveIt 2, and the sensor drivers are ported
and the official tutorials match what you'll actually run. It outlives both the course and the
job search.

The trap avoided: Humble has the largest tutorial ecosystem by volume, which makes 22.04 tempting.
But EOL lands mid-course, and finishing on an unsupported distro is a bad interview answer.

>Jazzy pins Python 3.12 via Noble; rclpy is a system C extension and won't import into a uv-downloaded interpreter

**Consequence:** when following tutorials, check the distro. Humble material is everywhere and
mostly transfers, but Nav2 and MoveIt 2 APIs did change between Humble and Jazzy. When something
doesn't work, distro mismatch is the first thing to check.

## WSL layout

Distros currently registered:

- `Ubuntu-24.04` — **the working distro.** Everything lives here.
- `Ubuntu` (26.04) — earlier attempt, user `seagraves`
- `Ubuntu-26.04` — earlier attempt, user `chris`, broken systemd user session

The two 26.04 distros are unused. Remove them once 24.04 is confirmed working:

```powershell
wsl --unregister Ubuntu
wsl --unregister Ubuntu-26.04
```

Destructive and irreversible — confirm nothing is in them first.

Set the default:

```powershell
wsl --set-default Ubuntu-24.04
```

GPU passthrough is confirmed working under WSL2 — `nvidia-smi` resolves inside the distro and
reports the 5080. CUDA workloads run without extra configuration.

## Gotchas

### 1. The RTX 5080 needs CUDA 12.8+

Blackwell is compute capability `sm_120`. Stock PyTorch wheels built against older CUDA install
cleanly and then **fail at runtime**:

```
CUDA error: no kernel image is available for execution on the device
```

Install a cu128-or-later build. Verify immediately after installing — don't discover this
mid-training in week 27:

```python
import torch
print(torch.__version__, torch.version.cuda)
print(torch.cuda.is_available(), torch.cuda.get_device_capability())
# want (12, 0) for sm_120
torch.zeros(1).cuda() @ torch.zeros(1, 1).cuda()   # actually exercises a kernel
```

`torch.cuda.is_available()` returning `True` does **not** mean kernels will run. Force an actual
operation.

### 2. Work inside the WSL filesystem

Keep everything in `~/`. Never work from `/mnt/c/`.

Windows-mounted paths cross the 9P protocol boundary: file operations are ~10–20× slower, file
watching breaks (so hot reload and `colcon` incremental builds misbehave), and Unix permissions
don't map correctly — which git notices and complains about constantly.

This also means **the project should not live in OneDrive.** OneDrive's sync daemon and git fight
over file locks, and `.git` in a synced folder is a known corruption source.

### 3. Git repo placement

`git init` run from `$HOME` makes your entire home directory a repository — it will try to track
`.bashrc`, `.cache/`, SSH keys, and everything else. If `git status` in your project shows paths
starting with `../`, this has happened.

Check and fix (safe when there are no commits yet):

```bash
git -C ~ rev-parse --git-dir 2>/dev/null && echo "HOME IS A REPO — fix it"
rm -rf ~/.git                    # only if it has no commits you care about
cd ~/12_months && git init -b dev
```

### 4. ROS 2 DDS across the WSL boundary

Fine entirely inside one distro. Painful the moment you talk to another machine — which happens
in **Part 6, week 20**, when the Raspberry Pi arrives.

WSL2 sits behind a NAT by default and DDS discovery relies on multicast, which doesn't traverse
it. Windows 11 supports mirrored networking mode, which mostly fixes this — in `%USERPROFILE%\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

Budget debugging time anyway. Cross-machine discovery is the standard first wall in real ROS 2
work, and `ROS_DOMAIN_ID` mismatches will get you at least once.

### 5. Native dual-boot before Part 3

WSL2 is genuinely good for Parts 1–2 — Python, C++, Linux, Docker are all native-quality. It gets
flaky exactly where you're heading:

- Gazebo and Isaac GPU rendering through WSLg — works, but unpredictably
- USB passthrough for real sensors (needs `usbipd-win`, extra friction every session)
- Cross-machine DDS, as above
- Real-time scheduling for control loops

**Plan the dual-boot for around week 8, needed by week 20.** Don't do it now — "perfect the
environment first" is the most reliable way for week 1 to never happen.

## Toolchain checklist

Set up in `Ubuntu-24.04` during week 1:

- [ ] `build-essential`, `cmake`, `gdb`, `valgrind`
- [ ] Python 3 + `uv` (or `venv`)
- [ ] PyTorch with **cu128+** — verify with the snippet above
- [ ] Docker Engine (in WSL, not Docker Desktop — fewer moving parts)
- [ ] Git configured: name, email, SSH key on GitHub
- [ ] Shell you actually like — you'll be in it for 550 hours
- [ ] VS Code + Remote-WSL extension
- [ ] ROS 2 Jazzy — **not needed until week 11**, don't install early

## Verify

```bash
uname -a && lsb_release -ds
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
gcc --version | head -1 && cmake --version | head -1
python3 -c "import torch; print(torch.__version__, torch.cuda.get_device_capability())"
docker run --rm hello-world
```
