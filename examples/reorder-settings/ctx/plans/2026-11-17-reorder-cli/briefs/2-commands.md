# Brief 2: Commands

## Goal

Build the command line on top of the existing storage part (`reorder/storage.py`, do not change it): `show`, `save` and `list`, run as `python -m reorder …` from the project root, with clear messages. With tests. Keep it short and plain; the next maintainer is not an expert.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-001 | `show <item>` prints the item number, min, reorder qty and supplier. For an unknown item it prints a clear "not found" message and nothing else. |
| R-002 | After `save`, `show` returns the new values. Saving the same item again replaces its values, and there is still only one row for it. |
| R-004 | Item number and supplier must not be empty (spaces at the ends are removed). Min must be a whole number 0 or more; reorder qty a whole number 1 or more. Bad input gets a message naming the problem, and the stored data does not change. |
| R-005 | Save supplier `O'Brien`, then `show` returns exactly `O'Brien`. |
| R-006 | `list` prints a table of all items sorted by item number. With no items it says "no items". |
| R-007 | Save `A-100`, then `show a-100` finds it. Saving `a-100` updates that item instead of creating a second one. |
| R-010 | The code uses only the Python standard library; no extra installation is needed. |

## Design to follow

- `reorder/cli.py` with `main(argv=None, store=None)` that returns an exit code; `store` lets tests pass a `ReorderStore(":memory:")`. When `store` is `None`, open `ReorderStore()` (default file `reorder.db` in the project root, owner's choice) and close it at the end.
- `reorder/__main__.py`: only calls `main()` and exits with its code.
- Use `argparse` with sub-commands:
  - `show ITEM`
  - `save ITEM --min N --reorder N --supplier TEXT` (all three options required)
  - `list`
- Numbers: read `--min` and `--reorder` as text and convert them yourself, so that a non-number gives the same kind of message as the storage checks, naming the field (for example "Minimum stock must be a whole number 0 or more"). Do not rely on argparse's generic `invalid int value` message. Then call `ReorderStore.save`; show its `ValidationError` message.
- Output (to standard output):
  - `show`: one line per field, for example
    ```
    Item:          A-100
    Minimum stock: 5
    Reorder qty:   20
    Supplier:      O'Brien
    ```
  - `save`: one confirmation line, for example `Saved A-100: minimum stock 5, reorder qty 20, supplier Acme`.
  - `list`: a header row and one row per item with aligned columns (item, minimum stock, reorder qty, supplier), sorted as `list_all` returns them. With no items, print exactly `No items.`
- Errors (to standard error, exit code 1): unknown item: `Item 'X' not found.` and nothing else; bad input: the `ValidationError` message. Usage mistakes (missing option, unknown command) are left to argparse (exit code 2). Success: exit code 0.
- Tests in `tests/test_cli.py` with `unittest` only: call `main([...], store=...)` with one shared in-memory store per test and capture output (for example `contextlib.redirect_stdout` / `redirect_stderr`). Cover R-001 (known and unknown item, nothing else printed for unknown), R-002 (save then show; save again replaces, `list` shows one row), R-004 (empty supplier, negative min, `abc` as min, reorder 0: message names the field, exit code 1, data unchanged), R-005 (`O'Brien`), R-006 (sorted table, `No items.`), R-007 (`show a-100`, save `a-100` updates). Name tests after the requirement like in `tests/test_storage.py`.
- `.gitignore`: add the lines `reorder.db` and `__pycache__/`, keep the existing line.

## Files to change

- `reorder/cli.py`: new.
- `reorder/__main__.py`: new.
- `tests/test_cli.py`: new.
- `.gitignore`: add two lines.
- `docs/architecture.md`: add rows for the command line (only what is in the code now). Do not change the existing rows except where they would become wrong.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed; do not change `reorder/storage.py` or `tests/test_storage.py` (report in Open if you think they need a change). Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-17-reorder-cli/scratch/` and are deleted before the report.
- Do not create `reorder.db` in the project root: trial runs of `python -m reorder` are done in a copy of `reorder/` placed in the scratch folder (run from there, so the data file lands there), then deleted.
- No README now; that is step 3.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

1. `python -m unittest -v` in the project root: all tests pass (the 13 storage tests and the new command tests).
2. Trial run in a scratch copy: `python -m reorder save A-100 --min 5 --reorder 20 --supplier "O'Brien"`, then `python -m reorder show a-100`, `python -m reorder show X-1` (not found, exit code 1), `python -m reorder save B-1 --min -1 --reorder 5 --supplier Acme` (message, exit code 1), `python -m reorder list`. Put the outputs (short) in the report.
3. No `reorder.db` in the project root; scratch copy deleted; `__pycache__` folders removed.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
