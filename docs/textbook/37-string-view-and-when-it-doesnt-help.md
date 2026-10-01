# 37 — `string_view`, and when it doesn't help

**Week 5.** Syllabus item: *vector, unordered_map, string_view, optional*. Prompted by changing
`Robot::get_temperature_sensor_buffer(const std::string&)` to take a `std::string_view`, and the
compile error at `_temperature_sensor_buffers.at(buffer_name)`. Related:
[36](36-maps-optional-and-the-copy-nobody-asked-for.md) (the map and `at`),
[23](23-converting-constructors-and-explicit.md) (`explicit` on the strong types).

---

## The mental model

A `std::string_view` is **a pointer and a length**, aimed at characters someone else owns. It
copies nothing and allocates nothing. It's read-only, and it can view a `std::string`, a string
literal, or part of either (`substr` on a view is just a new pointer and length).

A `std::string` **owns** its characters. Building one means getting memory and copying every
character into it.

## Why the conversion is explicit

`string_view → string` compiles only when written out: `std::string(view)`. The surprise was
reasonable — *"we're just trying to find the key with that string"* — but `at()` takes
`const key_type&`, and `key_type` is `std::string`. To call it, a real `std::string` has to exist.

The first guess at the reason was "a view isn't actually a string." Close, but a view really does
point at characters. The reason is **cost**: constructing a string copies, and the standard won't
copy silently. It's the same rule as the week-3 strong types, where `explicit` stopped five
swapped strings from converting without anyone noticing. Expensive or surprising conversions
should be visible at the call site.

## Counting the copies

New `std::string` objects constructed per call:

| Caller passes | `const std::string&` param | `string_view` param + `at(std::string(v))` |
| --- | --- | --- |
| a `std::string` it already has | **0** — the reference binds to it | **1** — the conversion |
| a literal, `"cpu"` | 1 — a temporary to bind to | 1 — the conversion |

So in this function `string_view` **ties or loses**. Every call has to end at a `std::string`
key, and the view only delays the copy. The first answer (one before, two after) counted the
caller's own string as well; with that included it's right for the first row, and it missed that
the literal case is a tie.

(Footnote: short strings like `"cpu"` fit inside the `std::string` object itself — the small
string optimisation, about 15 chars in libstdc++ — so neither column touches the heap here. The
copy still happens; the allocation doesn't. Count copies, not `malloc`s.)

## When it does help

`string_view` wins when the function **only reads** the characters and never needs to own them:

- parsing: splitting a CSV line into fields without making a string per field
- comparing, searching, printing
- taking a prefix or suffix (`substr` on a view copies nothing)

Rule of thumb: **if the body ends in a `std::string` anyway, take `const std::string&`.** If it only
looks, take `std::string_view` by value (it's two words; pass it like an `int`).

## The danger: it doesn't own

A view outlives what it points at as easily as a reference does — see the dangling reference in
week 3. Never return a `string_view` into a local or a temporary, and never store one in a member
unless something guarantees the owner lives longer.

```cpp
std::string_view name() { std::string s = "cpu"; return s; }   // dangles: s is destroyed
```

## Open: heterogeneous lookup

The standard did eventually fix the original complaint. C++20 lets `unordered_map::find` and
`contains` take a `string_view` directly, *if* the map is declared with a transparent hash and
`std::equal_to<>`. `at()` only got the same overload in C++26. This project is on C++17, and the
extra declarations aren't worth it for a lookup called a handful of times — but it's the answer
to "why can't I just look it up with a view."

## Where it returns

Week 7: parsing bytes off a socket is exactly the read-only, no-ownership case. ROS 2 message
handling in Part 4 too.
