# 33 — Writing a class template: one recipe, requirements nobody writes down

**Week 5.** Syllabus item: *Templates — enough to read them, not to write clever ones.* The
concept is [30](30-templates-vs-abstract-classes.md); this is what it took to actually convert
`IMUBuffer` into `SensorBuffer<T>`.

Prompted by the refactor, which went wrong twice in the same instructive way.

---

## What depends on the type?

Before touching code: *which parts of `IMUBuffer` depend on it being IMU data?* Answer: none of
the logic, only the names. A ring buffer never looks inside a reading. That's what makes it
template-shaped.

## The misconception: bodies per type

First attempt: the class got `template <typename T>`, but every member definition said
`SensorBuffer<IMUReading>::`. Second attempt: the same, with `TempReading` swapped in.

Both write bodies for **one** type. Every other `T` gets a declaration and no functions. (It also
isn't valid C++: specialising a member for one type needs `template <>`.)

The idea that was missing: **the bodies are written once, in terms of `T`.** `T` isn't only for
the class declaration; it's a name usable anywhere in the member functions. The compiler generates
the `IMUReading` version, the `TemperatureReading` version, and any other, from that single set.

```cpp
template <typename T>
class SensorBuffer {
  std::vector<T> _readings;
  void _add_reading(const T& reading);
  // ...
};

template <typename T>                         // repeated on every out-of-class definition
void SensorBuffer<T>::_add_reading(const T& reading) { /* uses T, never a concrete type */ }
```

Check: the finished `sensor_buffer.h` mentions no reading type and includes no reading header.

**Where does `TemperatureReading` get declared, then?** Not in the buffer header. The concrete
type is supplied where the buffer is *used*: the test or `main` includes both `sensor_buffer.h`
and `temperature_reading.h`, writes `SensorBuffer<TemperatureReading>`, and the compiler
instantiates it there.

## Bodies go in the header

The compiler instantiates `SensorBuffer<IMUReading>::_add_reading` at the point of use, so it
needs the **body** there, not just the declaration. Leave the bodies in a `.cpp` and it compiles,
then fails at link time: `undefined reference to SensorBuffer<IMUReading>::...`.

So `imu_buffer.cpp` was deleted and removed from `add_library`. Bodies in a header feels wrong
after [31](31-operators-const-this-and-what-a-header-promises.md)'s multiple-definition error, but
templates are exempt from that rule; `<vector>` is written the same way. Standard layout: class at
the top, definitions below, one file.

## The implicit requirements on `T`

A template has no interface listing what `T` must do. The requirements are **whatever the code
happens to do to a `T`**. "It's just holding readings" hides them. Line by line:

| Line | Operation on `T` | Required by |
| --- | --- | --- |
| `_readings.push_back(reading)` | copy-**construct** into a new slot | buffer |
| `_readings[i] = reading` | copy-**assign** over a live object | buffer (only because it wraps) |
| `EXPECT_EQ(got, expected)` | `operator==`, element by element | tests only |

Construction and assignment are different operations, and a type can have one without the other.
A `const` member or a reference member makes a type non-assignable: `push_back` would still
compile, and the error would appear only in the overwrite branch, reported deep inside the
template.

`operator==` is a requirement of the **tests**, not the buffer. `SensorBuffer<T>` compiles for a
`T` without it; you just can't assert on it.

## A declaration that's never defined links fine, until it's used

`TemperatureReading` was written with its `.cpp` missing from `add_library`, and `operator<<`
declared but never defined. Everything built and passed, because nothing called either. The
first test compiled against it only checked a field, so it couldn't fail and couldn't expose the
link problem. A test that uses the type **through the buffer with `EXPECT_EQ`** is what exercises
`operator==`, and so what proves the second type actually works.

Same trap as the template bodies, from the other direction: there the definition existed but
wasn't visible; here it was visible but never compiled.

## Naming

`TempReading` was read as "temporary reading." Fair reading. Renamed `TemperatureReading`. A name
that confuses its author on day one confuses everyone later.

## Open

- A C++20 `concept` can state the requirements on `T` explicitly and give a short error instead
  of a long one. The lab is on C++17. Worth knowing it exists, not needed this week.
- Week 7 (Boss Fight #2) is where one path has to carry every sensor type. Whether that's this
  template, an abstract base, or both is left open on purpose.
