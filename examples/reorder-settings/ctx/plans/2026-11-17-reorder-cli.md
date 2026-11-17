# Plan: Reorder settings command-line tool

Requirements: R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010
Size: M
Language: English

| # | Step | Agent | Model level | Task | How I verify |
|---|---|---|---|---|---|
| 1 | Storage part | worker | medium | Check the installed Python version. Build the storage part: SQLite file, input checks, one row per item ignoring case, all-or-nothing save. Add its tests and describe it in `docs/architecture.md`. | `python -m unittest` passes; tests cover create/update (R-002), a save failing partway leaves old values (R-003), bad input refused and nothing changed (R-004), `O'Brien` (R-005), `a-100` = `A-100` (R-007); only the Python standard library is used (R-010). |
| 2 | Commands | worker | medium | Build the commands `show`, `save`, `list` (`python -m reorder …`) with clear messages. Add their tests, keep `reorder.db` out of git, extend `docs/architecture.md`. | `python -m unittest` passes; trial runs: `show` known and unknown item (R-001), `save` then `show` (R-002), `list` with items and empty (R-006), bad input gives a message (R-004). |
| 3 | README | worker | medium | Write `README.md` for the next maintainer: install, run, every command with an example, running the tests, where the data file is. | The reviewer follows only the README in a scratch copy of the project: `save`, `show`, `list` work and the tests pass (R-008, R-009). |

## Choices for the owner

- Location of the data file `reorder.db`: (a) always in the tool's folder / (b) in the folder the command is run from. Chosen by the owner 2026-11-17: (a), so the data is always in one place. Tests use their own throwaway file and never touch the real data.

## Token estimate

About 250,000-450,000 tokens (rough guide), plus about half a step for each fix round.
