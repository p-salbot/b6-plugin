"""Stores reorder settings per item in a SQLite file."""

import sqlite3
from collections import namedtuple
from pathlib import Path

# The data file sits in the project root (the folder that contains "reorder/"),
# no matter which folder the program is started from.
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "reorder.db"

Item = namedtuple("Item", "item_no min_qty reorder_qty supplier")

# COLLATE NOCASE: "A-100" and "a-100" are the same item.
# The CHECKs repeat the input rules as a second line of defence.
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS reorder (
    item_no     TEXT PRIMARY KEY COLLATE NOCASE
                CHECK (length(trim(item_no)) > 0),
    min_qty     INTEGER NOT NULL CHECK (min_qty >= 0),
    reorder_qty INTEGER NOT NULL CHECK (reorder_qty >= 1),
    supplier    TEXT NOT NULL CHECK (length(trim(supplier)) > 0)
)
"""

# One statement: a new item is inserted, an existing one is updated in place
# (the stored spelling of the item number is kept).
SAVE_SQL = """
INSERT INTO reorder (item_no, min_qty, reorder_qty, supplier)
VALUES (?, ?, ?, ?)
ON CONFLICT (item_no) DO UPDATE SET
    min_qty = excluded.min_qty,
    reorder_qty = excluded.reorder_qty,
    supplier = excluded.supplier
"""


class ValidationError(ValueError):
    """The input is not allowed. The message names the field and the rule."""


def _clean_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must not be empty")
    return value.strip()


def _clean_whole_number(value, label, lowest):
    # bool is a kind of int in Python, so it is refused on purpose.
    if not isinstance(value, int) or isinstance(value, bool) or value < lowest:
        raise ValidationError(f"{label} must be a whole number {lowest} or more")
    return value


def check_item(item_no, min_qty, reorder_qty, supplier):
    """Return the cleaned values as an Item, or raise ValidationError."""
    return Item(
        _clean_text(item_no, "Item number"),
        _clean_whole_number(min_qty, "Minimum stock", 0),
        _clean_whole_number(reorder_qty, "Reorder quantity", 1),
        _clean_text(supplier, "Supplier"),
    )


class ReorderStore:
    """Reorder settings in the SQLite file at db_path (":memory:" for tests)."""

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.connection = sqlite3.connect(str(db_path))
        with self.connection:
            self.connection.execute(CREATE_TABLE)

    def close(self):
        self.connection.close()

    def read(self, item_no):
        """Return the Item, or None if there is no such item."""
        item_no = _clean_text(item_no, "Item number")
        row = self.connection.execute(
            "SELECT item_no, min_qty, reorder_qty, supplier "
            "FROM reorder WHERE item_no = ?",
            (item_no,),
        ).fetchone()
        return Item(*row) if row else None

    def save(self, item_no, min_qty, reorder_qty, supplier):
        """Create the item or replace its values. All or nothing."""
        item = check_item(item_no, min_qty, reorder_qty, supplier)
        # "with" commits if all went well and rolls back if anything fails.
        with self.connection:
            self.connection.execute(SAVE_SQL, tuple(item))

    def list_all(self):
        """Return all items as a list, sorted by item number ignoring case."""
        rows = self.connection.execute(
            "SELECT item_no, min_qty, reorder_qty, supplier "
            "FROM reorder ORDER BY item_no COLLATE NOCASE"
        ).fetchall()
        return [Item(*row) for row in rows]
