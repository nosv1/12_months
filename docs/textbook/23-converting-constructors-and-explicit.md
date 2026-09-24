# 23 — Converting constructors and `explicit`

**Week 3.** Syllabus item: *Classes, constructors, destructors*.

Prompted by writing the `cpp_telemetry` README. The Strong types section claimed wrapping each field
in its own type (`RobotID`, `Timestamp`, `Velocity`, …) made swapped arguments a compile error. A
five-line test said otherwise: it compiled, ran, and silently stored a robot ID in the timestamp.

Follows [22 — Parsing input that fights back](22-parsing-input-that-fights-back.md), whose open
questions raised strong types.

---

## The bug

```cpp
struct Timestamp { std::string v; Timestamp(std::string v) { this->v = v; } };
struct RobotID   { std::string v; RobotID(std::string v)   { this->v = v; } };
// ... Velocity, Battery, Temperature likewise, each taking std::string

std::string a = "amr-01", b = "2026-09-03T...", c = "0.9", d = "95.0", e = "31.2";
Reading r(a, b, c, d, e);   // timestamp and robot_id swapped
```

Prediction on record: *"it won't compile — wrong types in the constructor."* Result: compiles, runs,
`r.timestamp.v == "amr-01"`.

The strong types had been protecting the project all along, but not for the reason assumed. The
parser happens to write `Timestamp(row[0]), RobotID(row[1]), …` — naming every type at the call
site. **The protection was in the call site's habits, not in the types.** Anyone calling the
constructor with plain strings got no protection at all.

## The mental model: a one-argument constructor is a conversion rule

A constructor that can be called with a single argument does two jobs:

1. It builds the object when you ask: `RobotID id(s);`
2. It **tells the compiler how to turn that argument type into this type**, and the compiler will
   use that rule on its own whenever it has the argument type and needs this one.

The second job is called a **converting constructor**. `RobotID(std::string)` declares "any
`std::string` may become a `RobotID`." `Reading` needs a `Timestamp` in position 1, it has a
`std::string`, and there is a declared rule, so the compiler applies it. Same for every other
position. Five strings, five silent conversions, no error.

Every wrapper type took `std::string`, so **every wrapper type accepted every string**. The types
were distinct to the programmer and interchangeable to the compiler.

## The fix: `explicit`

```cpp
struct RobotID { std::string v; explicit RobotID(std::string v) { this->v = v; } };
```

`explicit` removes job 2 and keeps job 1. The constructor can still be called — you just have to
write the call. `RobotID(s)` and `RobotID{s}` work; handing a bare `std::string` to something that
wants a `RobotID` does not:

```text
error: no matching function for call to ‘Reading::Reading(std::string&, std::string&)’
```

**`explicit` forbids something; it doesn't check anything.** It doesn't "make sure the right type
is passed." It stops one specific automatic conversion — from the parameter type into this type —
so that the conversion only happens when written out.

### Where it goes: on the type being converted *into*

The first attempt put `explicit` on `Reading`'s constructor. Nothing changed. That's correct
behaviour, and the reason is the whole model:

- In `Reading r(a, b, c, d, e)`, nothing is converted **into** a `Reading` — its constructor is
  called directly, which is always allowed.
- The silent conversions were `std::string → Timestamp`, `std::string → RobotID`, and so on — one per
  **argument**. Whether those are allowed is decided by each argument type's own constructor.

So `explicit` on `Reading` forbids implicit conversions *to* `Reading`. There are some, and it
does block them — they just weren't the bug:

```cpp
Reading r = {Timestamp(b), RobotID(a)};   // copy-list-init: error if Reading's ctor is explicit
take_reading({Timestamp(b), RobotID(a)}); // same: braced list converted to a Reading parameter
```

```text
error: converting to ‘Reading’ from initializer list would use explicit constructor
```

## What `explicit` does not buy

```cpp
Reading r(Timestamp(a), RobotID(b));   // compiles with explicit everywhere; data still swapped
```

Strong types catch arguments **in the wrong position**. They cannot catch **correctly labelled
wrong data** — if the call site names the wrong column, the compiler takes the label at its word.
The type system moved the mistake from "positional" to "labelling," which is a real improvement
(labelling mistakes are visible on the line where they happen), not an elimination.

## A limit that was already there: one user-defined conversion

Even *without* `explicit`, this never compiled:

```cpp
Reading r("amr-01", "2026-09-03T...");   // error, explicit or not
```

A string literal is a `const char[N]`. Getting to `RobotID` needs two user-defined conversions:
`const char* → std::string` (a `std::string` constructor) and then `std::string → RobotID`. C++
allows at most **one** user-defined conversion per argument in an implicit conversion sequence. So
the hole only opened when the arguments were already `std::string` — which, in a CSV parser, they
always are.

## The rule

**Mark every single-argument constructor `explicit` unless you specifically want implicit
conversion.** Implicit conversion is right for types that genuinely *are* the other type in a new
form — `std::string` from `const char*` is the classic case, which is why `std::string`'s
constructor isn't `explicit`. A `RobotID` is not "a string in a different form." It's a string with
a meaning, and the whole point of the wrapper is that other strings don't have that meaning.

This is enforced by tooling in most codebases:

- **clang-tidy**: `google-explicit-constructor` (also catches conversion operators).
- **Google C++ style guide**: implicit conversions off by default; single-argument constructors
  `explicit`.

Default to `explicit`; justify its absence.

## Open questions

- **Conversion operators** (`operator double() const`) are the same idea in the other direction —
  `Velocity` silently becoming a `double` — and take `explicit` the same way. Not used here yet.
- **Multi-argument constructors** can take `explicit` since C++11. It matters only for braced
  copy-list-initialization (above). Whether to apply it by default is a style-guide argument, not a
  correctness one.
- **Strong-type libraries** (`NamedType`, `type_safe`) generate these wrappers, `explicit` included,
  plus opt-in arithmetic. Not worth a dependency for five fields; worth knowing exists.

## Where this returns

ROS 2 message types are structs with many same-typed fields (`geometry_msgs/Twist` is six doubles),
and units (metres vs millimetres, radians vs degrees) are the classic robotics bug. The same idea —
make "wrong kind of number" a compile error — is what unit libraries like `mp-units` do at scale.
Week 5 (STL and idiom) touches templates, which is how those libraries are built.
