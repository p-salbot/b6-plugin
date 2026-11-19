# Design: No empty task titles

## Intent

The owner sometimes presses Enter too early and gets a task with no title. Tiny Tasks should refuse such a task.

## Goals

- `add` refuses an empty title or a title made only of spaces, with a clear message.

## Out of scope

- Limits on title length or duplicate titles.

## Constraints

- No new dependencies; the check must be covered by a test in `test_tasks.py`.

## Approaches considered

| Option | Chosen? | Why |
|---|---|---|
| Check in `add_task` in `tasks.py`, the command line prints the reason | yes | The logic stays testable without files, as `docs/architecture.md` asks |
| Check only in `tiny_tasks.py` | no | No unit test could cover it |

## Open questions

| Question | Who decides |
|---|---|
| none | - |

## Links

- Requirements: R-002
- Decision records: none
