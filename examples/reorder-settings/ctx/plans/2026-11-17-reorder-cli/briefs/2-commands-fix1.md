# Brief 2 (fix round 1): Commands — number input and output encoding

## Goal

Fix two findings of the review of step 2. Everything else in step 2 stays as it is.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-004 | Item number and supplier must not be empty (spaces at the ends are removed). Min must be a whole number 0 or more; reorder qty a whole number 1 or more. Bad input gets a message naming the problem, and the stored data does not change. |
| R-005 | Save supplier `O'Brien`, then `show` returns exactly `O'Brien`. (Other special characters must work too.) |
| R-010 | The code uses only the Python standard library; no extra installation is needed. |

## Earlier review

`ctx/plans/2026-11-17-reorder-cli/review-3.md`. Findings to fix:

1. `reorder/cli.py` converts `--min` / `--reorder` with plain `int()`, so `1_0` is saved as 10 and full-width digits such as `５` pass. Fix: convert only text that, after `strip()`, is an optional `+`/`-` sign followed by the ASCII digits 0-9 (for example a regular expression `[+-]?[0-9]+` with `fullmatch`); otherwise pass the text on unchanged so that storage gives its field-naming message. Add CLI tests: `--reorder 1_0` and `--min ５` are refused with the message naming the field, exit code 1, data unchanged; `--min " 5 "` still works.
2. Output to a pipe or file on Windows uses cp1252: characters outside it (for example `Łódź`) crash `save` with a traceback after the row was saved, and `show` crashes halfway. Owner's decision (2026-11-17, option A): output is always written in UTF-8, and never crashes because of a character. Put the setup in a small function in `reorder/cli.py`, for example `configure_output(*streams)`, that reconfigures the given streams to `encoding="utf-8"` with `errors="replace"` (with a one-line comment saying why). `reorder/__main__.py` calls it with `sys.stdout` and `sys.stderr` before `main()`. Test it by passing `io.TextIOWrapper(io.BytesIO(), encoding="cp1252")` streams, then checking that writing `Łódź` and `Müller` does not raise and gives their UTF-8 bytes. Do not run `python -m reorder` as a subprocess in the tests (it would use the real `reorder.db`). Keep it plain.

Not part of this fix (accepted by the reviewer): `Reorder quantity` vs `Reorder qty` labels; the not-found message repeating spaces.

## Files to change

- `reorder/cli.py`: number conversion; optionally the output-setup function.
- `reorder/__main__.py`: call the output setup before `main()`.
- `tests/test_cli.py`: new tests for both findings.
- `docs/architecture.md`: update the "Command line" row (number rule, UTF-8 output) — only what is in the code.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed (not `reorder/storage.py`, not `tests/test_storage.py`). Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-17-reorder-cli/scratch/` and are deleted before the report.
- Tests must not create or touch `reorder.db` in the project root and must not depend on the run folder.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

1. `python -m unittest -v` in the project root: all tests pass, including the new ones.
2. Trial run in a scratch copy of `reorder/` (run from the scratch folder, then delete the copy and its `reorder.db`): `python -m reorder save L-1 --min 1 --reorder 2 --supplier "Łódź" > out.txt` gives exit code 0 and no traceback; `python -m reorder show L-1 > out.txt` writes all four lines, and `out.txt` read as UTF-8 contains `Łódź`; `python -m reorder save B-1 --min 1 --reorder 1_0 --supplier Acme` gives the field-naming message and exit code 1.
3. No `reorder.db` in the project root; `__pycache__` folders removed.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
