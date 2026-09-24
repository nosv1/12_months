# 24 — RAII: who frees the memory, on every exit path

**Week 4.** Syllabus items: *Stack vs heap*, *RAII*, *`unique_ptr`*, *Debug with sanitizers*.
Partial: *Dangling references, use-after-free, and how they present* (double free only).

Prompted by `cpp_memory/`, built in one sitting as a chain of predictions: a leak that looked fine,
a sanitizer that named the line, a throw that skipped the `delete`, a class that fixed it, and a
copy that broke it again.

Follows [21 — Values, references, pointers, and `const`](21-values-references-pointers-and-const.md)
(copy construction) and [23 — Converting constructors and `explicit`](23-converting-constructors-and-explicit.md).

---

## The mental model: two lifetimes

Every `new` creates **two** things with **different lifetimes**:

```cpp
int* t = new int(1);
```

| Thing | Where | Lives until |
| --- | --- | --- |
| `t` — 8 bytes holding an address | stack | the end of the enclosing scope, **guaranteed** |
| the `int` | heap | someone calls `delete t` — **nothing else frees it** |

Destroying a raw pointer does nothing to what it points at. Throwing away a slip of paper with an
address on it doesn't demolish the house. Lose the last slip and the house is still there, forever,
and nobody can find it: that is a **leak**.

Python never shows this split because the garbage collector ties the two lifetimes together. C++
leaves them separate, and every tool in this entry exists to tie them back together.

## Step 1 — A leak looks fine

```cpp
int main() {
  int* t = new int(1);
  return 0;
}
```

Builds, runs, exits 0. `-Wall` warns about an **unused variable**, which is about the name, not the
memory: print `*t` and the warning disappears while the leak stays. The compiler cannot know
whether a `delete` was meant to come later. Leaks need a runtime tool.

## Step 2 — AddressSanitizer

```cmake
target_compile_options(mem PRIVATE -Wall -Wextra -D_GLIBCXX_ASSERTIONS -fsanitize=address -g)
target_link_options(mem PRIVATE -fsanitize=address)
```

**The flag must go to both stages.** At compile time, `-fsanitize=address` rewrites the program:
every memory access and every `new`/`delete` gets a call to a checker (`__asan_...`) inserted
around it. Those checkers live in a runtime library that only gets linked if the *linker* also sees
the flag. Compile-only produces a wall of `undefined reference to __asan_...`, which is a linker
error by the stage rules in [20](20-the-four-stages-of-a-build.md).

`-g` adds debug info, so the report shows file and line instead of bare addresses.

On exit, LeakSanitizer (part of ASan) reports:

```text
ERROR: LeakSanitizer: detected memory leaks
Direct leak of 4 byte(s) in 1 object(s) allocated from:
    #0 ... in operator new(unsigned long) ...
    #1 ... in main .../cpp_memory/main.cpp:7
```

Read it like the assertion message in [22](22-parsing-input-that-fights-back.md): **what** (a direct
leak, 4 bytes, the size of one `int`), **where** (frame `#0` is the library's allocator; frame `#1`
is the first frame in your code, and its line is the `new`). No `gdb` needed; the stack trace is
already in the report.

Add the `delete`: silence.

## Step 3 — The realistic leak: an early exit

Nobody forgets `delete` in a four-line `main`. Leaks happen when something between the `new` and
the `delete` leaves the function early:

```cpp
int make_and_delete_int() {
  int* t = new int(1);
  throw std::runtime_error("eeee");
  delete t;                          // never runs
}
```

(Caught in `main`, so the program exits normally. An *uncaught* exception calls `std::terminate`,
which aborts, and LeakSanitizer never gets its end-of-program report. The leak would still exist;
the tool would just never see the exit it checks at.)

ASan reports a leak at the `new`. The mechanism is the two-lifetimes table. When the exception
leaves the function, C++ **does** clean up: it destroys every local on the way out. That is
**stack unwinding**, and it's guaranteed. `t` is a local, so `t` is destroyed. But `t` is the slip
of paper. The `int` is on the heap, and only `delete` frees it.

## Step 4 — RAII: make the stack object own the heap object

The stack lifetime is guaranteed and the heap lifetime isn't. So tie the second to the first: put
the pointer inside a stack object whose **destructor** calls `delete`.

```cpp
struct T {
  int* t;
  T(int* t) : t(t) {}
  ~T() { delete t; }     // frees what t points AT, not t itself
};

int make_and_delete_int() {
  T t(new int(1));
  throw std::runtime_error("eeee");
}
```

Clean under ASan, **including on the throwing path**. Unwinding destroys `t`, destroying `t` runs
`~T()`, and `~T()` frees the `int`. No cleanup was written for the error path; the type handled it.

