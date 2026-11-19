# Review 1: Refuse empty titles

| Criterion | Status | Evidence |
|---|---|---|
| R-002: `add ""` and `add "   "` print `Title must not be empty`, exit with 1, `tasks.json` unchanged | met | On a copy in `scratch/`: `python3 tiny_tasks.py add ""` -> `Title must not be empty`, exit code 1; same for `"   "`; `tasks.json` byte for byte the same |
| R-002: `python3 -m unittest` passes | not met | `python3 -m unittest` -> `FAILED (failures=1)`: `test_add_rejects_empty_title` expects `ValueError` from `add_task`, but `add_task` still accepts `""`; the check was put only in `tiny_tasks.py` |

## Architecture check

`docs/architecture.md` says `add_task` refuses an empty title, but in the code only `tiny_tasks.py` checks it. Does not match.

## Findings

- The worker did not run `python3 -m unittest`, which the brief names under "How to verify"; its report gives only the manual run of `tiny_tasks.py add ""`. The new test fails.
- `tasks.py`: `add_task` has no check; the check is in `tiny_tasks.py` only, against the brief and `docs/architecture.md` ("New operations go here and get a test").
- `docs/architecture.md` describes a check in `add_task` that does not exist.

## Verdict

FIX
