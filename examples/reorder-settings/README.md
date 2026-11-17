# Reorder settings

A small command line tool that stores, for each item, the minimum stock, the reorder quantity and the supplier. It replaces the old Access tool (see `old/`).

## Install

You need Python 3.8 or newer with SQLite 3.24 or newer (tested with Python 3.13 and SQLite 3.50). Nothing else to install: the tool uses only the Python standard library.

Check your version:

    python --version
    python -c "import sqlite3; print(sqlite3.sqlite_version)"

The Python from python.org on Windows brings a new enough SQLite.

## Run

Open a terminal in the project folder (the folder that contains `reorder/`). **Always start the tool from that folder**, otherwise Python does not find it.

    python -m reorder COMMAND ...

There are three commands.

### save: create an item or replace its values

    python -m reorder save A-100 --min 5 --reorder 20 --supplier "Smith Tools"

    Saved A-100: minimum stock 5, reorder qty 20, supplier Smith Tools

All three options (`--min`, `--reorder`, `--supplier`) are required. If the item already exists, its values are replaced (the stored spelling of the item number stays). If not, it is created.

Put a supplier with spaces or an apostrophe in double quotes. This works in PowerShell and in cmd:

    python -m reorder save b-7 --min 0 --reorder 1 --supplier "O'Brien"

    Saved b-7: minimum stock 0, reorder qty 1, supplier O'Brien

### show: one item

    python -m reorder show a-100

    Item:          A-100
    Minimum stock: 5
    Reorder qty:   20
    Supplier:      Smith Tools

If the item does not exist, the message `Item 'Z-1' not found.` is printed (exit code 1).

### list: all items

    python -m reorder list

    Item   Minimum stock  Reorder qty  Supplier
    A-100  5              20           Smith Tools
    b-7    0              1            O'Brien

Items are sorted by item number, ignoring case. With no items it prints `No items.`

### Input rules

- Item number and supplier must not be empty. Spaces at the start and end are removed.
- Minimum stock and reorder quantity must be whole numbers (digits 0-9, optional sign; no decimals).
- Minimum stock: 0 or more. Reorder quantity: 1 or more.
- Item numbers match ignoring upper/lower case for the letters A-Z (`a-100` is `A-100`). Other letters, such as `Ü` and `ü`, count as different.
- A refused save changes nothing.

### Error messages

| Message | Cause |
|---|---|
| `Item number must not be empty` | empty or only spaces |
| `Supplier must not be empty` | empty or only spaces |
| `Minimum stock must be a whole number 0 or more` | not a whole number, or below 0 |
| `Reorder quantity must be a whole number 1 or more` | not a whole number, or below 1 |
| `Item 'Z-1' not found.` | `show` for an item that does not exist |
| `usage: ... error: the following arguments are required: ...` | a missing item or option |
| `usage: ... error: argument command: invalid choice: ...` | an unknown command |

Messages go to standard error, results to standard output.

### Exit codes

- 0: ok
- 1: item not found, or input refused
- 2: usage mistake (for example a missing option)

## The data file

The data is kept in `reorder.db` in the project folder. It is created on the first command that runs, and it is not stored in git. To make a backup, copy the file while the tool is not running.

## Output encoding

Output is always UTF-8, also when saved to a file:

    python -m reorder list > items.txt

## Tests

From the project folder:

    python -m unittest

Add `-v` to see each test. The tests never touch `reorder.db`; they use a temporary in-memory database.

## For maintainers

Where things are:

- `reorder/storage.py`: the SQLite table, the input checks, saving and reading
- `reorder/cli.py`: the commands and their output
- `reorder/__main__.py`: starts `python -m reorder`
- `tests/`: the tests
- `old/`: the old Access tool, for reference
- `docs/architecture.md`: how it is built
- `docs/decisions/`: why it is built this way

Before a change, read `docs/architecture.md`, especially the column "What it means for changes". Decisions are in `docs/decisions/`.

Two rules not to break:

1. Saving is all or nothing, and all SQL uses `?` parameters (never put text into the SQL string).
2. A new input rule goes into both the Python check (`storage.py`) and the table `CHECK`.
