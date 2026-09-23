# 20 — The four stages of a build, and reading an error by stage

**Week 3.** Syllabus items: *compilation model: preprocessor → compile → link (and what each error
looks like)*; *headers, translation units, ODR*.

Prompted by three vocabulary questions asked before writing any C++ — what `-E`, `-S` and `-c` do,
what ODR stands for, what RAII stands for — and by an observation from week 1 that `#include` was
"kinda wild." The whole entry is an answer to that last one.

---

## The mental model

Python runs a file. C++ **builds** one, in four separate programs chained together, and `g++`
normally runs all four so fast that they look like one step. Each flag stops the chain early:

| Command | Stages run | Output |
|---|---|---|
| `g++ -E f.cpp` | preprocess | C++ source, expanded |
| `g++ -S f.cpp` | + compile | `f.s`, assembly text |
| `g++ -c f.cpp` | + assemble | `f.o`, machine code with holes |
| `g++ f.cpp` | + link | `a.out`, runnable |

Knowing which stage failed is most of C++ debugging, because the three stages fail in three
recognisably different shapes.

---

## What each stage actually does

### Preprocessor — text substitution, and nothing else

It does not know C++. `#include <iostream>` means *paste the contents of that file here*, and the
pasted file includes others, recursively. Macros expand, `#ifdef` resolves. The output is still
C++ source.

A five-line `hello.cpp` containing one `#include <iostream>`:

```
$ wc -l hello.cpp          6
$ g++ -E hello.cpp | wc -l 36588
```

A ~7,300x expansion. This is why C++ builds are slow in a way Python imports are not: every `.cpp`
in the project redoes this work from scratch, and nothing is cached between them.

To see which files got pasted in:

```bash
g++ -E hello.cpp | grep '^# 1 "' | grep -o '"[^"]*"' | sort -u
```

### Compiler — text to assembly

Those 36,588 lines compiled to **67 lines** of assembly.

The ratio is the lesson. Almost everything a header contains is **declarations** — promises that
something exists. Declarations generate no code. Only definitions do, and the program defined
exactly one function.

### Assembler — assembly to an object file

`f.o`: real machine code, not runnable. See below.

### Linker — filling the holes

Takes every `.o` plus the libraries, resolves every unfilled reference, writes the executable.

---

## Declarations, definitions, and ODR

A distinction Python does not have:

```cpp
int add(int a, int b);                       // declaration: this exists, here is its shape
int add(int a, int b) { return a + b; }      // definition:  here is the actual thing
```

**The One Definition Rule (ODR):** declare as often as you like; define **exactly once** in the
whole program.

It exists because of how compilation is split up. The compiler processes each `.cpp` file
*completely separately* and never sees the others. That unit — one `.cpp` after all its `#include`s
have been pasted in — is a **translation unit**. So `main.cpp` can call a function defined in
`math.cpp` without ever seeing its code: the header supplies the shape, the compiler emits a hole,
the linker fills it.

But the linker must choose **one** address per symbol. Give it two definitions and it refuses to
guess: `multiple definition of 'add'`.

This is also the real reason for header guards. Without them, a header included twice in one
translation unit pastes its contents twice, and anything *defined* in it is now defined twice in
that unit.

(`inline` functions and templates are deliberate exceptions to ODR — see below.)

### One rule, three different enforcers

The same mistake produces three unrecognisably different errors depending on *where* the duplicate
lands. All three were produced deliberately in one session:

**Duplicates in one translation unit → the compiler catches it.** A body in the header plus an
out-of-line definition in the `.cpp` that includes it:

```
reading.cpp:12:8: error: redefinition of 'static double Reading::celsius_to_fahrenheit(double)'
In file included from reading.cpp:3:
reading.h:14:17: note: previously defined here
```

Line, column, caret, and a `note:` pointing at the other copy — because both are visible at once.

**Duplicates across translation units → the linker catches it.** A free function defined at file
scope in a header, included by two `.cpp` files:

```
/usr/bin/ld: b.o: in function `f(double)':
multiple definition of `f(double)'; a.o: first defined here
```

No line number. The linker never saw the source. Note this fires **even if nothing calls the
function** — the definition is emitted either way.

**A duplicate that is legal.** A function defined *inside* a class body is **implicitly `inline`**,
and `inline` tells the linker "expect many identical copies, pick one." So moving the body into the
struct in the header and including it everywhere does *not* fail. This is what makes header-only
libraries possible, and it is why the struct itself can live in a header at all.

### `static` at file scope will hide this from you

An attempt to reproduce the linker error silently failed because the function kept a `static`
carried over from when it was a class member:

```cpp
static double celsius_to_fahrenheit(double c) { ... }   // at file scope in a header
```

At file scope `static` means **internal linkage** — private to each translation unit. Each `.o`
gets its own private copy with a local symbol, so there is nothing for the linker to collide with
and `multiple definition` can never fire.

`static` is one keyword with three unrelated meanings, a C inheritance the language never cleaned up:

| Where it appears | What it means |
|---|---|
| on a class member | belongs to the type, not an instance — no `this` |
| on a function or variable at **file scope** | internal linkage — private to this translation unit |
| on a local variable inside a function | persists for the program's lifetime, not the call's |

Moving one unchanged line from inside a class to file scope silently switches meaning #1 to
meaning #2. Nothing warns.

