# Telemetry (C++)

A toy problem to read telemetry data from csv and output basic analysis of the readings. This is a scoped C++ port of the python variant in /telemetry. The priority of this port was to review the language - not to expand the functionality.

## Setup and running

```bash
cmake -B build
cmake --build build
./build/telem
```

Run from this directory — the CSV path is relative to the working directory, not the binary.

Requires a C++17 compiler and CMake 3.16+. No dependencies.

<!-- Note the -Wall -Wextra -D_GLIBCXX_ASSERTIONS flags and what _GLIBCXX_ASSERTIONS buys,
if you think a reader needs it. -->

## Input format

Data is provided via a CSV file - [sample_telemetry](data/sample_telemetry.csv)

Headers: timestamp,robot_id,velocity,battery,temperature

| Header | Type |  
| --- | --- |
| timestamp | ISO (as string) |  
| robot_id | string |  
| velocity | double |  
| battery | double |  
| temperature | double |  

Given the objective was C++ structure and less about data validation, parsing a line into a `Reading` was simply a matter of making sure the line had the expected number of columns and each element could be converted to the correct type.

## Output format

```bash
Readings: 359            # total accepted readings
Rejected readings: 3     # total malformed rows or rows with un-parseable fields
amr-01 -- 120 readings   # robot id and number of 'valid' readings
min: -273.2              # min temperature
max: 33                  # max temperature
avg: 28.1242             # avg temperature

...[per robot]...
```

## Architecture

- **Reader:** read csv file and output a `vector<vector<string>>` as `data`
- **Parser:** convert `data` into `ParsedLines` holding accepted readings as a `vector<Reading>` and `bad_rows` as a `vector<vector<string>>`
- **Reading:** a parsed row storing timestamp and robot_id as strings and velocity, battery, and temperature as doubles
- **Grouper:** group the robots into a map of `map<string, vector<Reading>>` where key is robot_id
- **Analysis:** loop robot readings and compute the min/max/avg temperature stored in `TemperatureAnalysis` (default output is null if no readings are present)

## Design decisions

Before designing this C++ variant, three questions came up:

1. **What owns the collection of readings?** How do per-robot stats accumulate, and what happens to
   a `Reading` after it has been parsed?

   > A (pre): a vector can hold pointers, not references, so make_unique_ptr for each reading?
   > A (post): ParsedLines.readings holds the readings until they're grouped into a robots map of [str, vector[readings]] by coping them via push_back()

   A vector of Readings was decided given there was no relevant benefit of storing them as pointers, no memory or speed benefit - in addition it was just easier only dealing with the objects.

2. **Which functions take `const Reading&`, which take `Reading&`, and which take values?**
   Justify each one individually. This is 2026-09-23's material applied directly, and it's the
   checkable part.

   > A (pre): default to all of them, unless we need to edit something in the function
   > A (post): agreed, we always send the const version, once we parse/validate/create a reading, it never needs to be edited so we never send it an editable version

3. **Where do malformed rows go?** With exceptions out of scope, what is the signature of the parse
   function? This one is genuinely hard in C++ and has no obviously correct answer — the first
   instinct is what's wanted, not the right answer. It's also the question C++ answers very
   differently from Python, where raising was free.

   > A (pre): idk if we can return tuples (or similar type, guessing not), instant feel then is see if line is parseable, then based on that, try and do it after you get out of that 'is this line parseable function'? feels gross tho because by checking i'd want to return if valid (like in python),
   > A (post): ParsedLines does this perfectly for us, while we're looping rows, we're trying to create readings, if there's an error we store the row (as a ',' split string) in bad_rows, valid readings go to ParsedLines.readings

In addition to the three questions, a difference came up in C++ where there are no keyword args, so to prevent incorrect ordering or typing of the Reading args, it was decided to use strong types. double velocity became struct Velocity with double v - and so on.

## Differences from the Python version

The Python version was less review, and more design. Though the design was rough, it focused on validation tests and error handling. There was also a CLI and a JSON output. The C++ variant ignores defined ranges for the CSV fields and prioritizes structure. In my opinion, the C++ variant, so far, is a much cleaner experience. The choice to have a `ParsedLines` object and strongly typed fields means we can put the validators right inside the strong types upon construction, if desired.

## What broke?

### The compiler error that named a variable you never wrote

Remember to put new files in CMakeLists! My goodness, this got me twice, when you create a new file that main depends on in some way, you've got to remember to add it to add_executable in the CMakeList.

### The segfault on a four-field row

There was no hint to why a `row[_index_]` caused the seg fault, not until we stuck a -W... flag in the build script. (still not sure what those flags do, but they did point us in the right direction). The main issue was not all rows have the correct number of columns, so when we expect 5 columns and get 4 then do a row[4] we get a Python out of range error or a C++ seg fault. Lesson learned, check the col count, or use .at() with a cost.

## Known issues / What's next?

- Doubles can be converted from non-exact-doubles via `stod` - `1.5kg` can still be read as `1.5`
- I'd love to have a config for the telemetry path (if we're not having a CLI)