This is **RAII**, *Resource Acquisition Is Initialization*, a famously bad name for a simple rule:

> **Acquire a resource in a constructor; release it in the destructor; hold the object on the
> stack.** Then release happens on every exit path — end of scope, `return`, `throw` — without
> anyone remembering to do it.

The resource doesn't have to be memory. `std::ifstream` is RAII over a file handle, which is why
`cpp_telemetry/reader.cpp` never calls `close()`. Mutex locks (`std::lock_guard`, week 6) and
sockets (week 7) work the same way.

### The first attempt, and what it shows

The first version of `T` had a constructor and a member, and **no destructor**. It still leaked.
The compiler generates a destructor if you don't write one, but the generated one only destroys
members, and destroying an `int*` member is the slip-of-paper problem again. **Wrapping a pointer
in a class does nothing on its own. The destructor is what does the work.**

## Step 5 — The copy that breaks it: double free

```cpp
T a(new int(1));
T b = a;
```

Prediction on record: *"b is just renaming a, so it'll all behave the same."* Result:

```text
ERROR: AddressSanitizer: attempting double-free on 0x... in thread T0:
    #0 ... in operator delete(void*, unsigned long) ...
    #1 ... in T::~T() .../cpp_memory/main.cpp:7
```

`T b = a` is **copy construction** (see [21](21-values-references-pointers-and-const.md)): a second,
separate object. The generated copy constructor copies each member, and the member is an address.
Now two objects hold the same address and **both believe they own it**. At end of scope `b`'s
destructor frees the `int`, then `a`'s destructor frees it again.

Without ASan a double free is undefined behaviour. It might crash immediately, or it might corrupt
the allocator's internal bookkeeping and crash somewhere unrelated much later, which is the worst
kind of bug to find. ASan stops at the second `delete` and names the line.

**A class that owns a resource cannot use the default copy.** This is the **Rule of Three**: if
a class needs a custom destructor, it almost certainly needs a custom (or deleted) copy constructor
and copy assignment too. The destructor is the signal that the class owns something.

### Forbid it

```cpp
T(const T&) = delete;
```

```text
error: use of deleted function ‘T::T(const T&)’
```

The double free is now a compile error.

## Step 6 — `std::unique_ptr` is that class

```cpp
auto p = std::make_unique<int>(1);
auto q = p;
```

```text
error: use of deleted function ‘std::unique_ptr<_Tp, _Dp>::unique_ptr(const std::unique_ptr<_Tp, _Dp>&)
    [with _Tp = int; _Dp = std::default_delete<int>]’
```

Same error as the hand-written `T`. Read the template arguments: `_Tp = int` is what it owns;
`_Dp = std::default_delete<int>` is what its destructor does, which is call `delete`. **`unique_ptr` is
`T`**: a pointer, a destructor that deletes, copying deleted. It is generic, tested, and zero
overhead (the same size as a raw pointer).

It adds one thing `T` doesn't have: a way to **transfer** ownership instead of copying it,
`std::move`. That is move semantics, next.

## The rules

- **Raw `new`/`delete` in application code is a smell.** Use `std::make_unique`. The ownership
  lives in the type, so the compiler enforces it.
- **A raw pointer (`T*`) or reference means "I'm using it, I don't own it."** An owning pointer is
  a `unique_ptr`. That convention lets a reader tell who is responsible for freeing something from
  the signature alone.
- **If you write a destructor, decide about copying.** Delete it, or define it deliberately. Never
  leave the default in place by accident.
- **ASan in every debug build.** `-fsanitize=address -g` on compile *and* link. It costs ~2x
  runtime and finds leaks, double frees, use-after-free, and buffer overruns at the line they
  happen.

## Open questions

- **Move semantics.** What does `std::move` actually do (spoiler: nothing at runtime; it's a
  cast), and what is left in the moved-from `unique_ptr`?
- **`shared_ptr`**: when ownership genuinely is shared, and why that is rarer than it seems. The
  syllabus asks "when each is correct."
- **Use-after-free**: the other half of the syllabus item. Keeping a raw pointer to what a
  `unique_ptr` owns, after the `unique_ptr` is gone, is the natural way to produce one.
- **`valgrind`**: the other tool the syllabus names. It works without recompiling but runs tens of times
  slower. Worth running once on the same leak to compare.

## Where this returns

Every ROS 2 node is held by a `std::shared_ptr` (`rclcpp::Node::SharedPtr`), and publishers,
subscriptions and timers are too. The reason is the question above, answered at scale. The week 7
sensor simulator owns threads and sockets; both are resources, and both want RAII wrappers.
