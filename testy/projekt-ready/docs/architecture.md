# Architecture

| Section | What holds today | What it means for changes | Why |
|---|---|---|---|
| Storage | Tasks live in `tasks.json` next to the code; `storage.py` reads and writes it | Any new field must be added in `storage.py` and `tasks.py` together | One small file is enough for one person |
| Task logic | `tasks.py` has add, list and mark done; it does not touch files | New operations go here and get a test in `test_tasks.py` | Keeps the logic testable without files |
| Command line | `tiny_tasks.py` parses arguments and prints | New commands are added in `build_parser` and `main` | Single entry point |
