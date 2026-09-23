# 22 — Parsing input that fights back

**Week 3.** Syllabus item: none directly — this is what the week-3 deliverable taught on the way.

Prompted by porting `telemetry/` to C++: a `std::invalid_argument` with no line number, a
`conflicting declaration ‘RobotID* row’` that named a variable nobody wrote, and a segfault on
line 301 of the sample CSV.

Follows [21 — Values, references, pointers, and `const`](21-values-references-pointers-and-const.md).

---

## Parsing *is* validation

The instinct carried over from Python is to check first, then convert:

```python
if is_valid_float(cell):
    value = float(cell)
```

In C++ the same shape feels worse, and the discomfort is correct: **there is no cheap separate check
that is also correct.** The only honest answer to "is this a valid double?" is to try to turn it
into one. A separate validator either duplicates the parser (and can disagree with it) or is wrong.

So the question is never "how do I validate before parsing." It is:

> **How does an attempt report that it failed?**

That single reframing is what the rest of this entry answers.

### Shape and value are different questions

One exception, and it matters:

| Property | Question | How it's answered |
| --- | --- | --- |
| **Shape** | does this row have 5 fields? | must be checked *before* indexing |
| **Value** | is field 2 a double? | only by attempting the conversion |

Checking `row.size() != 5` before touching `row[2]` is not the double-work objected to above.
Indexing is the operation that breaks, so the check has to come first. Two different kinds of wrong,
two different mechanisms.

---

## Reporting failure: the three shapes in C++17

### 1. Throw and catch

`std::stod` throws. Two things, and only two:

| Exception | When |
| --- | --- |
| `std::invalid_argument` | no leading number at all — `"velocity"`, `"abc"`, `""` |
| `std::out_of_range` | parseable, but too large for a `double` |

Both derive from `std::logic_error`, which derives from `std::exception`. Needs `<stdexcept>`.

```cpp
try {
  readings.push_back(Reading{...});
} catch (const std::invalid_argument& e) {
  // count it, record the row number
} catch (const std::out_of_range& e) {
  // ...
}
```

### 2. `std::optional<T>`

A function returns "a `T`, or nothing." The caller cannot read the value without checking first —
the type enforces it. This is what `auto [ok, value]` is groping toward, without the problem of
deciding what `value` holds when `ok` is false.

### 3. `std::from_chars` (`<charconv>`)

The non-throwing standard parser. Returns an error code; never throws. Built for exactly this case:
untrusted input where failure is routine.

### Which one

The deciding frame: **exceptions are for things that shouldn't happen.** A telemetry file containing
malformed rows is a file behaving exactly as expected — the Python version *counted* bad readings
as a deliverable. A third of the input being junk is not exceptional, it's the input.

That argues against throwing as the primary mechanism, though catching is the cheapest thing to
reach for when the throw is already happening inside a library call.

Whatever is chosen, the failure must carry **which row and which field**, or the resulting count is
a number nothing can be done with.

---

## Catch by `const&`

One of the few rules in C++ with no exceptions.

```cpp
catch (std::exception e)          // wrong
catch (const std::exception& e)   // right
```

Catching by value **copy-constructs** the exception into the base type, which slices off everything
derived — an `std::invalid_argument` caught as an `std::exception` by value keeps only the base
part. That is the copy constructor from [21](21-values-references-pointers-and-const.md) doing
damage rather than being educational. It is also a pointless copy of an object about to be
discarded.

### How broadly to catch

```cpp
catch (const std::invalid_argument& e)  // this specific failure
catch (const std::exception& e)         // everything standard
catch (...)                             // everything, with no access to what was thrown
```

`e.what()` returns a `const char*`. For `stod` failures the message is terse and unhelpful; the
useful context (row number, field name) has to be supplied by the catching code.

Catching `std::exception` is the C++ equivalent of a bare `except Exception:` — it will also
swallow `std::bad_alloc` and any genuine bug that happens to throw. Catch what is expected. If
something else comes out, that is information.

---

## Constructors that can fail

Pushing conversion into a constructor —

```cpp
struct Velocity {
  double v;
  Velocity(std::string s) { v = std::stod(s); }   // throws on bad input
};
```

— is how the decision above gets made by accident. A constructor cannot return anything, so
throwing is very nearly its only option, and a half-constructed object cannot exist.

**A constructor that can fail is a smell in C++.** The usual fix is a factory: a static function
that returns an `optional` (or a result type), with the constructor taking an already-valid value
and therefore being incapable of failing.

```cpp
struct Velocity {
  double v;
  explicit Velocity(double v) : v(v) {}            // cannot fail
  static std::optional<Velocity> from_string(const std::string& s);
};
```

