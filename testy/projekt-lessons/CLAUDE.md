# Tiny Tasks

Small Python command line app for a to-do list (add, list, done). Tasks are stored in `tasks.json`.
Run the tests with `python3 -m unittest`.

Work status is in `ctx/TASKS.md`, requirements in `ctx/requirements.md`, architecture in `docs/architecture.md`.
For building and changes, follow the method of the `b6` plugin (skill `workflow`), not another brainstorming or planning skill.
Project documents are written in English.

## Lessons

- 2026-06-02: Keep `tasks.json` in the repository with three sample tasks; tests must not write to it.
- 2026-06-20: Task ids are never reused after `done`; new ids come from the highest id plus one.
- 2026-07-08: Print messages for the owner in plain English, without Python tracebacks.
- 2026-07-25: Save `tasks.json` with an indent of 2 and a newline at the end, so changes stay readable.
- 2026-08-11: A new command gets an example line in `README.md` in the same change.
- 2026-08-29: Read and write files as UTF-8, so titles with accents survive.
- 2026-09-14: Keep `storage.py` the only module that opens files.
- 2026-09-30: Command names stay short English verbs (`add`, `list`, `done`).
- 2026-10-17: Options of `list` are flags (`--open`), not extra commands.
- 2026-11-03: Trial runs of `tiny_tasks.py` use a copy of the project in the run's `scratch/`, never the real `tasks.json`.