### What a header guard actually does

```cpp
#ifndef READING_H   // 1st paste: not defined → true → process the body
#define READING_H   //            set the flag
  ...body...
#endif              // 2nd paste: now defined → false → skip to here
```

`#include` is **purely filename-based**. It has no relationship to the guard macro; `READING_H` is
an arbitrary flag meaning *"already pasted into this translation unit."* It could be named anything;
the filename-uppercased convention exists only to avoid collisions between headers.

Deleting the `#define` line disables the guard entirely — the flag is never set, so `#ifndef` is
always true. This produces no error until the header is included twice in one translation unit, at
which point the struct is redefined and the **compiler** objects.

Nobody writes the same `#include` twice on purpose, which is why a broken guard can look harmless.
The real case is indirect:

```
main.cpp → robot.h  → reading.h
         → sensor.h → reading.h
```

Neither intermediate header knows about the other. At ROS 2 scale this is constant, which is why
guards are unconditional practice rather than a judgment call. `#pragma once` is the one-line
alternative — non-standard but universally supported.

Guards are **per translation unit**. Every `.cpp` starts with no macros defined, so a header is
fully pasted into each one — that is the legal duplication, and it only works because identical
struct definitions are ODR-exempt.

---

## What "a hole" means, literally

`main` calling an undefined `foo()` and `std::cout`:

```
   8:  e8 00 00 00 00    call   <main+0xd>
  21:  e8 00 00 00 00    call   <main+0x26>
```

`e8` is the x86 call opcode; the following four bytes are the destination address. They are
literally zero — the compiler did not know where `foo` would live.

Zeros alone would be useless, so the compiler also leaves a note in a **relocation table**
(`objdump -r`):

```
OFFSET            TYPE             VALUE
0000000000000009  R_X86_64_PLT32   _Z3foov
0000000000000022  R_X86_64_PLT32   _ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
```

Row one reads: *at byte offset 9 — the four zeros after the `e8` at offset 8 — patch in the address
of symbol `_Z3foov`.* That is `foo()` after **name mangling**, which encodes namespace and parameter
types into the symbol because C++ permits overloading and the linker matches on names alone.
`c++filt`, or `nm -C`, decodes them.

**A hole is zeroed bytes plus a relocation record describing how to fill them.** Linking is
resolving every such record.

List a file's holes without waiting for a failure — `U` is undefined:

```bash
g++ -c hello.cpp && nm -C hello.o | grep ' U '
```

Note what row two implies: **not one instruction of iostream's implementation is in the object
file**, despite 36,588 lines of headers being pasted in. Headers carried the shape; the library
carries the code.

---

## Reading an error by stage

**Preprocessor** — it could not find text to paste:

```
fatal error: iostrem: No such file or directory
```

**Compiler** — it is looking directly at the source, so it can point:

```
cmp.cpp:2:33: error: expected ';' before 'return'
    2 | int main() { std::cout << "hi\n" return 0; }
      |                                 ^~~~~~~
      |                                 ;
```

**Linker** — it never saw the source, only symbols and byte offsets:

```
/usr/bin/ld: lnk.o: in function `main':
lnk.cpp:(.text+0x9): undefined reference to `foo()'
collect2: error: ld returned 1 exit status
```

The practical rule:

| Tell | Stage | Means |
|---|---|---|
| line, column, `^` caret | compiler | it did not understand what was written |
| `ld:`, symbol name, `.text+0x…` | linker | it understood fine; a promise was never kept |

`undefined reference` costs newcomers hours because it looks like a code error yet names no line.
It is not a code error. The code was accepted. Something promised to exist does not.

---

## On the vocabulary

C++ culture names ordinary things with acronyms:

- **ODR** — "define it once"
- **TU** — "one `.cpp` file after its includes"
- **RAII** — *Resource Acquisition Is Initialization*, a genuinely bad name for "acquire a resource
  in the constructor, release it in the destructor." C++ guarantees a stack object's destructor runs
  when it leaves scope, including when an exception unwinds past it, so tying cleanup to object
  lifetime makes leaks structurally impossible. Python solves the same problem with an explicit
  `with` block; C++ gets it from ordinary object lifetime, so it is automatic and composes —
  a class holding three such members cleans up all three with no code written. Week 4 is where this
  gets built rather than defined.

An unfamiliar acronym here is close to zero evidence about difficulty. The jargon layer is the
cheapest part of the language and looks the most intimidating from outside. The honest converse:
move semantics, template instantiation and undefined behaviour are genuinely hard, and the
vocabulary will not tell you which is which in advance.

---

## Where this returns

- **Week 3, headers and ODR** — a function body in a header, included twice, is a duplicate symbol.
  Same linker, same table.
- **Week 3, CMake** — CMake's job is deciding which `.o` files exist and what gets linked together.
- **Week 4, RAII** — see above.
- **Week 11+, ROS 2** — `undefined reference` against a ROS library almost always means a missing
  `target_link_libraries`, not broken code. The error shape names the stage, and the stage names
  the fix.

## Open

- `-O2` changes the assembly enough that the 67-line comparison stops holding. Worth rerunning
  `-S` under optimisation once inlining means something.
- Static vs dynamic linking not covered. `ldd a.out` shows what is still being resolved at *run*
  time, which is a fifth stage in all but name.
