# 21 — Values, references, pointers, and `const`

**Week 3.** Syllabus items: *References vs pointers vs values*; *`const` correctness*.

Prompted by a copy constructor with an empty body that made a struct's `robot_id` print blank, and
by the guess that `Reading b = a;` stores "how to create a Reading" in `b`.

Follows [20 — The four stages of a build](20-the-four-stages-of-a-build.md).

---

## The mental model: a variable *is* the object

This is the break from Python, and almost every confusion below is a symptom of it.

In Python, a name is bound to an object that lives somewhere else. Two names can be bound to the
same object, and nothing is ever copied unless asked for:

```python
def f(r):
    r.temperature = 999

a = Reading("a", t, 1.0)
f(a)
a.temperature      # 999
```

In C++, `a` is not a name pointing at a `Reading`. `a` **is** the `Reading` — a chunk of memory
holding a `std::string`, a `time_t`, and a `double`. Handing it to a function that takes a
`Reading` by value builds a *second, independent* `Reading`:

```cpp
void f(Reading r) { r.temperature = 999; }

Reading a("a", t, 1.0);
f(a);
a.temperature;     // 1.0 — untouched
```

Everything else follows from that one fact.

---

## Copy construction

**Copy construction** is building a new object initialized from an existing object of the same
type. It is not assignment, and it is not rare.

These all copy-construct:

```cpp
Reading b = a;          // yes — this is construction, despite the =
Reading b(a);           // identical to the above
Reading b{a};           // identical again; modern style prefers this spelling
f(a);                   // a by-value parameter
return local_reading;   // returning by value (often elided — see below)
v.push_back(a);         // std::vector stores by value
```

### Construction vs assignment

```cpp
Reading b = a;   // copy CONSTRUCTOR   — b does not exist yet
b = a;           // copy ASSIGNMENT    — b exists, is being overwritten
```

The `=` on the first line performs no assignment. It is *copy-initialization*; the `=` is pure
syntax. This is a genuine wart in the language and experienced C++ programmers have to consciously
remember it.

**The rule that disambiguates:** if the line starts with a **type name**, it's construction. If it
starts with an **already-declared variable**, it's assignment.

### Why C++ splits them at all

Python has no analogue because `b = a` rebinds a name and nobody's memory is touched. C++ has to
distinguish two genuinely different situations:

| | Memory before | What must happen |
| --- | --- | --- |
| **Construction** | raw, uninitialized | build contents from scratch |
| **Assignment** | a live, valid object | *release* the old contents, then install new ones |

That second row is the entire reason. If `robot_id` is a `std::string` holding `"b"`, that string
owns a heap allocation; overwriting the object must free it first. A constructor never has to,
because there was nothing there.

### The compiler writes one for you

Declare no copy constructor and the compiler generates one whose body is "copy every member, in
declaration order." For a struct of a `std::string`, a `time_t` and a `double`, that is correct —
and **silent**, which is the problem when trying to learn where copies happen.

### The signature, and why it must be a reference

```cpp
Reading(const Reading &other);
```

The parameter cannot be taken by value:

```cpp
Reading(Reading other);   // rejected by the compiler
```

To call that, C++ would have to construct `other` from the argument — which means calling the copy
constructor — which means constructing *its* parameter — forever. GCC rejects it outright rather
than emitting infinite recursion, with an error that names the fix:
`invalid constructor; you probably meant 'Reading (const Reading&)'`.

A reference is the only way to get hold of the source object without performing the very operation
being defined.

The `&` is **required**. The `const` is a separate, near-universal choice: a promise not to modify
the object being copied from.

### The bug that prompted this entry

```cpp
Reading(const Reading &other)
{
}
```

Correct signature, empty body. `Reading b = a;` then compiled and ran, and `b.robot_id` printed
**blank**.

Not a placeholder, not a deferred construction — the copy constructor was called, and it was told
to do nothing. `robot_id` came out empty rather than garbage because **members are constructed
before the constructor body runs**: `std::string` is a class, so it got its own default constructor
and became `""`. `temperature` and `timestamp` are primitives, so nobody initialized them at all.

That asymmetry — class members default-constructed, primitives left as garbage — is the reason
member initializer lists exist. Assigning in the body is not initialization; it is overwriting
whatever initialization already happened.

