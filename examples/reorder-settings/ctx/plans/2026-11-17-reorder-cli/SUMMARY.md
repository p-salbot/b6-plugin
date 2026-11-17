# Summary: Reorder settings command-line tool

## Where we stopped

All three steps OK (review-2, review-5, review-7). Run ended; handed over to wrap-up.

## Steps done

| # | Step | Result | Evidence |
|---|---|---|---|
| 1 | Storage part | OK (after fix round 1) | `python -m unittest -v` -> 13 tests OK (Python 3.13.17, SQLite 3.50.4); review-1.md FIX (docs only), review-2.md OK |
| 2 | Commands | OK (after fix rounds 1 and 2) | `python -m unittest` -> 33 tests OK; scratch trial `show L-1 > out.txt` -> UTF-8 `Łódź`, `--reorder 1_0` refused, exit 1; full-width test fails against plain `int()`; PowerShell `--supplier "O'Brien & Sons"` and cmd `--supplier "O'Neil Ltd"` stored and shown exactly; review-3 FIX, review-4 FIX, review-5 OK |
| 3 | README | OK (after fix round 1) | README commands replayed in order on a fresh scratch copy -> outputs match exactly; missing option / unknown command -> README messages, exit 2; `python -m unittest` -> 33 OK; review-6 FIX, review-7 OK |

## Decisions

- Data file `reorder.db` lives in the tool's folder (project root), not the current folder; owner, 2026-11-17.
- Item numbers never contain accented letters, so the ASCII-only case rule is enough; owner, 2026-11-17.
- Output is always written in UTF-8 (option A), so special characters never crash or get lost when output goes to a file or pipe; owner, 2026-11-17.
- `reorder.db` is created by any command, not only by the first save; README follows the code; main chat, accepted by review-6/7.

## Rounds of fixes

- Step 1: round 1, docs/architecture.md described the future command line and did not state the ASCII-only case rule; fixed, review-2.md OK.
- Step 2: round 1, number fields accepted `1_0`/full-width digits; output crashed on non-cp1252 characters when piped; code fixed, review-4.md FIX for one test.
- Step 2: round 2, full-width digit test used "Ff15" instead of "５" (GNU sed reads `\u` as "uppercase next letter"); fixed, review-5.md OK.
- Step 3: round 1, README examples not reproducible in order, wrong unknown-command message, too broad version claim; fixed, review-7.md OK.

## Steps not done

- none

## Token use

About 330,000 tokens for agents (14 agent runs, sum of reported use), plus the main chat (estimate 250,000-450,000 for the agents; the 4 fix rounds are included).

Run ended: yes, all steps OK.
