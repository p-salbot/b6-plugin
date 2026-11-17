# Review 1: Storage part

| Criterion | Status | Evidence |
|---|---|---|
| R-002 save then read returns new values; saving again replaces, one row | met | `reorder/storage.py:85-90` one upsert statement (`SAVE_SQL`, lines 27-34). Tests `test_r002_save_then_read_returns_new_values`, `test_r002_saving_again_replaces_values_with_one_row` (`tests/test_storage.py:20-28`, checks `COUNT(*) == 1`) pass. |
| R-003 a forced failure partway through a save leaves old values unchanged | met | `test_r003_failed_save_keeps_old_values` (`tests/test_storage.py:40-50`) adds an `AFTER UPDATE` trigger with `RAISE(ABORT)`, saves an existing item, expects `sqlite3.Error`, then checks the old values and one row. Passes. Save runs inside `with self.connection` (storage.py:89-90), so it rolls back on error. |
| R-004 empty item/supplier refused (trimmed), min int >= 0, reorder int >= 1, clear message, data unchanged | met | `_clean_text` / `_clean_whole_number` (storage.py:41-51) run in `check_item` before any write (line 87); `bool` refused on purpose (line 49), `float` and `str` refused by `isinstance(int)`. Messages name field and rule, e.g. "Minimum stock must be a whole number 0 or more". `test_r004_bad_input_is_refused_and_data_unchanged` (test lines 52-72) covers 10 bad inputs with exact messages and checks stored data unchanged; `test_r004_zero_min_is_allowed`, `test_r004_spaces_at_the_ends_are_removed`, `test_r004_database_checks_refuse_bad_rows_too` (table `CHECK`s, storage.py:16-22) pass. |
| R-005 `O'Brien` comes back exactly; other special characters | met | All SQL uses `?` parameters (storage.py:78-82, 90, 94-97; no f-string or `+` into SQL). `test_r005_apostrophe_supplier` and `test_r005_special_characters_come_back_exactly` (double quote, `;`, `--`, `ü`, and an injection string, in item number and supplier) pass. |
| R-007 `a-100` finds `A-100`; saving `a-100` updates it and keeps stored spelling | met | `PRIMARY KEY COLLATE NOCASE` (storage.py:17); upsert `DO UPDATE` does not touch `item_no` (lines 30-33). `test_r007_read_ignores_case`, `test_r007_save_with_other_case_updates_and_keeps_spelling` (one row, spelling `A-100`) pass. |
| R-010 standard library only | met | `grep "^import\|^from" reorder/`: only `sqlite3`, `collections`, `pathlib`. Tests import only `sqlite3`, `unittest`, `reorder.storage`. |
| Design: package files, `DEFAULT_DB_PATH` from code location, every path overridable | met | `reorder/__init__.py` (empty), `reorder/storage.py`; `DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "reorder.db"` (line 9); `ReorderStore(db_path=...)` (line 67). |
| Design: read / save / list sorted ignoring case | met | `read` returns `Item` or `None` (lines 75-83), `save` (85-90), `list_all` with `ORDER BY item_no COLLATE NOCASE` (92-98); `test_r002_list_is_sorted_ignoring_case`, `test_r002_read_unknown_item_returns_none` pass. |
| Tests use `unittest` only and `:memory:`, never the real file or system temp | met | `setUp` uses `ReorderStore(":memory:")` (test line 12); no other path used. |
| No command line built (no `__main__.py`, no commands) | met | `ls reorder tests`: only `__init__.py`, `storage.py`, `test_storage.py` (plus `__pycache__`). |
| Verify 1: Python version 3.8 or newer | met | `python --version` -> Python 3.13.17 (SQLite 3.50.4). |
| Verify 2: `python -m unittest -v` all pass, names show R-002/003/004/005/007 | met | Ran it: 13 tests, OK; test names start with `test_r002`, `test_r003`, `test_r004`, `test_r005`, `test_r007`. |
| Verify 4: no `reorder.db` in project root after tests | met | `ls reorder.db` after the run -> "No such file or directory". |
| Code is short and plain, comments only where the reason is not obvious | met | storage.py is 98 lines; comments explain NOCASE, CHECKs, bool refusal, `with` rollback, path choice. |
| `docs/architecture.md`: rows for storage, link 0001, "Nothing is built yet." removed, only what is in the code now | not met | Rows and links present, the line is removed, but two rows describe the command line that does not exist yet (see Architecture check). |

## Architecture check

Mostly matches `reorder/storage.py`. Differences:

- `docs/architecture.md:10` (Input checks): "The command line shows the `ValidationError` message to the user." There is no command line yet; this is a plan.
- `docs/architecture.md:11` (Reading): "The command line only formats these results." Same: describes step 2, not today's code.
- `docs/architecture.md:8` (Table): "ignores upper/lower case" is true only for ASCII letters (SQLite `NOCASE`); `Ü` and `ü` count as different item numbers. The row does not say this.

## Findings

1. `docs/architecture.md:10` and `:11` describe the not-yet-built command line (plans). Fix: remove these sentences or reword them to what holds today (for example "Callers get the message from `ValidationError`").
2. `docs/architecture.md:8`: "ignores upper/lower case" overstates; `COLLATE NOCASE` folds only ASCII letters. Fix: add "(ASCII letters only)" or similar so a maintainer knows non-ASCII item numbers are case-sensitive. If this behaviour is not wanted, list it in Open for the owner rather than deciding it.
3. Note (not blocking by itself): running the tests leaves `reorder/__pycache__/` and `tests/__pycache__/`; `.gitignore` covers only `.claude/`. Consider whether the owner wants `__pycache__/` ignored (`.gitignore` is not in this brief's file list).

No changes found outside the named files: other untracked files predate the step (19:57-19:59) or are the run folder's `SUMMARY.md`. No edits in `ctx/` or `docs/decisions/` by the worker.

## Verdict

FIX