### Make copies visible

The same move as printing in a destructor to make lifetime visible
([20](20-the-four-stages-of-a-build.md)): give the copy constructor a `std::cout` line. Copies stop
being invisible, and questions like "how many objects did that call create?" become observable
instead of theoretical.

---

## Passing: value, reference, const reference

Three functions differing only in the parameter:

```cpp
void by_value(Reading r);           // copies
void by_ref(Reading &r);            // no copy, may modify the caller's object
void by_const_ref(const Reading &r);// no copy, may not modify
```

Called on the same object, with a printing copy constructor in place, only `by_value` produces a
`copy` line. A reference is an alias for the object already sitting there; nothing is constructed.

### The aliasing hazard

`by_ref(a);` and `by_value(a);` are **identical at the call site**. One of them can reach back into
the caller and rewrite `a`; the other cannot. Nothing where the call is written says which.

Python always has the first behavior, so there is nothing to choose. C would have required `&a` at
the call site, making it visible. C++ makes it invisible — so the signature is the only
documentation, which is why it matters what the signature says.

### `const&` is the default

For anything non-trivial, `const Reading&` is the parameter type to reach for:

- No copy. A by-value `Reading` heap-allocates and copies a string on every call, for nothing.
- No permission granted. `Reading&` is an unsigned permission slip to modify the caller's object.

Reach for `Reading&` only when modification is the point, and justify it.

### The inversion from Rust

Rust: `&T` and `&mut T` — **immutable by default, opt in to mutation.**
C++: `T&` and `const T&` — **mutable by default, opt out.**

Same two concepts, opposite defaults. In Rust the discipline is free; in C++ it is a habit that has
to be maintained. This is why `const`-correctness is a practice in C++ and merely the ground state
in Rust.

---

## Dangling references

The hazard with **no Python equivalent at all**.

In Python, if anything still refers to an object, the object stays alive — that is what the
garbage collector is for. Holding a reference to a dead object is structurally impossible.

**A C++ reference keeps nothing alive.** It is an alias to memory someone else owns. When the owner
dies, the reference remains, naming memory that now holds something else.

```cpp
Reading& make_reading()
{
    Reading r("temp", 0, 42.0);
    return r;              // r is destroyed at this brace
}
```

`r` is already dead by the time the function returns. With a printing destructor, `goodbye temp`
appears *before* the caller ever reads the value. Nobody kills the object later; nobody owns it,
and nobody ever will. **A reference confers no ownership and extends no lifetime.**

The compiler catches this one statically:

```text
warning: reference to local variable ‘r’ returned [-Wreturn-local-addr]
```

### What actually happened at runtime

The naive story — "you read stale bytes off a dead stack frame" — is not what GCC did. Printing the
reference's address gives **`0`**. GCC saw a local's address returned, concluded the program is
meaningless, and emitted a null reference. Dereferencing it segfaults immediately.

That is undefined behavior made concrete: the compiler did not preserve the broken code, it
*replaced* it. A different compiler, or `-O2`, or a slightly different function, and the stale-`42`
version appears instead — which is far worse, because it looks like it works.

**The warning is the signal. The runtime symptom is a coin flip.**

### The rule worth carrying

- A reference **parameter** is safe. The caller's object outlives the call, by construction. Use
  `const&` params freely and without anxiety.
- A reference that is **returned or stored** is where lifetime has to be reasoned about. Who owns
  the object, and does it outlive the reference?

References are not the dangerous thing; lifetime is. A pointer dangles identically *and* can be
null. Of the two, the reference is the safer.

---

## References vs pointers

Both can modify the caller's object — that part is not the distinction:

```cpp
void by_ptr(Reading* r) { r->temperature = 999; }   // called as by_ptr(&a)
```

| | can be null | can be reseated | syntax | call site |
| --- | --- | --- | --- | --- |
| `Reading&` | no | no | `.` | `f(a)` |
| `Reading*` | yes | yes | `->` | `f(&a)` |

Also: pointer arithmetic exists, and pointers can be stored in a `std::vector` while references
cannot.

Reach for `*` when the value is genuinely optional, or when it must point at different objects over
time. Otherwise `const&`.

