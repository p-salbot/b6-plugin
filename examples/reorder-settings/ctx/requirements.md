# Requirements

## Intent

A small Python command-line tool that stores the reorder settings per item (minimum stock, reorder quantity, supplier) and replaces the old Access/VBA tool (`old/ReorderSettings.bas`). It is used by the owner on their own PC; a planner occasionally asks the owner for values. The reason for the rebuild: someone other than the owner must be able to understand, fix and change it, it must be documented, and saving must never lose data.

## Out of scope

- 2026-11-17: A window or web page (terminal commands only).
- 2026-11-17: Deleting items.
- 2026-11-17: Import from Access and CSV export; the owner types the items in by hand.
- 2026-11-17: Several users at the same time.
- 2026-11-17: Any calculation from actual stock levels.
- 2026-11-17: Editing the data in Excel.

Statuses: proposed -> approved -> met or partly met; cancelled.

| ID | Priority | Requirement | Source | Acceptance criterion | Status | Evidence |
|---|---|---|---|---|---|---|
| R-001 | MUST | `show <item>` shows the settings of one item. | Owner, 2026-11-17 | It prints the item number, min, reorder qty and supplier. For an unknown item it prints a clear "not found" message and nothing else. | met | 2026-11-17: CLI tests for known/unknown item pass (`python -m unittest` -> 33 OK); trial `show X-1` -> `Item 'X-1' not found.`, exit 1, nothing else printed; review-5 and review-7 OK. |
| R-002 | MUST | `save <item> --min … --reorder … --supplier …` creates a new item or updates an existing one. | Owner, 2026-11-17 | After `save`, `show` returns the new values. Saving the same item again replaces its values, and there is still only one row for it. | met | 2026-11-17: storage and CLI tests (save then show; save again replaces, `list` shows one row) pass; README sequence replayed on a fresh copy; review-2, review-5, review-7 OK. |
| R-003 | MUST | Saving is all-or-nothing. | Owner, 2026-11-17 | A test makes the save fail partway through. Afterwards the old values are still there, unchanged. | met | 2026-11-17: `test_r003_failed_save_keeps_old_values` (trigger raises during update; old values unchanged) passes; save is one upsert in one transaction; review-2 OK. |
| R-004 | MUST | Bad input is refused. | Owner, 2026-11-17 | Item number and supplier must not be empty (spaces at the ends are removed). Min must be a whole number 0 or more; reorder qty a whole number 1 or more. Bad input gets a message naming the problem, and the stored data does not change. | met | 2026-11-17: storage and CLI tests (empty text, negative min, reorder 0, `abc`, `1_0`, full-width digit; message names the field, exit 1, data unchanged) pass; full-width test shown to fail against plain `int()`; review-5 OK. |
| R-005 | MUST | Apostrophes and other special characters work. | Owner, 2026-11-17 | Save supplier `O'Brien`, then `show` returns exactly `O'Brien`. | met | 2026-11-17: tests for `O'Brien`, quotes, `;`, `--`, `ü` pass; output always UTF-8 (`Łódź` written to a file correctly); PowerShell and cmd quoting tried; review-5 OK. |
| R-006 | MUST | `list` shows all items. | Owner, 2026-11-17 | It prints a table of all items sorted by item number. With no items it says "no items". | met | 2026-11-17: CLI tests (sorted table; empty -> `No items.`) pass; README `list` output reproduced exactly; review-5 and review-7 OK. |
| R-007 | MUST | Item numbers ignore upper/lower case. | Owner, 2026-11-17 | Save `A-100`, then `show a-100` finds it. Saving `a-100` updates that item instead of creating a second one. | met | 2026-11-17: storage and CLI tests (`show a-100` finds `A-100`; save `a-100` updates, stored spelling kept) pass; letters A-Z only, accepted by owner (no accented item numbers); review-2 and review-5 OK. |
| R-008 | MUST | It is documented for the next maintainer. | Owner, 2026-11-17 (Claude's proposal, approved) | A README covers how to install, how to run, and every command with an example. `docs/architecture.md` describes how it is built. Someone following only the README can run show, save and list. | met | 2026-11-17: reviewer followed only `README.md` on a fresh copy: all outputs, messages and exit codes match; `docs/architecture.md` matches the code; review-7 OK. |
| R-009 | MUST | It has automatic tests. | Owner, 2026-11-17 | One command (`python -m unittest`) runs tests for R-001 to R-007, and all of them pass. | met | 2026-11-17: `python -m unittest` -> 33 tests OK (13 storage, 20 CLI), named after R-001 to R-007; review-7 OK. |
| R-010 | MUST | It needs nothing beyond Python itself. | Owner, 2026-11-17 (Claude's proposal, approved) | The code uses only the Python standard library; no extra installation is needed. | met | 2026-11-17: imports only `sqlite3`, `collections`, `pathlib`, `argparse`, `re`, `sys` (standard library); review-2, review-5, review-7 OK. |
