# Estimates vs actuals

Started 2026-09-21 at his request: *"idk if you actually have a grasp for time yet."* He's right. My
estimates are priors about generic work of that shape, not measurements of him. This file turns them
into measurements.

## Rules

- **Log every estimate when it's given**, with who gave it. His and mine are separate columns: his
  are a skill he's building (see [decisions.md](decisions.md)), mine are a tool he paces against.
- **Never edit an estimate after the fact.** The first number stands, even when it looks bad.
- **Actuals come from `date` and commit timestamps**, never from memory. Breaks excluded, same as
  the hours log.
- **Name the end state**, not the topic. "`json.tool` parses the installed tool's output from `~`",
  not "shipping".
- **Tag the kind of work.** Ratios are expected to differ by kind, so one global factor is wrong:
  `code-new` (from blank), `code-change` (modify existing), `debug`, `prose` (READMEs, requirements),
  `read` (absorb docs / textbook and use them), `ops` (install, ship, environment), `review`.
- **Ratio = actual / estimate midpoint.** Summarise per kind on Sundays in the table at the bottom;
  don't draw a conclusion from fewer than ~5 entries of a kind.

## Log

| Date | Task → end state | Kind | His est | My est | Actual | Ratio | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 09-12 | Tests: every bad row has a failing-if-broken test | code-new | 1h → 2h (added parser redesign) | — | not recorded | — | Scope merged with parser redesign and pipeline work across 09-12–09-17; no clean boundary. The "~3× out" in the 09-18 notes came from this period; its basis wasn't written down. |
| 09-17 | Multi-error collection shipped | code-change | 30–45 min | — | within estimate | ~1x | Per 09-18 session notes, once the 27-min `Literal[True]` detour is discounted. Commits 19:37–20:11 (34 min). |
| 09-19 | Boss Fight #1: §1–§8 from empty | code-new | 6h (earlier "4–6h or maybe 2h") | — | 9h38m | 1.6x | ~1h of header work beyond original scope; ~1.4x on like-for-like. |
| wk 2 | I/O separation | code-change | 1h | — | not recorded | — | Date given not recorded. Happened (textbook 09, 09-14) but not timed separately. |
| wk 2 | CI, once there's something worth running | ops | 1h | — | not started | — | Carried into week 3; now mine to scaffold. |
| wk 2 | README | prose | 0.5h | — | not started | — | Note his 0.5h vs my 45–60 min below. |
| 09-20 | `telemetry/` README he'd hand a new teammate | prose | — | 45–60 min | | | |
| 09-20 | Review my CI scaffold for `telemetry/` | review | — | 30 min | | | |
| 09-21 | Fight artifact shipped: installed tool's output parses as JSON from `~`, snapshot demo done | ops | — | 15 min | | | |

## Ratios by kind

Fill on Sundays. Too few entries to say anything yet (2026-09-21).

| Kind | Entries | His median ratio | My median ratio |
| --- | --- | --- | --- |
