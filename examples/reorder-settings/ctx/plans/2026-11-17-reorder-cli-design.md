# Design: Reorder settings command-line tool

## Intent

Replace the Access/VBA tool `old/ReorderSettings.bas` with a small Python command-line tool that stores minimum stock, reorder quantity and supplier per item. For the owner (a planner occasionally asks the owner). It must be maintainable by someone else, documented, and must never lose data when saving.

## Goals

- Another person can understand, fix and change it.
- Documented (README for users and maintainers, `docs/architecture.md`).
- Saving is all-or-nothing; the old values survive any failed save.
- Small: three commands (`show`, `save`, `list`).

## Out of scope

- Window or web page.
- Deleting items.
- Import from Access, CSV export.
- Several users at the same time.
- Calculations from actual stock levels.
- Editing data in Excel.

## Constraints

- Python standard library only (R-010); Python is installed on the owner's PC.
- One user at a time, data on the owner's PC.
- Item numbers are matched ignoring upper/lower case, like the old Access tool (R-007).

## Approaches considered

| Option | Chosen? | Why |
|---|---|---|
| SQLite file + Python tool | yes | Built-in all-or-nothing saving and rules; no Access needed; widely known (decision 0001). |
| CSV file + Python tool | no | Safe saving built by hand; Excel can damage the data. |
| Keep Access, fix VBA | no | Others still need Access/VBA skills. |
| Terminal commands | yes | Smallest and easiest to test; the owner is the only regular user. |
| Simple window | no | More code; not needed now. |
| Local web page | no | Needs a server and an extra library. |

Proposed structure (proposal, details in the plan):

- A storage part: all database access, input checks and the all-or-nothing save (one transaction, parameterised queries, a unique key on the item number ignoring case).
- A command part: reads the command line (`show`, `save`, `list`) and prints results and clear error messages.
- Tests for R-001 to R-007, run with `python -m unittest`.
- Data file `reorder.db` in the project folder, not stored in git; backup is up to the owner.

## Open questions

| Question | Who decides |
|---|---|
| Which Python version is on the owner's PC? | Claude (check at build start) |
| Will the future maintainer have Python on their PC? | owner |
| Who maintains the tool when the owner is away? | owner |

## Links

- Requirements: R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010
- Decision records: 0001
