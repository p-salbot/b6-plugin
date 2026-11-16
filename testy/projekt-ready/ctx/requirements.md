# Requirements

## Intent

Tiny Tasks lets one person keep a short to-do list from the command line. (2026-11-01)

## Out of scope

- Reminders and due dates (2026-11-01)

| ID | Priority | Requirement | Source | Acceptance criterion | Status | Evidence |
|---|---|---|---|---|---|---|
| R-001 | MUST | The list can show only open tasks | Owner, 2026-11-01 | `python3 tiny_tasks.py list --open` prints no finished task | met | Review 2026-11-05: verdict OK; `test_tasks.py` test_list_only_open passes; checked by running the command on `tasks.json` |
