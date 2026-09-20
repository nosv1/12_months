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
20260919 0710 - 1710 (6.5 hours -- Boss Fight #1 day 1: uv init, package rename after 01_telemetry proved un-importable, reader/parser/validator/grouper/robot modules, 38-test suite under way; 3h20m away excluded)
20260920 0815 - 1124 (3.15 hours -- Boss Fight #1 day 2: report module, console script installed and run outside the source tree (§8), fight stopped at 9h38m total against a 6h estimate)
20260920 1124 - 1214 (0.85 hours -- post-fight review against §1-§9: six findings incl. anonymous robots in the report and a stale uv tool install emitting a dict repr; robot_id fix; textbook 17 and 18)

### Estimated Task Times

- Tests (est 2h, actual _h - every way a row can be bad has a failing-if-broken test ... and parser redesign)
- I/O separation, which testing will push you into (est 1h, actual _h)
- CI, once there's something worth running (est 1h, actual _h)
- README (est 0.5h, actual _h)
- Boss fight (est 4-6h or maybe 2h, actual 9.65h -- 1.6x the 6h estimate; ~1h of that was header handling beyond the original scope)
