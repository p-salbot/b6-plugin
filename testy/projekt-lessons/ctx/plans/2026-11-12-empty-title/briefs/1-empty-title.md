# Brief 1: Refuse empty titles

## Goal

`add` refuses a task whose title is empty or only spaces, with a clear message.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-002 | `python3 tiny_tasks.py add ""` and `add "   "` print `Title must not be empty`, exit with 1 and leave `tasks.json` unchanged; `python3 -m unittest` passes |

## Files to change

- `tasks.py`: `add_task` raises `ValueError("Title must not be empty")` for an empty or blank title.
- `tiny_tasks.py`: `add` prints the reason, returns 1 and does not save.
- `test_tasks.py`: a test for the empty and the blank title.
- `docs/architecture.md`: update if how the system works changed.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed. Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-12-empty-title/scratch/` and are deleted before the report.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

- `python3 -m unittest` -> OK.
- On a copy of the project in `scratch/`: `python3 tiny_tasks.py add ""` -> prints `Title must not be empty`, exit code 1, `tasks.json` unchanged.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
