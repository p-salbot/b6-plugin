# Brief 3: README

## Goal

Write `README.md` in the project root so that the next maintainer (not an expert, possibly someone who has never seen the project) can install, run, test and change the tool using only this file and the documents it points to. English, plain words, short.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-008 | A README covers how to install, how to run, and every command with an example. `docs/architecture.md` describes how it is built. Someone following only the README can run show, save and list. |
| R-009 | One command (`python -m unittest`) runs tests for R-001 to R-007, and all of them pass. |
| R-010 | The code uses only the Python standard library; no extra installation is needed. |

## Content to cover

Read `reorder/storage.py`, `reorder/cli.py`, `reorder/__main__.py`, `tests/`, `docs/architecture.md` and `docs/decisions/0001-sqlite-file-with-python-tool.md` first; describe only what the code really does.

1. What the tool is: stores minimum stock, reorder quantity and supplier per item; replaces the old Access tool in `old/`.
2. Requirements and install: Python 3.8 or newer (tested with 3.13), nothing else to install; how to check (`python --version`).
3. How to run: open a terminal in the project folder (the folder that contains `reorder/`) and run `python -m reorder …`. Say clearly that the command must be started from that folder.
4. Every command with an example and a sample of its output: `show`, `save` (all three options required; how to quote a supplier with spaces or an apostrophe, e.g. `--supplier "O'Brien"`, works in PowerShell and cmd), `list`. The rules for input (empty text, whole numbers, min 0 or more, reorder 1 or more, spaces at the ends removed, item numbers match ignoring case for A-Z), the error messages and the exit codes (0 ok, 1 not found or bad input, 2 usage mistake).
5. The data file: `reorder.db` in the project folder, created on the first save; not stored in git; to back it up, copy the file while the tool is not running.
6. Output is always UTF-8, also when saved to a file (`python -m reorder list > items.txt`).
7. Tests: `python -m unittest` (or `-v`) from the project folder; tests never touch `reorder.db`.
8. For maintainers: where things are (one short list of the files), pointer to `docs/architecture.md` (read its column "What it means for changes" before a change) and to `docs/decisions/`; the two rules not to break (all-or-nothing save with `?` parameters; a new input rule goes into both the Python check and the table `CHECK`).

Examples must be real: run each example command in a scratch copy and paste its true output.

## Files to change

- `README.md`: new.

## What not to do

- Do not change `ctx/` or `docs/`, except files in the run folder that this brief names. Do not change code or tests (report in Open if the README reveals a problem).
- Do not change files that are not listed. Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-17-reorder-cli/scratch/` and are deleted before the report; keep `scratch/.gitignore`.
- Do not create `reorder.db` in the project root: run example commands in a copy of `reorder/` inside `scratch/`, then delete it.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

1. Copy the project (without `ctx/`) into `scratch/`, follow only `README.md` there: `save`, `show`, `list` work as described and give the documented output; `python -m unittest` passes. Delete the copy.
2. Every command, option, message and exit code in the README matches the code.
3. Remove `__pycache__` folders; no `reorder.db` in the project root.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