### A reference cannot be rebound

The misconception the syntax actively encourages:

```cpp
int i = 1;
int j = 2;
int& r = i;

r = j;

// i == 2, j == 2, r == 2
```

Not `1, 2, 2`. **`r = j` sets `i` to `2`.**

There is no syntax in C++ that rebinds a reference. Once bound, **every use of a reference *is* the
referent** — it has no separate identity. `r = j` means `i = j`. `r++` means `i++`. Even `&r` yields
`&i`.

"Reference" is a slightly misleading name for this. After `int& r = i;`, `r` is a **second name for
`i`**, and nothing more.

The pointer has both operations and makes the choice explicit:

```cpp
int* p = &i;
p = &j;     // rebind — p points at j; i untouched
*p = j;     // assign through — writes j's value into whatever p points at
```

The reference cannot express the first, so `=` can only ever mean the second.

---

## `const` member functions

The motivating failure. A member function that only reads:

```cpp
double as_fahrenheit();               // in the struct
```

called on a `const Reading&`:

```cpp
void by_const_ref(const Reading &r)
{
    std::cout << r.as_fahrenheit() << std::endl;   // does not compile
}
```

GCC:

> `error: passing ‘const Reading’ as ‘this’ argument discards qualifiers [-fpermissive]`

The editor's linter (clangd) says the same thing in different words, and this is the one likely to
appear first:

> `the object 'r' has type qualifiers that are not compatible with the member function`

Both mean: the object is `const`, the function doesn't promise to be.

### Why — the compiler never reads the body

Every non-static member function has a hidden first parameter, `this`. As declared above, that
parameter is `Reading*` — non-const. Calling it on a `const Reading` would silently launder the
`const` away, so the compiler refuses **regardless of what the body does**.

That is deliberate. `const` is part of the **interface contract**. If it were inferred from the
body, adding one line to that body later would silently break every caller. Instead the promise is
stated up front, and the compiler enforces it against the implementation too.

### The fix

```cpp
double as_fahrenheit() const;                        // declaration, reading.h
double Reading::as_fahrenheit() const { /* ... */ }  // definition, reading.cpp
```

The `const` goes in **both** places or the definition doesn't match the declaration and the linker
complains — the same class of failure as [20](20-the-four-stages-of-a-build.md).

Inside a `const` member function, `this` is `const Reading*`, so `this->temperature = 5;` is a
compile error there too.

### `const` describes the access path, not the object

Worth holding onto, from the error's wording — *"assignment of member in read-only object"*:

The object is not read-only. `a` is a perfectly mutable `Reading` sitting in `main`. The `const` is
on the **reference**, so the same object is writable through one handle and read-only through
another, at the same time.

### `const`-correctness is bottom-up

`const Reading&` parameters are only usable if the member functions they need are marked `const`.
One unmarked getter and the whole chain collapses — and the reflexive fix is to delete the `const`
from the parameter, which spreads the rot upward instead of down.

**Working rule: mark every member function `const` that does not modify the object.** Getters,
formatters, comparisons, anything that computes a value. Do it while writing them, not later.

---

## Open questions, deliberately deferred

- **Copy elision and move semantics.** Returning by value is often free, which undercuts the "avoid
  copies" instinct in exactly one place. Week 4.
- **The Rule of Three/Five.** The generated copy constructor is correct here because every member
  knows how to copy itself. When a class owns a raw pointer or a file handle, memberwise copy gives
  two objects that believe they own the same resource, and a double-free. Week 4 — memory and
  ownership.
- **Member initializer lists.** Assigning in the constructor body runs *after* members are already
  initialized. For a `std::string` that is a wasted construction; for a `const` member or a
  reference member it is impossible.
- **Temporaries.** `const Reading&` binds to a temporary and `Reading&` does not. Related to why
  `const&` is the default, and to how `make_reading()` behaves at a call site.

## Where this returns

Week 4 (memory and ownership) turns the lifetime question from a hazard into the main subject:
`unique_ptr`, `shared_ptr`, and who is allowed to destroy what. Every ROS 2 node from week 6 onward
passes messages by `const&` or by shared pointer, and the choice between them is this entry's
material at a larger scale.
