# `#include`, namespaces, and `using namespace std`

**Week:** 1 (pre-week-3 prep) · **Syllabus item:** C++ toolchain verified with a hello world ·
**Prompted by:** deleting `#include <iostream>` from `hello.cpp` and reading the error; "why
`std::cout` and not `cout`?" — "no idea."

---

## Mental model: `#include` is copy-paste, not `import`

The comparison to Python's `import` is where most people start. It's close enough to be misleading.

| Python `import` | C++ `#include` |
| --- | --- |
| Runtime: executes a module once, caches it | Before compilation: the **preprocessor** pastes the file's text in place |
| Gives you a module object (`math.sqrt`) | Gives you **declarations**, dropped straight into your file |
| Controls names: `import x` vs `from x import y` | Controls nothing. Every name in the header appears, just as it's written there |

The C++ build has stages: **preprocess → compile → link**. `#include <iostream>` is handled in the
first stage. The compiler never sees the `#include`, only several thousand lines of pasted
declarations followed by your `main`. You can see this yourself:

```bash
g++ -E hello.cpp | wc -l      # -E: stop after preprocessing
```

So when the include is deleted, the error isn't "module not found." It's the compiler reaching
`std::cout` and never having been told that name exists: *`'cout' is not a member of 'std'`*.
A **declaration** is a promise that a name exists, with its type. The compiler refuses to use a
name it hasn't seen declared. (The **definition**, the actual machine code, is found later by the
linker. That distinction shows up in week 3 as "undefined reference" errors.)

A correction to "no include means no `std` namespace": `std` isn't one thing that `<iostream>`
switches on. Every standard header adds its own names to it. `<vector>` adds `std::vector`,
`<string>` adds `std::string`. `<iostream>` adds `std::cout`. Leave that header out and `std`
can still exist, just without `cout` in it.

## Namespaces: a surname for names

C++ has no modules to keep names apart (C++20 modules exist but are barely used yet). Without
something to separate them, every name from every library you include would share one global
pool. A `count` from your code, a `count` from the standard library and a `count` from a robotics
library would collide.

A **namespace** is a prefix that keeps them apart. The whole standard library lives in `std::`,
and ROS 2 lives in `rclcpp::`. `::` is the scope operator, so `std::cout` means "the `cout` that
belongs to `std`."

## Why `using namespace std;` is considered bad style

`using namespace std;` takes every name `std` has from the headers you've included and pours it
into the current scope. The standard library has many short, common names: `count`, `distance`,
`max`, `min`, `size`, `data`, `swap`, `list`, `function`, `byte`...

1. **Collisions.** Write your own `distance()` for robot odometry and a call to it can end up
   ambiguous with `std::distance`, or quietly resolve to the wrong one. Which one wins depends on
   argument types and overload rules, and the error messages are awful.
2. **It breaks later.** New C++ standards add names to `std`. Code that compiles today can stop
   compiling after a compiler upgrade, with no change on your side.
3. **In a header, it's contagious.** This is where the first half of this entry matters. A header
   is pasted into every file that includes it, so a `using namespace std;` in a header is forced
   onto every one of those files, including files in other people's code. **Never put it in a
   header.** This one is a firm rule, not a style preference.
4. **Readability.** `std::` tells the reader "this is standard, go read cppreference." Without
   it, `sort(v)` could be yours, the standard library's, or a third library's.

Python has the same smell: `from numpy import *`. Same problem, same reason people avoid it.

### What's acceptable

- Writing `std::` explicitly. This is the default. It's five characters.
- Pulling in one name, in a `.cpp` file or inside a function: `using std::cout;`
- A namespace alias for long names: `namespace fs = std::filesystem;`, the C++ version of
  `import numpy as np`.
- `using namespace std::chrono_literals;` inside a function. Some namespaces are *designed* to be
  pulled in. You'll see this in ROS 2 for `500ms`-style durations.

## Open questions / where this returns

- **Week 3:** header/source splits, include guards (`#pragma once`), and why pasting the same
  header twice would otherwise define things twice.
- **Week 3–4:** "undefined reference" linker errors: declared (header seen) but never defined
  (`.cpp` not compiled in or linked).
- **CMake:** `target_include_directories` is how the preprocessor is told *where* to find the
  files it pastes.
- `std::endl` vs `'\n'`: `endl` also flushes the output buffer every time. Worth knowing, not
  worth worrying about in a hello world.
