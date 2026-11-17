# Review 5: Step 2, Commands (fix round 2)

## Fix brief criteria (2-commands-fix2.md)

| Criterion | Status | Evidence |
|---|---|---|
| Finding 1: `test_r004_full_width_digit_in_min_is_refused` passes the escape `"５"`, file stays plain ASCII | met | `od -c` of `tests/test_cli.py:94` shows `m i n i m u m = " \ u f f 1 5 " )`; `grep -n 'uff15'` gives line 94 with the backslash; `file tests/test_cli.py`: "ASCII text"; `grep -P '[^\x00-\x7f]'` finds nothing. |
| R-004 (full-width digit refused, field message, exit 1, data unchanged) | met | The test uses `assert_refused` (`test_cli.py:63-70`): exit code 1, empty stdout, `MIN_MESSAGE` in stderr, `list_all()` unchanged. Passes against `reorder/cli.py:10-19` (`[+-]?[0-9]+` with `fullmatch`). |
| How to verify 1: line 94 has `"５"` with a backslash | met | See first row. |
| How to verify 2: `python -m unittest -v` all 33 pass, including the full-width test | met | Ran in project root: `Ran 33 tests ... OK` (13 storage + 20 CLI); `test_r004_full_width_digit_in_min_is_refused ... ok`. |
| How to verify 3: test fails against plain `int()` | met | Copied `reorder/` and `tests/` into `scratch/`. With `_to_number` changed to `try: return int(text) except ValueError: return text` (the old behaviour): `test_r004_full_width_digit_in_min_is_refused ... FAIL` (`AssertionError: 0 != 1`) and `test_r004_underscore_in_reorder_is_refused ... FAIL`; the other 18 pass. With bare `int(text)` the full-width test also FAILs. Copy deleted; `scratch/` holds only `.gitignore` again. |
| How to verify 4: no `__pycache__` left, no `reorder.db` in root | met | Before my run, `find` listed no `.pyc` files. I removed the caches my test run created (`reorder/__pycache__`, `tests/__pycache__`); final `find` shows no `__pycache__` and no `reorder.db`. |
| Only `tests/test_cli.py` line 94 changed | met (as far as checkable) | Project is untracked in git, so no diff. Change times: only `tests/test_cli.py` (20:12:29) is newer than the fix brief (20:12:07) among project files (besides `SUMMARY.md` in the run folder, 20:13, main chat). `reorder/cli.py`, `__main__.py`, `docs/architecture.md` (20:09:50), `storage.py`, `test_storage.py` (20:01), `docs/decisions/0001` (19:57), `.gitignore` (20:05) are older. Lines 90-99 match review 4's description apart from line 94; still 33 tests, same names. |

## Step-2 criteria still hold (2-commands.md, 2-commands-fix1.md)

| Criterion | Status | Evidence |
|---|---|---|
| R-001, R-002, R-004, R-005, R-006, R-007 tests | met | All `test_r00*` CLI tests pass in my run (20 CLI tests). |
| R-004 number rule (`1_0`, full-width refused, `" 5 "` allowed) | met | `cli.py:10-19` unchanged; `test_r004_underscore_*`, `full_width_*`, `spaces_around_number_*` pass. |
| R-005 UTF-8 output (`configure_output`) | met | `cli.py:22-25`, unchanged since review 4; `test_r005_output_is_utf_8_and_never_fails` passes. |
| R-010 standard library only | met | `cli.py` imports `argparse`, `re`, `sys`, `reorder.storage`; tests `contextlib`, `io`, `unittest`. |
| Design, `.gitignore`, `storage.py` untouched | met | Files unchanged since review 4 (change times above). |

## Earlier findings

| Finding | Resolved? | Evidence |
|---|---|---|
| 1. `tests/test_cli.py:93-94` used ASCII `"Ff15"` instead of the full-width digit, so the test did not guard the fix | resolved | Line 94 now `minimum="５"` (bytes checked); the test fails against plain `int()` in a scratch copy and passes against the current code. |
| 2. Note: `scratch/.gitignore` exists with `*` | resolved (note only) | Still present, unchanged (20:10:43); kept by me. |

## Architecture check

Matches. `docs/architecture.md` (unchanged, 20:09:50) "Command line" row describes `configure_output` and the number rule (optional sign and digits 0-9 after trimming), as in `cli.py:10-25` and `__main__.py`. Tests are not described there, so the test change needs no update. No plans described.

## Findings

- none.

## Verdict

OK
