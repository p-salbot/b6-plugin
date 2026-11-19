# Review 1: Refuse empty titles

| Criterion | Status | Evidence |
|---|---|---|
| R-002: `add ""` and `add "   "` print `Title must not be empty`, exit with 1, `tasks.json` unchanged | met | On a copy in `scratch/`: `python3 tiny_tasks.py add ""` -> `Title must not be empty`, exit code 1; same for `"   "`; `tasks.json` byte for byte the same |
| R-002: `python3 -m unittest` passes | met | `python3 -m unittest` -> `Ran 4 tests ... OK`; `test_add_rejects_empty_title` passes; the worker report shows the same command and result |

## Architecture check

matches

## Findings

- none

## Verdict

OK
