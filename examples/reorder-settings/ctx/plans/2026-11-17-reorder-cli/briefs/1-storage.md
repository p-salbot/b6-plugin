# Brief 1: Storage part

## Goal

Build the part of the new tool that stores reorder settings in a SQLite file: input checks, one row per item ignoring upper/lower case, and an all-or-nothing save. With tests. The command line comes in step 2; do not build it now.

Background: this replaces `old/ReorderSettings.bas` (read it). The old tool lost an item when a save failed between its DELETE and INSERT, and broke on apostrophes because it glued text into SQL. Both must be impossible here. The code must be easy for a non-expert maintainer to read: short, plain, with comments only where the reason is not obvious.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-002 | After `save`, reading the item returns the new values. Saving the same item again replaces its values, and there is still only one row for it. (Here: tested on the storage functions; the `save`/`show` commands come in step 2.) |
| R-003 | A test makes the save fail partway through. Afterwards the old values are still there, unchanged. |
| R-004 | Item number and supplier must not be empty (spaces at the ends are removed). Min must be a whole number 0 or more; reorder qty a whole number 1 or more. Bad input gets a message naming the problem, and the stored data does not change. |
| R-005 | Save supplier `O'Brien`, then reading returns exactly `O'Brien`. |
| R-007 | Save `A-100`, then reading `a-100` finds it. Saving `a-100` updates that item instead of creating a second one. |
| R-010 | The code uses only the Python standard library; no extra installation is needed. |

## Design to follow

- Package folder `reorder/` in the project root with `reorder/__init__.py` and `reorder/storage.py`.
- Default data file: `reorder.db` in the project root (the folder that contains `reorder/`), computed from the location of the code, not from the current folder. Expose it as a constant (for example `DEFAULT_DB_PATH`). Every function or class must also accept another path, so tests never touch the real file.
- Table with columns item number, min qty, reorder qty, supplier. The item number is unique ignoring upper/lower case (for example `PRIMARY KEY COLLATE NOCASE`). Add `CHECK` constraints matching R-004 as a second line of defence. Create the table if it does not exist.
- Functions (or one small class) for: read one item (returns the values or "none"), save one item (create or update), list all items sorted by item number (ignoring case).
- Save is one statement or one transaction: never delete-then-insert outside a transaction. All SQL uses `?` parameters, never text glued into SQL.
- Checks run before writing. A failed check raises one clear error type (for example `ValidationError`) whose message names the field and the rule, for example "Minimum stock must be a whole number 0 or more". Whole numbers: accept `int` (not `bool`, not `float`). Text: strip spaces at both ends before checking and storing.
- When an existing item is updated using a different case (`a-100` for stored `A-100`), keep the stored spelling `A-100`.
- Tests in `tests/` (`tests/__init__.py`, `tests/test_storage.py`) using `unittest` only. Tests use an in-memory database (`:memory:`) or a file inside the project's run scratch folder; never the real `reorder.db`, never the system temp folder.
- R-003 test: cause a real failure in the middle of a save of an existing item (for example a SQLite trigger that raises, or making the commit fail), then check the old values are still stored unchanged. Also test that a refused input (R-004) leaves the stored data unchanged.
- R-005 test: also include other special characters in item number and supplier (double quote, semicolon, `--`, a non-ASCII letter such as `ü`).

## Files to change

- `reorder/__init__.py`: new.
- `reorder/storage.py`: new.
- `tests/__init__.py`: new.
- `tests/test_storage.py`: new.
- `docs/architecture.md`: add rows for the storage part (what holds today, what it means for changes, link `decisions/0001-sqlite-file-with-python-tool.md` where it fits). Remove the line "Nothing is built yet." Only what is in the code now.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed. Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-17-reorder-cli/scratch/` and are deleted before the report.
- Do not build the command line (`show`, `save`, `list` commands, `__main__.py`); that is step 2.
- Do not create `reorder.db` in the project root.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

1. `python --version` in the project root: report the version (needs 3.8 or newer; report if older).
2. `python -m unittest -v` in the project root: all tests pass, and the test names show tests for R-002, R-003, R-004, R-005, R-007.
3. `reorder/storage.py` imports only standard-library modules.
4. No `reorder.db` exists in the project root after the tests.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open. Include the Python version.
