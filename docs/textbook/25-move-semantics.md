# 25 — Move semantics: `std::move` moves nothing

**Week 4.** Syllabus item: *Move semantics and why copies are expensive*. Partial: *Dangling
references, use-after-free, and how they present* (null dereference after a move).

Prompted by `cpp_memory/`, as a chain of predictions: a moved `unique_ptr`, a class that prints
which constructor ran, a `vector` that constructed one more object than it was asked to, and a
`std::move` that ran a copy.

Follows [24 — RAII](24-raii-and-ownership.md), which ended on the question this entry answers: if
`unique_ptr` can't be copied, how does ownership ever change hands?

---

## The mental model: ownership moves, the object stays put

```cpp
auto a = std::make_unique<int>(42);
std::unique_ptr<int> b = std::move(a);
```

Prediction on record: *"move probably moves the location of the int?"* That's the natural reading
of the word, and it's wrong. Printing the addresses shows what actually happened:

```text
(before) a: 0x502000000010
(after)  b: 0x502000000010
(after)  a: 0
```

The `int` never moved. It sits at `...010` throughout. What moved is the **8-byte address**,
copied from `a` into `b`, after which `a` was set to null. Going back to the slip-of-paper picture
from [24](24-raii-and-ownership.md): the house stays where it is, and the slip is handed over.
The old holder is left with a blank slip.

Why null `a`? If it kept the address, both destructors would `delete` the same `int`, which is the
double free from 24, step 5. "Exactly one owner" is maintained by **emptying the source**.

This is also why moves are cheap. Moving a `unique_ptr` to a 1 GB buffer copies one pointer. A
*copy* of an owning object has to duplicate everything it owns (a **deep copy**). A move steals
the internals and leaves the source empty.

## Using a moved-from object

```cpp
std::cout << *a;   // after the move
```

`*p` **dereferences**: it goes to the address `p` holds and reads what's there. `a` holds `0`.

Prediction on record: *"it might just say heads up a is useless after the move."* Nothing warns
you. **It compiles cleanly under `-Wall -Wextra`.** How it fails depends on the build:

| Build flags | What you see |
| --- | --- |
| `-D_GLIBCXX_ASSERTIONS` | `unique_ptr.h:453: ... operator*() ... Assertion 'get() != pointer()' failed.` Abort. The library checked for null before dereferencing. |
| `-fsanitize=address` only | `AddressSanitizer: SEGV on unknown address 0x000000000000` ... `The signal is caused by a READ memory access.` `Hint: address points to the zero page.` |
| neither | `Segmentation fault`, and no line number. |

The ASan version *is* a segfault. ASan catches the signal and writes a report before the process
dies.

> **An address at or near zero in a crash report almost always means a null pointer was
> dereferenced.** Check this first when reading any crash report.

The standard's rule is that a moved-from object is in a *valid but unspecified* state. You can
destroy it, or assign it a new value. Don't read from it unless the type documents what's left.
`unique_ptr` does document it: null. Rust rejects use-after-move at compile time. C++ leaves it to
you, and to the sanitizers.

## Which constructor runs: the `Tracer` experiment

A class whose only job is to report which special member function ran:

```cpp
struct Tracer {
  Tracer()                         { std::cout << "const" << std::endl; }
  Tracer(const Tracer& other)      { std::cout << "copy"  << std::endl; }
  Tracer(Tracer&& other) noexcept  { std::cout << "move"  << std::endl; }
};
```

### A detour: the constructor that called itself

The first version was

```cpp
Tracer(const Tracer& other) : Tracer(other) { ... }
```

and the editor reported *constructor delegates directly or indirectly to itself*. After a
constructor's `:` comes the **member initializer list**, which runs before the body. When the thing
named there is another constructor of the same class, that's **delegation**: "run that
constructor on this object first." `Tracer(other)` with `other` a `const Tracer&` picks the copy
constructor, which is the constructor being defined. That's infinite recursion.

The next attempt, `: Tracer()`, compiled but made every copy print `const` and then `copy`, which
ruins the instrument. `Tracer` has no members, so nothing belongs after the colon.

