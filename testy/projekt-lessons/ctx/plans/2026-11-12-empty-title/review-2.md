# Review 2: Refuse empty titles (fix round 1)

| Criterion | Status | Evidence |
|---|---|---|
| R-002: `add ""` and `add "   "` print `Title must not be empty`, exit with 1, `tasks.json` unchanged | met | On a copy in `scratch/`: `python3 tiny_tasks.py add ""` -> `Title must not be empty`, exit code 1; same for `"   "`; `tasks.json` byte for byte the same |
| R-002: `python3 -m unittest` passes | met | `python3 -m unittest` -> `Ran 4 tests ... OK`; `test_add_rejects_empty_title` passes |

## Earlier findings

| Finding | Resolved? | Evidence |
|---|---|---|
| `python3 -m unittest` not run, the new test fails | resolved | Worker report shows the command and `OK`; my own run: `Ran 4 tests ... OK` |
| Check only in `tiny_tasks.py` | resolved | `tasks.py` `add_task` raises `ValueError("Title must not be empty")`; `tiny_tasks.py` only catches it and prints it |
| `docs/architecture.md` does not match the code | resolved | The rows `Task logic` and `Command line` describe the code as it is now |

## Architecture check

matches

## Findings

- none

## Verdict

OK
