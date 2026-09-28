# 30 — Templates vs abstract classes: when the type gets decided

**Week 5.** Syllabus item: *Templates — enough to read them, not to write clever ones.* Also sets
up Boss Fight #2 (week 7): *add a sensor type without modifying the core.*

Prompted by setting the week-5 end state. The instinct was "somewhere there's gotta be a template
or an abstract class," followed by "idk exact difference... that's just the vibe." The vibe is
right: both let one piece of code serve many types. The difference is **when the type is
decided.**

---

## Template: decided at compile time

```cpp
template <typename T>
T biggest(const std::vector<T>& v) { /* ... */ }

biggest(ints);     // compiler generates biggest<int>
biggest(doubles);  // and, separately, biggest<double>
```

A template is not a type or a function. It's a **recipe**. Each use with a new `T` makes the
compiler stamp out a new, independent copy. `biggest<int>` and `biggest<double>` are two unrelated
functions in the binary.

The types need nothing in common except that the code compiles for them (here, `<` must work).
There's no base class and no declared interface. The requirement is implicit, which is why
template errors are famously long: the compiler reports the failure deep inside the recipe.

## Abstract class: decided at runtime

```cpp
struct Shape {
  virtual double area() const = 0;   // "= 0": pure virtual, so Shape is abstract
  virtual ~Shape() = default;        // needed when deleting through a Shape*
};
struct Circle : Shape { double area() const override { /* ... */ } };
struct Square : Shape { double area() const override { /* ... */ } };

std::vector<std::unique_ptr<Shape>> shapes;   // Circles and Squares, mixed
for (auto& s : shapes) s->area();             // which area()? looked up at runtime
```

There's one copy of the calling code. Each object carries a hidden pointer to its type's function
table (the **vtable**), and `s->area()` follows it at runtime. The interface is explicit: a type
has to inherit from `Shape` and implement `area()`, and `override` makes the compiler check it.

## Side by side

| | Template | Abstract class |
| --- | --- | --- |
| Type decided | Compile time | Runtime |
| Mixed types in one container | No | Yes, through pointers |
| Types must share a base | No | Yes |
| Interface | Implicit ("whatever compiles") | Explicit (the pure virtuals) |
| Cost | Code duplicated per `T`; long errors | Indirect call; objects usually on the heap |

## The check question, and the half-right answer

*Why can't a `std::vector<SensorBuffer<T>>` hold both the IMU buffer and the temperature buffer?*

The first answer given was **size**: the compiler needs to know how much space each element takes.
That's a real constraint (a `vector` stores elements back to back at a fixed stride) but not the
root cause. A counterexample: a buffer that holds a `std::vector` plus a couple of integers has
the same `sizeof` whatever `T` is, since a `std::vector` is three pointers. The two buffers can
be **identical in size** and still can't share a container.

The root cause is that **`SensorBuffer<IMUReading>` and `SensorBuffer<TempReading>` are unrelated
types.** `std::vector<SensorBuffer<T>>` doesn't even compile until `T` is named, and once it's
named, the vector holds that one type. To the compiler the two buffers are as unrelated as `int`
and `std::string`.

To mix them you need a type they both *are*: a common base, stored through pointers, where the
pointers really are all the same size. That's where the size instinct was pointing, and it's why
the example above holds `unique_ptr<Shape>`, not `Shape`.

## Where each fits in this project

- **One kind of reading per buffer** is template-shaped: `SensorBuffer<IMUReading>`,
  `SensorBuffer<TempReading>`. Week 5.
- **A bus that carries every sensor through one path** is where the abstract class question comes
  in. That's week 7 and Boss Fight #2, so the design is left open here on purpose.

Both are often used together: a templated container with a small abstract base for the part that
has to be uniform at runtime.

## Open questions

- What does a `SensorBuffer<T>` require of `T`? Write the list down. That list is the implicit
  interface, and C++20 *concepts* are how you make it explicit.
- For the week-7 bus: which operations actually need to be uniform across sensors? That list is
  the abstract base, and if it's empty, you don't need one.

## Where this returns

- ROS 2 publishers and subscribers are templates on the message type
  (`create_publisher<sensor_msgs::msg::Imu>`). Nodes are a class hierarchy (`rclcpp::Node`).
- Week 7 bus, Boss Fight #2.
