# Brief 2: Refuse empty titles (fix round 1)

## Goal

Fix the findings of `review-1.md`: the check belongs in `add_task`, and the tests must pass.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-002 | `python3 tiny_tasks.py add ""` and `add "   "` print `Title must not be empty`, exit with 1 and leave `tasks.json` unchanged; `python3 -m unittest` passes |

## Earlier review

`ctx/plans/2026-11-12-empty-title/review-1.md`. Findings to fix:

- `python3 -m unittest` was not run and fails (`test_add_rejects_empty_title`).
- The check is only in `tiny_tasks.py`; move it to `add_task` in `tasks.py`, the command line only prints the reason.
- `docs/architecture.md` must match the code.

## Files to change

- `tasks.py`: `add_task` raises `ValueError("Title must not be empty")` for an empty or blank title.
- `tiny_tasks.py`: catch `ValueError` in `add`, print it, return 1, do not save.
- `test_tasks.py`: keep `test_add_rejects_empty_title`.
- `docs/architecture.md`: update if how the system works changed.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed. Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-12-empty-title/scratch/` and are deleted before the report.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

- `python3 -m unittest` -> OK. Put the command and its result in the report.
- On a copy of the project in `scratch/`: `python3 tiny_tasks.py add ""` -> prints `Title must not be empty`, exit code 1, `tasks.json` unchanged.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
