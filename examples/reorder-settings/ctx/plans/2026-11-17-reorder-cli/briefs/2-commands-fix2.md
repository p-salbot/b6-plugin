# Brief 2 (fix round 2): Commands — full-width digit test

## Goal

Make the test for full-width digits really test a full-width digit. Nothing else changes.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-004 | Min must be a whole number 0 or more; reorder qty a whole number 1 or more. Bad input gets a message naming the problem, and the stored data does not change. |

## Earlier review

`ctx/plans/2026-11-17-reorder-cli/review-4.md`. Finding to fix:

1. `tests/test_cli.py:94`: `test_r004_full_width_digit_in_min_is_refused` passes the ASCII text `"Ff15"` instead of the full-width digit five (U+FF15). `"Ff15"` would be refused by plain `int()` too, so the test does not protect the fix. Change the argument to the Python escape `"５"` (backslash, `u`, `ff15` inside the string literal), keeping the file plain ASCII.

Caution: an earlier attempt to write `５` turned into `Ff15`, probably through shell or tool escaping. Use the Edit tool, then check the bytes of line 94 (for example `grep -n 'uff15' tests/test_cli.py` must show a backslash before `u`).

## Files to change

- `tests/test_cli.py`: only line 94.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed. Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-17-reorder-cli/scratch/` and are deleted before the report; keep `scratch/.gitignore`.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

1. Line 94 of `tests/test_cli.py` contains `"５"` with a backslash.
2. `python -m unittest -v`: all 33 tests pass, including `test_r004_full_width_digit_in_min_is_refused`.
3. Proof the test now protects the fix: in a scratch copy of the project (`reorder/` and `tests/` copied into `scratch/`), replace the number check in the copied `reorder/cli.py` with plain `int(text)` and run the tests there: `test_r004_full_width_digit_in_min_is_refused` must fail. Delete the copy afterwards.
4. Remove `__pycache__` folders you created; no `reorder.db` in the project root.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
