# Review 2: Storage part (fix round 1)

| Criterion | Status | Evidence |
|---|---|---|
| Fix R-007: save `A-100`, read `a-100` finds it; saving `a-100` updates, no second row | met | `reorder/storage.py:17` `PRIMARY KEY COLLATE NOCASE`, upsert `SAVE_SQL` (lines 27-34) does not touch `item_no`. `test_r007_read_ignores_case`, `test_r007_save_with_other_case_updates_and_keeps_spelling` pass (own run). |
| Fix R-008 (part): `docs/architecture.md` describes only what holds in the code today, no plans | met | Read all 11 lines; every statement checked against `reorder/storage.py` (see Architecture check). `grep -niE "command\|cli\|step 2\|will\|later\|plan"` finds only line 8 "Changing the table needs a plan for existing data files", which is a rule for changes, not a plan. |
| Fix verify 1: no statement about the command line or other parts not built | met | `docs/architecture.md:10` now "Callers get `ValidationError` with a message naming the field and the rule; keep messages that way."; `:11` now "Callers only get `Item` values or `None`." No mention of a command line anywhere in the file. |
| Fix verify 2: row "Table" says only ASCII letters are matched ignoring case; changes column notes Unicode folding needs a table change | met | `docs/architecture.md:8`: "matched ignoring upper/lower case for the ASCII letters A-Z only (SQLite `NOCASE`); for example `Ü` and `ü` count as different" and "Full Unicode case folding would need a change to the table." Confirmed with an in-memory SQLite query: `'Ü'='ü' COLLATE NOCASE` -> 0, `'A'='a' COLLATE NOCASE` -> 1. |
| Fix verify 3: `python -m unittest` passes (13 tests); no other changed files | met | Own run of `python -m unittest -v`: "Ran 13 tests ... OK". `find . -newer briefs/1-storage-fix1.md` (excluding `.git`): only `docs/architecture.md` (20:03:03) and the run folder's `SUMMARY.md`. `reorder/storage.py` and `tests/test_storage.py` unchanged since 20:01:19, before review 1 (20:02:34). |
| Fix: only the named cells changed | met | Rows "Storage file", "Saving" read the same as described in review 1; changes are in the cells named in the fix brief (Table text and changes, Input checks changes, Reading changes). No git history to diff (no commits), so judged from content and review 1. |
| R-002 save/read, saving again replaces with one row | met | `storage.py:85-90`; `test_r002_*` (4 tests) pass, `count_rows() == 1` checked (test line 28). |
| R-003 forced failure keeps old values | met | `test_r003_failed_save_keeps_old_values` (test lines 40-50): `AFTER UPDATE` trigger with `RAISE(ABORT)`, old values and one row checked; passes. Save in `with self.connection` (storage.py:89-90). |
| R-004 input checks, clear messages, data unchanged | met | `_clean_text` / `_clean_whole_number` (storage.py:41-51) via `check_item` before writing (line 87); `test_r004_*` (4 tests, 10 bad inputs with exact messages, table `CHECK`s) pass. |
| R-005 `O'Brien` and other special characters come back exactly | met | Only `?` parameters (storage.py:78-82, 90, 94-97). `test_r005_apostrophe_supplier`, `test_r005_special_characters_come_back_exactly` (`"`, `;`, `--`, `ü`, injection string) pass. |
| R-010 standard library only | met | `grep "^import\|^from"`: storage.py imports `sqlite3`, `collections`, `pathlib`; tests import `sqlite3`, `unittest`, `reorder.storage`. |
| Design: package files, `DEFAULT_DB_PATH` from code location, other paths accepted | met | `reorder/__init__.py`, `reorder/storage.py`; storage.py:9 `Path(__file__).resolve().parent.parent / "reorder.db"`; `ReorderStore(db_path=...)` line 67. |
| Design: read / save / list sorted ignoring case; stored spelling kept | met | storage.py:75-98, `ORDER BY item_no COLLATE NOCASE` line 96; tests pass. |
| Tests use `unittest` and `:memory:` only | met | `setUp` uses `ReorderStore(":memory:")` (test line 12); no other path. |
| No command line built | met | `reorder/` holds only `__init__.py`, `storage.py` (and `__pycache__`); no `__main__.py`. |
| Verify 1: Python 3.8 or newer | met | `python --version` -> Python 3.13.17. |
| Verify 2: all tests pass, names show R-002/003/004/005/007 | met | 13 tests OK; names `test_r002_*`, `test_r003_*`, `test_r004_*`, `test_r005_*`, `test_r007_*`. |
| Verify 3: storage.py imports only standard library | met | See R-010. |
| Verify 4: no `reorder.db` in project root after the tests | met | `ls reorder.db` after the run -> "No such file or directory". |
| Code short and plain, comments only where needed | met | storage.py 98 lines, comments on path choice, NOCASE, CHECKs, bool refusal, `with` rollback. |
| `docs/architecture.md`: storage rows, link 0001, "Nothing is built yet." removed, only today's code | met | Five rows (lines 7-11), each links `decisions/0001-sqlite-file-with-python-tool.md` (file exists); the line "Nothing is built yet." is absent; no plans (see above). |

## Earlier findings

| Finding | Resolved? | Evidence |
|---|---|---|
| 1. `docs/architecture.md:10` and `:11` describe the not-yet-built command line | resolved | Line 10 changes cell: "Callers get `ValidationError` with a message naming the field and the rule; keep messages that way."; line 11: "Callers only get `Item` values or `None`." No "command line" in the file. |
| 2. `docs/architecture.md:8` "ignores upper/lower case" overstates; NOCASE is ASCII only | resolved | Line 8 now says ASCII A-Z only with the `Ü`/`ü` example, and the changes column notes that full Unicode case folding needs a table change. Behaviour confirmed with SQLite (0 for `Ü`/`ü`, 1 for `A`/`a`). |
| 3. `__pycache__/` left by tests; `.gitignore` covers only `.claude/` | moved to step 2 (not blocking) | Deliberately out of scope of this fix brief ("goes into step 2"). Still present: `git status` lists `reorder/__pycache__/` and `tests/__pycache__/` files; `.gitignore` unchanged (19:18). Not counted against this round. |

## Architecture check

Matches. Each row checked against `reorder/storage.py`: storage file and `DEFAULT_DB_PATH` (line 9, 67); table, NOCASE ASCII-only, `CHECK`s, create if missing (lines 15-23, 70); one upsert in one transaction keeping stored spelling (lines 27-34, 89-90); input checks with trim, `bool`/`float` refused, `ValidationError` naming field and rule (lines 37-61); `read` returns `Item` or `None`, `list_all` sorted ignoring case (lines 75-98). No plans or parts that do not exist yet are described.

## Findings

- none. (Earlier finding 3, `__pycache__/` in `.gitignore`, stays open for step 2 by decision of the main chat.)

## Verdict

OK
