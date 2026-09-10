### Deliverable — Telemetry Toolkit

A command-line robot telemetry analyzer, as a real repository.

*Input:* `timestamp`, `robot_id`, `velocity`, `battery`, `temperature`
*Output:* average velocity, max temperature, min battery, warnings

```
raw data → parser → validation → analysis → report
```

Must have: clean module boundaries, tests, a CLI, a README someone else could follow, an example
dataset, and CI that runs the tests on push.