# Telemetry (C++)

A toy program that reads robot telemetry from a CSV file and prints per-robot temperature
statistics. It is a scoped C++ port of the Python version in [`/telemetry`](../telemetry). The
purpose of the port was to review the language, not to extend the functionality.

## Setup and running

```bash
cmake -B build
cmake --build build
./build/telem
```

Run from this directory. The CSV path is relative to the working directory, not to the binary.

Requires a C++17 compiler and CMake 3.16+. No other dependencies.

## Input format

Data is read from a CSV file: [`data/sample_telemetry.csv`](data/sample_telemetry.csv).

| Column | Type |
| --- | --- |
| `timestamp` | ISO 8601, stored as a string |
| `robot_id` | string |
| `velocity` | double |
| `battery` | double |
| `temperature` | double |

Because the objective was C++ structure rather than data validation, parsing a row into a
`Reading` checks only two things: that the row has exactly five columns, and that each numeric
field can be converted to a `double`.

## Output format

```text
Readings: 359            # total accepted readings
Rejected readings: 3     # rows with the wrong column count or an unparseable field
amr-01 -- 120 readings   # robot ID and number of accepted readings
min: -273.2              # minimum temperature
max: 33                  # maximum temperature
avg: 28.1242             # mean temperature

...[repeated per robot]...
```

## Architecture

- **Reader:** reads the CSV file into a `vector<vector<string>>` (`data`).
- **Parser:** converts `data` into a `ParsedLines`, which holds the accepted readings as a
  `vector<Reading>` and the rejected rows as `bad_rows`, a `vector<vector<string>>`.
- **Reading:** one parsed row. `timestamp` and `robot_id` are stored as strings; `velocity`,
  `battery`, and `temperature` are stored as strong types (`Velocity`, `Battery`, and
  `Temperature`), each of which holds its value as a `double`.
- **Grouper:** groups readings into a `map<string, vector<Reading>>` keyed by `robot_id`.
- **Analysis:** iterates over each robot's readings and computes the minimum, maximum, and mean
  temperature, returned as a `TemperatureAnalysis`. Returns `std::nullopt` if the robot has no
  readings.

## Design decisions

Three questions were posed before any code was written. Each has the answer given beforehand
(pre) and the answer after implementation (post), recorded verbatim.

1. **What owns the collection of readings?** How do per-robot statistics accumulate, and what
   happens to a `Reading` after it has been parsed?

   > **Pre:** a vector can hold pointers, not references, so make_unique_ptr for each reading?
   >
   > **Post:** ParsedLines.readings holds the readings, then they're grouped into a robots map of [str, vector[readings]] by coping them via push_back()

   A vector of `Reading` values was chosen over a vector of pointers. Pointers offered no memory
   or speed benefit here, and working with the objects directly was simpler.

2. **Which functions take `const Reading&`, which take `Reading&`, and which take values?**
   Justify each one individually.

   > **Pre:** default to all of them, unless we need to edit something in the function
   >
   > **Post:** agreed, we always send the const version, once we parse/validate/create a reading, it never needs to be edited so we never send it an editable version

   Specifically:

   - `group_robots()` takes a const reference: it only loops over the readings, copying each one
     into the map via `push_back`.
   - `analyze_temperature()` takes a const reference: it only loops over the readings, reading
     each temperature to compute the statistics.

3. **Where do malformed rows go?** With exceptions out of scope, what is the signature of the
   parse function? C++ answers this very differently from Python, where raising an exception
   was the obvious choice.

   > **Pre:** idk if we can return tuples (or similar type, guessing not), instant feel then is see if line is parseable, then based on that, try and do it after you get out of that 'is this line parseable function'? feels gross tho because by checking i'd want to return if valid (like in python),
   >
   > **Post:** ParsedLines does this perfectly for us, while we're looping rows, we're trying to create readings, if there's an error we store the row (as a ',' split string) in bad_rows, valid readings go to ParsedLines.readings

   Although exceptions were out of scope, a `try`/`catch` for `std::invalid_argument` was used
   anyway: it is the exception `std::stod` throws when a field cannot be parsed as a double, and
   catching it was a simple way to filter out malformed rows. It is not a complete filter; `nan`
   still passes as a valid value.

### Strong types

A fourth decision came up during implementation. C++ has no keyword arguments, so a constructor
taking three `double`s accepts them in any order without complaint. To prevent incorrectly
ordered arguments, each field is wrapped in its own type: `double velocity` became
`struct Velocity { double v; }`, and likewise for the other fields. By including `explicit` in the strong typed constructors, it stops a string automatically becoming a strong type (RobotID, Velocity, Battery, etc) - it is still possible for same-type values to be assigned to the incorrect strong type.

## Differences from the Python version

The Python version was an exercise in design rather than review. Its design was rough, but it
emphasized validation, tests, and error handling, and it included a CLI and JSON output. The C++
version ignores the defined value ranges for each field and prioritizes structure.

In my opinion, the C++ version is the cleaner of the two so far. Because `ParsedLines` separates
accepted from rejected rows and each field has its own type, validators could be placed directly
in the strong types' constructors if range checking were added later.

## What broke

### Forgetting to add new files to `CMakeLists.txt`

This happened twice. When a new source file is created and `main` depends on it, the file must
also be added to `add_executable` in `CMakeLists.txt`. Otherwise the build fails at linking time because there are undefined references.

### The segfault on a four-field row

`row[4]` caused a segmentation fault with no indication of the cause until
`-D_GLIBCXX_ASSERTIONS` was added to the build. The flag triggered at run time and showed a message in the terminal:

```text
/usr/include/c++/13/bits/stl_vector.h:1128: std::vector<_Tp, _Alloc>::reference std::vector<_Tp, _Alloc>::operator[](size_type) [with _Tp = std::__cxx11::basic_string<char>; _Alloc = std::allocator<std::__cxx11::basic_string<char> >; reference = std::__cxx11::basic_string<char>&; size_type = long unsigned int]: Assertion '__n < this->size()' failed.
Aborted (core dumped)
```

Which tells us we have a vector of strings, but the index trying to be read is not less than the size of the vector, so the assertion fails. Without the flag, if the address at the index is not mapped, the program is killed with a segfault.

The root cause was that not every row has five columns. Indexing past the end of a list raises an
`IndexError` in Python; in C++ it produced a segfault. The lesson: check the column count first,
or use `.at()`, which is bounds-checked at a small runtime cost.

## Known issues and next steps

- `std::stod` parses a leading number and ignores the rest of the string, so `1.5kg` is accepted
  as `1.5`.
- Out-of-range values (`std::out_of_range`) are not caught, and `nan` is accepted as valid.
- The telemetry file path is hard-coded. A config file would be useful if no CLI is added.
