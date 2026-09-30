# 35 — A library another project can use: ODR, `include/`, and who can see what

**Week 5.** Syllabus item: *Build a library, link it from another project.* Until this session,
only this project's own executable and test used `sensor_processing_library`. Here a separate
project, `labs/w05-consumer/`, pulls it in with `add_subdirectory`. Related:
[31](31-operators-const-this-and-what-a-header-promises.md) (what a header promises; multiple
definitions), [30](30-templates-vs-abstract-classes.md).

---

## First: a function body in a header is a link error waiting to happen

`analysis.h` defined `mean`'s body, not just its declaration. Every `.cpp` that includes the header
compiles its own copy of `analysis::temperature::mean`. As soon as two `.cpp` files in the same
binary include it, the linker fails with *multiple definition*. It hadn't failed yet only because
one file included it.

This is the **One Definition Rule (ODR)**: a non-inline function may be defined only once across
the whole program. The fixes are to mark it `inline` (the linker merges the copies) or move the
body into `analysis.cpp`. The body was moved.

**Templates are exempt.** That's why `sensor_buffer.h` can hold all of `SensorBuffer<T>`'s bodies:
the compiler has to see a template's body at every use, so the rule allows repeated definitions.

## Namespaces, not empty structs

The first design idea was `struct Analysis { TemperatureAnalysis temperature_analysis; }`, with
`calculate_mean` as a member. The question to ask: **what state does the struct hold?** If the
answer is none, it's a namespace in disguise:

```cpp
namespace analysis::temperature {   // C++17 nested form
double mean(const std::vector<TemperatureReading>& readings);
}  // namespace analysis::temperature
```

No semicolon after the closing brace. In the `.cpp`, either reopen the namespace or write the full
name: `double analysis::temperature::mean(...) { ... }`.

## Why the consumer couldn't find the headers

`#include "sensor_buffer.h"` with quotes searches **the including file's own directory first**.
Every file in `w05-sensor-processing/` sat next to the headers, so this never needed configuring.
The consumer's `main.cpp` is somewhere else, so the compiler had nowhere to look. The library has
to **publish** its include directory:

```cmake
target_include_directories(sensor_processing_library
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
)
```

The first working version put this in the **consumer's** `CMakeLists.txt`, with a relative path.
It built, but then every consumer would have to copy that block and know the path. The library
knows where its headers live, so it declares that once, and linking the library carries it along.

## `PRIVATE`, `INTERFACE`, `PUBLIC`: who gets the setting

This got confused in the session ("`INTERFACE` means only the local files can see them"). That
describes `PRIVATE`. The table:

| Keyword | The library's own `.cpp` files | Targets that link the library |
| --- | --- | --- |
| `PRIVATE` | ✓ | ✗ |
| `INTERFACE` | ✗ | ✓ |
| `PUBLIC` | ✓ | ✓ |

Applied to what's in this project:

- **Include directory → `PUBLIC`.** After the move to `include/` + `src/`, the library's own
  `src/*.cpp` no longer sit next to the headers, so they need the path too. Verified by breaking it:
  switching to `INTERFACE` made `analysis.cpp` fail with "no such file" on `analysis.h`.
- **`-Wall -Wextra` → `PRIVATE`.** Warnings about the library's code are the library's business.
- **ASan link flag → `INTERFACE`.** A static library never goes through the link step itself. Only
  the executables that link it do (textbook 31's undefined references).

## `include/` and `src/`

```text
w05-sensor-processing/
├── include/   headers: the public face
├── src/       library .cpp files
├── main.cpp
└── sensor_processing_test.cpp
```

This does more than tidy up. `PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}` would expose *every* file in the
directory to consumers, `main.cpp` and the test file included. Pointing it at `include/` exposes
only what's meant to be public. `git mv` keeps each file's history through the move.

## `CMAKE_SOURCE_DIR` vs `CMAKE_CURRENT_SOURCE_DIR`

Worked out before hitting the bug: *"CMAKE_SOURCE_DIR is probably for the consumer dir, not the
library source."*

- `CMAKE_SOURCE_DIR` is the **top-level** project's directory, i.e. whoever ran `cmake -S`. The same
  line gives different answers depending on who's building.
- `CMAKE_CURRENT_SOURCE_DIR` is the directory of the `CMakeLists.txt` **currently being processed**.
  In the library's file, it's always the library's directory.

Rule: a `CMakeLists.txt` that someone else might `add_subdirectory` shouldn't use
`CMAKE_SOURCE_DIR`.

## `add_subdirectory` runs the whole file

*"I don't understand how the consumer cmake is running… the consumer only needs the library bit."*

`add_subdirectory(../w05-sensor-processing sensor_processing_library)` runs the library's entire
`CMakeLists.txt` as if it were pasted in. The second argument is required when the directory is
outside the consumer's tree: it names where that project's build files go. Arguments are separated
by spaces, and **quotes join everything inside them into one argument**, which is why
`"../w05-sensor-processing sensor_processing_library"` failed as a single nonexistent path.

**Defining a target is not building it.** Configure *defines* every target in the file. `cmake
--build` then builds the target `all`, which means every target anyone defined, regardless of
whether the consumer needs it. There are two standard controls, and projects usually use both:

- **In the library:** `if(PROJECT_IS_TOP_LEVEL)` (CMake 3.21+) around the things only a standalone
  build needs: `FetchContent` for gtest, the test executable, the demo `main`. Before 3.21, people
  compared `CMAKE_SOURCE_DIR` to `CMAKE_CURRENT_SOURCE_DIR`. Write `if(PROJECT_IS_TOP_LEVEL)`, not
  `if(${PROJECT_IS_TOP_LEVEL})`: `if` looks up variable names itself, and the `${}` form expands
  the value first.
- **In the consumer:** `add_subdirectory(... EXCLUDE_FROM_ALL)`. Everything is still defined, but
  only targets the consumer depends on get built. This doesn't stop `FetchContent`, which downloads
  during *configure*, so the library's guard still matters.

Also learned by moving blocks around: CMake runs top to bottom. **A `target_*` command must come
after the `add_library`/`add_executable` that creates the target.**

## Configure, then build

```bash
cmake -S . -B build     # configure: read CMakeLists.txt, find the compiler, write Makefiles
cmake --build build     # build: run them
```

A new build directory always needs the configure step. After moving files, delete `build/` and
configure again, because a stale cache and moved files don't mix well.

## Editor vs compiler

After the move, VS Code reported *"name followed by '::' must be a class or namespace name"* on a
line that compiled fine. IntelliSense has its own include paths and didn't know about `include/`.
Fix: `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` writes `build/compile_commands.json` (the exact flags per
file), and `C_Cpp.default.compileCommands` points the extension at it. When the editor and the
compiler disagree, **the compiler is right**. Build before trusting a squiggle.

## Open

- The consumer's `main.cpp` prints nothing, so "it runs" shows only that it links.
- `find_package` is the other way to consume a library: install it, then find the installed copy.
  It's how system libraries and ROS packages work (`ament_cmake`, week 13).

**Returns in:** week 7 (the simulator as several libraries), week 13 onward (every ROS 2 package is
a CMake project that exports targets for others to link).
