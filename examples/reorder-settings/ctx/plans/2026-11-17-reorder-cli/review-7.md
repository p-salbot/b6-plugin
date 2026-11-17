# Review 7: Step 3, README (fix round 1)

Method: I copied the project without `ctx/` (README.md, .gitignore, old/, reorder/, tests/, docs/) to `scratch/proj`, where there was no `reorder.db`. Using only README.md, I ran every command in the order the README gives them and compared each output with the README, ignoring only line endings. Both the README and the program output use CRLF. I also ran a missing option, a missing item, an unknown command and the tests. Then I deleted the copy, which also removed its `reorder.db`, `items.txt` and `__pycache__`. `scratch/` now holds only `.gitignore`. There is no `reorder.db` and no `__pycache__` anywhere in the project.

| Criterion | Status | Evidence |
|---|---|---|
| Fix 1: the sections go save, save O'Brien, show, list, with real outputs; the not-found sentence stays | met | README.md:24-57 has the order save (:26-28), save `"O'Brien"` (:34-36), show (:40-45), list (:51-55). I ran these on an empty copy. The save lines matched :28 and :36, `show a-100` matched :42-45, and `list` matched :53-55, all with exit 0. I compared them with `diff --strip-trailing-cr` and found no difference. The not-found sentence is still at :47, and `show Z-1` gives `Item 'Z-1' not found.` with exit 1. |
| Fix 2: the error table has two rows with the real messages, both exit 2 | met | README.md:76 and :77. `save C-1 --min 1 --reorder 2` gave `python -m reorder save: error: the following arguments are required: --supplier`, exit 2. `show` gave `... error: the following arguments are required: item`, exit 2. `foo` gave `python -m reorder: error: argument command: invalid choice: 'foo' (choose from 'show', 'save', 'list')`, exit 2. Each one printed a `usage:` line first. |
| Fix 3: Python/SQLite wording, the sqlite check and the python.org sentence | met | README.md:7 has the exact wording from the brief. :11-12 has `python --version` and the sqlite check. :14 has the python.org sentence. In the copy, the check printed `Python 3.13.17` and `3.50.4`. The SQLite 3.24 need comes from `ON CONFLICT ... DO UPDATE` (reorder/storage.py:30). |
| Fix brief: only README.md changed, only the named parts; no code, tests, docs or ctx changed | met | Files newer than the fix brief (20:17:18): only README.md (20:17:38) and ctx/.../SUMMARY.md (20:18, the main chat's run file, which the worker did not report). reorder/*.py is from 20:09 or earlier, tests from 20:12 or earlier, docs from 20:09 or earlier. The rest of the README (Run, Input rules, Data file, Encoding, Tests, Maintainers) has the same content as in review 6. |
| No helper script left (worker used a Python script for the edit) | met | `find` for `*.py` newer than the fix brief found nothing. No other new file is in the project, and `scratch/` held only `.gitignore` before my copy. The reorder/ and tests/ folder times (20:17:53) fit a `__pycache__` that was deleted after the test run. No file is left over. |
| R-008: install, run, every command with an example; architecture.md describes the build; a newcomer can run show, save and list | met | See fix 1. README.md:5-14 covers install, :16-20 covers run, and :24-57 cover the commands. :114 and :117 point to architecture.md. |
| R-009: `python -m unittest` runs the tests and all pass | met | In the copy, `Ran 33 tests ... OK`, and `-v` also gave OK. After I deleted `reorder.db`, the test run did not create it again, which confirms README.md:103. |
| R-010: standard library only | met | The only imports are sys, argparse, re, sqlite3, collections.namedtuple and pathlib (reorder/*.py). |
| Original content items 1-8 (start folder, rules, data file, UTF-8, tests, maintainers) | met | These were checked in review 6 and have not changed since. I checked again in the copy: `list` on an empty file gives `No items.` with exit 0 (:57). `list > items.txt` with supplier `Müller` gives a UTF-8 file (:93-95). |
| No `reorder.db` in the project root | met | `find -name reorder.db` found nothing after the cleanup. |

## Earlier findings

| Finding | Resolved? | Evidence |
|---|---|---|
| 1. Sample outputs did not match what a reader sees | resolved | The new order and outputs match a real run on an empty data file exactly (see fix 1). |
| 2. Wrong error-table row for an unknown command | resolved | README.md:76-77 are two separate rows that match the real messages, all with exit 2. |
| 3. Untested Python version claim | resolved | README.md:7, :12 and :14 are worded as the fix brief asks. |
| 4. Note on quoting (accepted) | resolved | Accepted in review 6. README.md:32 is unchanged in meaning, and `"O'Brien"` and `"Smith Tools"` were stored exactly in Git Bash. |
| 5. Note on refused commands (accepted) | resolved | Nothing to do. |

## Architecture check

Matches. docs/architecture.md was not changed (20:09:50) and still describes the code. The README agrees with it, and the document describes no plans.

## Findings

- none. No command was refused during this review.

## Verdict

OK