Constructors **don't return anything**. By the time one runs, the memory for the object already
exists (a stack slot, or what `new` allocated). The constructor fills that memory in.

### The predictions

```text
Tracer a;                          const
Tracer b = a;                      copy
Tracer c = std::move(a);           move
std::vector<Tracer> v;             (nothing: an empty vector holds no Tracer)
v.push_back(b);                    copy
v.push_back(std::move(b));         predicted: copy    actual: move, move
```

Five of six were right. The last line is wrong twice.

**First,** `std::move(b)` made `push_back` pick its move overload. The prediction assumed
`push_back` copies no matter what.

**Second,** one `push_back` produced two constructions. Printing `v.capacity()` shows why: it was
`1` when the second element arrived. A `vector` keeps its elements in **one contiguous heap buffer**.
With no room left, it allocates a bigger buffer, **moves every existing element** into it, and
frees the old one. The second `move` is the old element being relocated.

(In libstdc++ the new element is built in the new buffer *first* and the old ones are relocated
after it. That's why the output reads "move (new element), move (relocated old one)".)

Relocating every element is O(n), which sounds bad. So `vector` doesn't grow by one: libstdc++
**doubles** the capacity (1, 2, 4, 8, ...). Reallocations get exponentially rarer, so the
average cost per `push_back` stays constant. If the final size is known, `v.reserve(n)` skips
reallocation entirely.

## The `noexcept` trap

`noexcept` was in the move constructor because an online tutorial had it. Delete it, and the
last line changes:

```text
push_back(move(b))...move
copy                                  ← was "move"
```

`noexcept` is a **promise that a function won't throw**. The compiler doesn't check it: if a
`noexcept` function throws anyway, the program calls `std::terminate`. But code can *ask* at
compile time whether a function is `noexcept`, and `vector` does.

The reason is reallocation halfway through. Say element 500 of 1000 fails:

- **Copying** leaves the old buffer untouched. `vector` throws away the half-built new buffer, and
  the container is exactly as it was before the `push_back`. This is the **strong exception
  guarantee**: the operation either succeeds or has no effect.
- **Moving** empties each source as it goes. Elements 1–499 in the old buffer have already been
  emptied, and moving them back could throw too. There's no way back to the original state.

So `vector` relocates with `std::move_if_noexcept`: **move if the move constructor is
`noexcept`, otherwise copy.** A slow copy can be undone. A fast move might not be.

Explained back in session: *"it copies because it's too risky to try and move and get an error for
it."* The corrected version: what's lost isn't the addresses but the **contents** of the
moved-from elements.

**Two separate decisions are made here, and the output shows both:**

1. **The element being pushed** is built from whatever you pass. `push_back(b)` copies;
   `push_back(std::move(b))` moves. `noexcept` doesn't matter for this one.
2. **The existing elements**, during reallocation, are moved only if the move is `noexcept`.

### Do you have to write `noexcept` yourself?

Usually not. If a class declares **none** of the destructor, copy constructor, copy assignment,
move constructor, or move assignment, the compiler generates the moves. A generated move is
`noexcept` whenever every member's move is. `std::string`, `std::vector`, and `std::unique_ptr` all
qualify:

```cpp
struct Z { std::string s; std::vector<int> v; std::unique_ptr<int> p; };
std::is_nothrow_move_constructible_v<Z>   // 1
```

This is the **Rule of Zero**: build classes out of members that already manage themselves, write
none of the five, and you get correct, fast moves for free.

Two ways to lose the fast move:

- **Hand-write a move constructor and forget `noexcept`.** Every reallocation silently becomes a
  full copy.
- **Declare a destructor** (even an empty one) **or a copy constructor.** That suppresses the
  implicit move entirely:

  ```cpp
  struct D { std::string s; ~D() {} };
  std::is_nothrow_move_constructible_v<D>   // 0: "moves" now go through the copy constructor
  ```

  `struct T` in [24](24-raii-and-ownership.md) has a destructor and a deleted copy, so it has
  **no move at all**. It can't be copied or moved.

**Either way nothing reports it: no error, no warning, just slower code.** For a class owning a
large buffer, that's a deep copy of every element each time the container grows. It's the
syllabus's "why copies are expensive" showing up in real code.

## What `std::move` actually does

With the move constructor deleted from `Tracer` and only the copy constructor left:

```text
c = move(a)...copy
```

`std::move` was written, and a copy ran. No error.

This took four guesses in session: "making a copy then deleting the old bits", "copies its
contents and changes its address", "changes it into a pointer". All three describe **runtime
work**, and `std::move` has none. **It compiles to zero instructions.** Something that emits no
instructions can only change what the *compiler* believes. So it's a cast:

```cpp
std::move(a)   ≡   static_cast<Tracer&&>(a)
```

`Tracer&&` is an **rvalue reference**: a reference that binds only to things marked "temporary,
safe to steal from." A temporary such as `Tracer()` qualifies on its own. A **named variable
doesn't**, because the compiler assumes you might still use `a`. `const Tracer&`, by contrast,
binds to anything, including temporaries.

So overload resolution for `Tracer c = <expr>`:

| Expression | Move ctor `Tracer(Tracer&&)` | Copy ctor `Tracer(const Tracer&)` | Runs |
| --- | --- | --- | --- |
| `a` | can't bind (named) | binds | copy |
| `std::move(a)`, move ctor exists | binds, **better match** | binds | move |
| `std::move(a)`, no move ctor | — | binds | copy; `a` untouched |

> **`std::move` doesn't move. It gives permission, and the constructor decides what happens.**

Every effect seen today came from the **constructor that was chosen**. `unique_ptr`'s move
constructor nulled `a`. `Tracer`'s copy constructor takes `const&`, so it *couldn't* modify `a`,
and it didn't. The emptying is the move constructor's job, not `std::move`'s.

Explained back in session: *"move tells the compiler... we can run move if avail otherwise copy,
where copy only gets a reference so it can't delete things, and move gets an rvalue reference which
is safe to take."* Two corrections:

- It's the **`const`** that stops the copy constructor from modifying the source. A plain
  `Tracer&` could modify it.
- `std::move` isn't consulted "in the event a move is supposed to happen." It's **what makes a
  move eligible at all.** Without it, a named variable always goes to the copy.

## The rules

- **After `std::move(x)`, treat `x` as empty.** Destroy it or assign to it; don't read it.
- **Hand-written move constructor ⇒ `noexcept`.** Otherwise containers copy instead of moving.
- **Prefer the Rule of Zero.** Members that manage themselves (`unique_ptr`, `vector`, `string`)
  give correct, `noexcept` moves with no code. Writing a destructor "just to be safe" disables them.
- **Writing `std::move` guarantees nothing.** If the type has no move constructor, you get a copy
  and no message. When it matters, check with a tracer or `static_assert(std::is_nothrow_move_constructible_v<T>)`.
- **`reserve` when the size is known.**
- **Keep `-D_GLIBCXX_ASSERTIONS` and ASan in debug builds.** They turned a silent null
  dereference into a report naming the line.

## Open questions

- **Returning a local by value** (`Tracer make() { Tracer t; return t; }`): copy, move, or
  neither? This was on the plan and got skipped. The answer involves *copy elision*, which is
  when the compiler builds the object directly in the caller's slot and runs no constructor at all.
- **Move assignment** (`b = std::move(a)` where `b` already exists) is the fifth special member.
  What does it have to do with what `b` already owned?
- **Rule of Five**: 24's Rule of Three plus the two move operations. When is writing all five
  correct, rather than zero?
- **`shared_ptr`**: copying one doesn't copy the pointee. What does it copy?

## Where this returns

ROS 2 publishers take messages as `std::unique_ptr<Msg>` so a large message (an image, a point
cloud) can be **moved** into the middleware without copying the payload. `publish(std::move(msg))`
is idiomatic, and `msg` is null afterwards, the same moved-from state as `a` here. The week 6
thread work moves `std::thread` objects, which can't be copied, only moved, for the same one-owner
reason as `unique_ptr`.
