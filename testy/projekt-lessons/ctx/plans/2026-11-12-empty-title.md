# Plan: No empty task titles

Requirements: R-002
Size: M
Language: English

| # | Step | Agent | Model level | Task | How I verify |
|---|---|---|---|---|---|
| 1 | Refuse empty titles | worker | medium | `add_task` in `tasks.py` raises `ValueError` for an empty title; `tiny_tasks.py` prints the reason and exits with 1 without saving; a test in `test_tasks.py`; update `docs/architecture.md` | `python3 -m unittest` -> OK; `python3 tiny_tasks.py add ""` -> `Title must not be empty`, exit code 1, `tasks.json` unchanged |

## Choices for the owner

- none

## Token estimate

About 100 000 - 200 000 tokens (rough guide).
