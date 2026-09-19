# Week 2 20260914 - 20260920 — <topic>

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260912 2030 - 2245 (2.25 hours -- parser redesign, circular import fix; start approx.)
20260913 1217 - 1530 (2.5 hours -- pipeline stages redesign, BadReading, customer reject-row spec; 37 min break 1401-1438 excluded)
20260914 1637 - 1829 (1.75 hours -- functional core/imperative shell split; first real assertion in the test suite; textbook 09)
20260915 1706 - 1901 (1.9 hours -- exception taxonomy: base class, per-field error types; customer spec for valid ranges; textbook 10)
20260916 1614 - 1840 (2.4 hours -- test suite: parametrized accepts/rejects tables, defect set by line number; ColumnCountError; ruff B/C4; textbook 11 and 12)
20260917 1903 - 2119 (2.0 hours -- accepts-side partition tests found silent data loss in parse_lines; timestamp-order stage rewritten, validate_robot_timestamps deleted; suite green at 37; customer requirements doc; textbook 13 and 14; 15 min phone excluded)
20260918 1759 - 2012 (2.2 hours -- multi-error collection shipped: validate_parsed_line returns Reading | list[TelemetryException], BadReading holds the list, suite green at 40; -Infinity requirements violation found and fixed; requirements doc gains §8; textbook 15 and 16)

### Estimated Task Times

- Tests (est 2h, actual _h - every way a row can be bad has a failing-if-broken test ... and parser redesign)
- I/O separation, which testing will push you into (est 1h, actual _h)
- CI, once there's something worth running (est 1h, actual _h)
- README (est 0.5h, actual _h)
- Boss fight (est 4-6h or maybe 2h, actual _h)