The tradeoff: the invariant "a `Velocity` always holds a valid number" is preserved either way, but
the factory gives the failure somewhere to live that isn't the exception system.

---

## `operator[]` does not bounds-check

Line 301 of the sample CSV is a truncated row — a timestamp and nothing else. Reading `row[1]`
segfaulted.

```cpp
row[0]     // operator[]  — NO bounds check. Out of range is undefined behavior.
row.at(0)  // .at()       — bounds-checked. Throws std::out_of_range with a message.
```

This is the same bargain as the dangling reference in [21](21-values-references-pointers-and-const.md):
C++ does not make you pay for a check you might not need, and the price is that being wrong is
undefined rather than reported. Python's list indexing is always `.at()`; C++ makes it a choice and
defaults to the unchecked one.

`.at()` turns the segfault into a catchable exception naming the index.

### The build flag that makes this findable

```cmake
target_compile_options(telem PRIVATE -Wall -Wextra -D_GLIBCXX_ASSERTIONS)
```

`_GLIBCXX_ASSERTIONS` enables libstdc++'s cheap precondition checks — `operator[]` on a `vector`,
`front()` on an empty container, invalid iterators. A segfault becomes:

```text
Error: attempt to subscript container with out-of-bounds index 1, but container only holds
1 elements.
```

with a line number. Small runtime cost; belongs in every debug build.

The heavier tool is `-fsanitize=address` (AddressSanitizer), which also catches use-after-free and
buffer overruns — week 4 material, same idea.

---

## The Most Vexing Parse

```cpp
Reading r(Timestamp(row[0]), RobotID(row[1]), Velocity(row[2]));
```

> `error: conflicting declaration ‘RobotID* row’`
> `note: previous declaration as ‘Timestamp* row’`
> `warning: parentheses were disambiguated as a function declaration [-Wvexing-parse]`

The compiler read that line as a **function declaration**: a function named `r`, returning
`Reading`, taking three parameters —

- `Timestamp(row[0])` → a parameter named `row` of type `Timestamp[0]`, decaying to `Timestamp*`
- `RobotID(row[1])` → another parameter named `row`, of type `RobotID*`

Three parameters with the same name, hence "conflicting declaration." The error is accurate; it is
answering a question nobody asked.

**The rule: if something can be parsed as a declaration, C++ parses it as a declaration.**
Parentheses are ambiguous — they serve both calls and declarations — and declaration wins.

### The fix, and why modern style uses braces

```cpp
Reading r{Timestamp(row[0]), RobotID(row[1]), Velocity(row[2])};
```

Braces cannot introduce a function declaration, so the ambiguity cannot arise. **This is the actual
reason `Type name{args}` is the recommended modern spelling**, not merely fashion.

The degenerate case is worth recognising too:

```cpp
Widget w();   // declares a function taking no arguments and returning Widget
Widget w{};   // constructs a Widget
```

---

## Finding an uncaught exception: `catch throw`

An uncaught exception aborts with a type name and no line number:

```text
terminate called after throwing an instance of 'std::invalid_argument'
```

The C++ equivalent of `pytest --pdb` ([19](19-debugging-with-pdb.md)) is gdb's `catch throw`.
Debug symbols first:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

```text
(gdb) catch throw      # break at the moment of the throw
(gdb) run
(gdb) bt full          # backtrace WITH locals for every frame
(gdb) p row[2]         # evaluate any expression in the current frame
```

`catch throw` is the whole trick. Without it the program stops at `terminate()`, long after the
stack that caused the throw has unwound and the evidence is gone.

Note the distinction, which costs time if missed:

- `info locals` — local **variables** only
- `info args` — **parameters**. A constructor's parameter is not a local, so `info locals` in a
  constructor's frame shows nothing.
- `bt full` shows both, for every frame, in one command.

---

## Open questions

- **Where the `try` goes** is a design decision, not a mechanical one. Around the whole row means
  one bad field discards the row. Around each field means deciding what a `Reading` with one
  missing value means.
- **Strong types** (`struct Velocity { double v; };`) prevent swapping same-typed arguments at a
  call site, which the compiler otherwise accepts silently. They also push conversion into
  constructors, which is how the failure-reporting decision gets made by accident.
- **`std::expected`** is C++23's answer to "a value or an error, with the error carrying detail."
  Not available in C++17, which is what ROS 2 Jazzy targets.

## Where this returns

Week 4 (memory and ownership) makes `-fsanitize=address` routine. Every ROS 2 node parses
configuration and messages from outside itself, and the shape of "this input might be wrong" does
not change — only the volume.
