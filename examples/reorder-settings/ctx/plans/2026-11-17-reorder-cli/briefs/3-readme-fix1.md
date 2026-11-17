# Brief 3 (fix round 1): README — examples, error table, Python version

## Goal

Fix three findings of the review of step 3 in `README.md`. Everything else stays.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-008 | A README covers how to install, how to run, and every command with an example. `docs/architecture.md` describes how it is built. Someone following only the README can run show, save and list. |
| R-010 | The code uses only the Python standard library; no extra installation is needed. |

## Earlier review

`ctx/plans/2026-11-17-reorder-cli/review-6.md`. Findings to fix:

1. `README.md:23-28` and `:50-52`: the `show` and `list` samples show data (8 / 25 / Smith Tools Ltd) that the README never creates, and `show` comes before any `save`. Reorder the command sections so that a reader following them in order on an empty data file sees exactly the printed output: first `save` (create A-100), then `save` with the apostrophe example, then `show a-100`, then `list`. Run this exact sequence on a fresh scratch copy (no `reorder.db`) and paste the real outputs. The not-found sentence stays.
2. `README.md:73`: an unknown command does not give "the following arguments are required". Split into two rows with the real messages: missing item or option -> `... error: the following arguments are required: ...`; unknown command -> `... error: argument command: invalid choice: ...`. Check both against a real run; both exit code 2.
3. `README.md:7` and the version check: say "Python 3.8 or newer with SQLite 3.24 or newer (tested with Python 3.13 and SQLite 3.50)" and add the check `python -c "import sqlite3; print(sqlite3.sqlite_version)"` next to `python --version`, with one sentence that the Python from python.org on Windows brings a new enough SQLite.

## Files to change

- `README.md`: only the parts named above.

## What not to do

- Do not change `ctx/` or `docs/`, except files in the run folder that this brief names. Do not change code or tests.
- Do not change files that are not listed. Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-17-reorder-cli/scratch/` and are deleted before the report; keep `scratch/.gitignore`.
- Do not create `reorder.db` in the project root.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

1. On a fresh scratch copy of `reorder/` (no `reorder.db`), run the README's commands in the README's order: every printed output matches the README exactly.
2. Run a missing option and an unknown command: messages match the two table rows, exit code 2.
3. `python -m unittest` in the project root still passes (33 tests).
4. Delete the scratch copy, its `reorder.db` and `__pycache__`; no `reorder.db` in the project root.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
