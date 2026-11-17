# Brief 1 (fix round 1): Storage part — architecture text

## Goal

Correct `docs/architecture.md` so that it describes only what is in the code today and states the case rule exactly. The code and tests are correct; do not change them.

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-007 | Save `A-100`, then reading `a-100` finds it. Saving `a-100` updates that item instead of creating a second one. |
| R-008 (part) | `docs/architecture.md` describes how it is built — only what holds in the code today, no plans. |

## Earlier review

`ctx/plans/2026-11-17-reorder-cli/review-1.md`. Findings to fix:

1. `docs/architecture.md` rows "Input checks" and "Reading" mention the command line, which does not exist yet ("The command line shows the ValidationError message…", "The command line only formats these results."). Reword these cells to describe only today's code (for example: "Callers get `ValidationError` with a message naming the field and the rule; keep messages that way." / "Callers only get `Item` values or `None`.").
2. Row "Table" says the item number "ignores upper/lower case". SQLite `NOCASE` folds only the ASCII letters A–Z; `Ü` and `ü` count as different. State this exactly in the row, and in "What it means for changes" note that full Unicode case folding would need a change to the table.

Finding 3 of the review (`__pycache__/` in `.gitignore`) is not part of this fix; it goes into step 2.

## Files to change

- `docs/architecture.md`: only the cells named above.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed (no code, no tests, no `.gitignore`). Do not write outside the project folder. Trial copies and helper files go only to `ctx/plans/2026-11-17-reorder-cli/scratch/` and are deleted before the report.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

1. `docs/architecture.md` contains no statement about the command line or other parts that do not exist yet.
2. Row "Table" says that only ASCII letters are matched ignoring case.
3. `python -m unittest` still passes (13 tests); `git status` shows no other changed files from you.

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
