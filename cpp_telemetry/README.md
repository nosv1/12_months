# Telemetry (C++)

<!-- One or two sentences: what this does and why it exists. Mention that it's a deliberately
     scoped C++ port of ../telemetry, and that the point was the language, not the problem. -->

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

<!-- The five columns. What counts as a malformed row, and the two kinds you reject:
     wrong field count, and a field that won't parse as a number. -->

## Output format

<!-- Show a real run's output, trimmed. Say what min/max/avg are computed over. -->

## Architecture

<!-- One line per translation unit: reader, parser, grouper, analysis, reading.
     A reader should be able to tell which file to open for a given question. -->

## Design decisions

<!-- The three SPEC questions, in prose, with the reasoning — including where you changed
     your mind between designing and building. Candidates:
       - who owns the readings, and why values rather than pointers
       - const& everywhere that reads; copy at the point of storage
       - how malformed rows are reported (ParsedLines partition, throw/catch, optional)
       - strong types (Timestamp/RobotID/Velocity/...) — what they buy, what they cost
       - std::optional for a robot with no readings, rather than a sentinel -->

## Differences from the Python version

<!-- Scope was capped deliberately. What ../telemetry does that this doesn't, and why:
     no JSON output, no error taxonomy, no CLI flags, no tests yet, no range/domain
     validation (so -273.2 is accepted as a real reading here). -->

## What broke?

<!-- The filter: what would break someone else, or what changed how you think.
     Not a list of typos. Each one: what you saw, what was actually wrong, why.
     Four or so is plenty. -->

### The compiler error that named a variable you never wrote

### The segfault on a four-field row

### Every robot reporting the same min, max and avg

### The one still latent, that only bites certain data

## Known issues / What's next?

<!-- Including anything on SPEC.md's "Want to add" list, and the latent bugs you know about
     but scoped out. -->
