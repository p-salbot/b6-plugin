# Review 6: Step 3, README

Method: I copied the project without `ctx/` to `scratch/proj`, ran the README commands in that copy in the order the README gives them, ran the tests, then deleted the copy. `scratch/.gitignore` is kept. There is no `reorder.db` and no `__pycache__` in the project.

| Criterion | Status | Evidence |
|---|---|---|
| R-008: the README covers install, run, and every command with an example | met | README.md:5-11 covers install, :13-17 covers run, and :21-54 cover `show`, `save` and `list`, each with an example and output. Input rules are at :56-62, messages at :64-75 and exit codes at :77-81. |
| R-008: `docs/architecture.md` describes how it is built, and the README points to it | met | README.md:110 and :113 point to it and name the column "What it means for changes". README.md:111 points to `docs/decisions/`. |
| R-008: someone who follows only the README can run show, save and list | met (with findings 1 and 2) | In the copy, every command worked and gave exit 0. `save A-100 ...` printed `Saved A-100: minimum stock 5, reorder qty 20, supplier Smith Tools`. `save b-7 ... "O'Brien"` printed exactly the README line. `list` and `show a-100` also worked. But the sample output for `show` and `list` does not match what a reader sees (finding 1). |
| R-009: `python -m unittest` runs the tests, and all pass | met | In the copy: `Ran 33 tests ... OK`, and `-v` also gave OK. After I deleted `reorder.db`, the test run did not create a new one, which confirms README.md:99. Both test files use `ReorderStore(":memory:")` (tests/test_cli.py:14, tests/test_storage.py:12). The link from tests to R-001 to R-007 was checked in earlier reviews; this step did not change the tests (by file times). |
| R-010: standard library only, no extra install | met | The only imports are sys, argparse, re, sqlite3, collections and pathlib (reorder/*.py). README.md:7 says so. |
| Content 3: the README says to start from the project folder | met | README.md:15 says it in bold. |
| Content 4: messages, rules and exit codes match the code | not met | The rules match `_to_number` and `check_item` (cli.py:10-19, storage.py:139-159). I checked them in the copy: `" +3 "` gave 3, `1_0`, `1.5` and `-1` were refused, and `Ü-1` and `ü-1` count as different. Exit codes 0, 1 and 2 matched. One error-table row is wrong (finding 2). |
| Content 5: the data file | met | The code creates `reorder.db` on any command, because `ReorderStore()` connects in `main`, before any command runs (cli.py:89-90). In the copy, `list` on an empty folder created the file. README.md:85 follows the code. The worker reported the conflict with the brief, which says "first save"; I accept following the code. `.gitignore` lists `reorder.db`. |
| Content 6: output is UTF-8, also when saved to a file | met | In the copy, `list > items.txt` with the supplier `Müller` gave `Unicode text, UTF-8`. |
| Content 8: maintainer section and the two rules | met | README.md:103-118 match architecture rows "Saving" and "Table". |
| Examples are real (brief: "paste its true output") | not met | See finding 1. |
| Only README.md changed; no edits in ctx/ or docs/ | met | The project is not in git (everything is untracked), so I compared file times. Only README.md (20:14) changed after the brief (20:14). docs/ is from 20:09 and earlier, code from 20:09 and earlier, tests from 20:12 and earlier. |

## Architecture check

Matches. docs/architecture.md describes the code as it is, and the README agrees with it: the default file location, case matching for A-Z only, exit codes 0/1/2, UTF-8 output, and the CLI holding no input rules of its own. It describes no plans.

## Findings

1. **The sample outputs do not match each other or what a reader sees.** `show a-100` (README.md:23-28) and `list` (README.md:50-52) show A-100 as `8 / 25 / Smith Tools Ltd`. That data appears nowhere in the README. A reader who follows the commands in order sees this instead:
   - `show a-100` comes first and gives `Item 'a-100' not found.` with exit 1, because the data file is still empty.
   - After the README's `save`, `show` gives `5 / 20 / Smith Tools`.
   - `list` gives `A-100  5  20  Smith Tools`.

   **Fix:** put the examples in a real order (save first, then show and list) with the outputs that order really gives. Or say clearly that the examples are separate and show the data each one assumes.
2. **One row of the error table is wrong for an unknown command.** README.md:73 says an unknown command gives `the following arguments are required: ...`. The real output of `python -m reorder foo` is `python -m reorder: error: argument command: invalid choice: 'foo' (choose from 'show', 'save', 'list')`, with exit 2. **Fix:** list `invalid choice` as a separate message, or describe the row more generally (an argparse `usage:` line plus an `error:` line).
3. **The Python version claim is untested (worker's open point 2).** The claim "Python 3.8 or newer" is plausible for the Python code itself: `reconfigure` and required subparsers need 3.7 or newer. But `save` uses `INSERT ... ON CONFLICT DO UPDATE`, which needs SQLite 3.24 or newer. Python on Linux uses the system SQLite, which can be older; Windows and python.org builds are fine. Only 3.13 with SQLite 3.50.4 was tested. **Fix:** word it more carefully, for example "Python 3.8 or newer with SQLite 3.24 or newer (tested with Python 3.13)". Also give a check: `python -c "import sqlite3; print(sqlite3.sqlite_version)"`.
4. **Note on quoting (worker's open point 3).** In Git Bash, `--supplier "O'Brien"` and `"Smith Tools"` were stored exactly. I did not test PowerShell or cmd myself; the main chat reports it tested both. README.md:40 can stay as it is.
5. **Note on refused commands:** none.

## Verdict

FIX
