"""Command line: show, save and list reorder settings."""

import argparse
import re
import sys

from reorder.storage import ReorderStore, ValidationError


_WHOLE_NUMBER = re.compile(r"[+-]?[0-9]+")


def _to_number(text):
    """Turn text into a whole number. Only an optional sign and the digits 0-9 count.
    Anything else is returned unchanged: the storage check then refuses it with a
    message naming the field."""
    if _WHOLE_NUMBER.fullmatch(text.strip()):
        return int(text)
    return text


def configure_output(*streams):
    """Write in UTF-8 and never fail on a character (a pipe on Windows uses cp1252)."""
    for stream in streams:
        stream.reconfigure(encoding="utf-8", errors="replace")


def _build_parser():
    parser = argparse.ArgumentParser(prog="python -m reorder")
    commands = parser.add_subparsers(dest="command", required=True)

    show = commands.add_parser("show", help="show the settings of one item")
    show.add_argument("item")

    save = commands.add_parser("save", help="create an item or replace its values")
    save.add_argument("item")
    # The numbers are read as text so that bad input gets our own message.
    save.add_argument("--min", required=True, help="minimum stock (0 or more)")
    save.add_argument("--reorder", required=True, help="reorder quantity (1 or more)")
    save.add_argument("--supplier", required=True)

    commands.add_parser("list", help="list all items")
    return parser


def _show(store, args):
    item = store.read(args.item)
    if item is None:
        print(f"Item '{args.item}' not found.", file=sys.stderr)
        return 1
    print(f"Item:          {item.item_no}")
    print(f"Minimum stock: {item.min_qty}")
    print(f"Reorder qty:   {item.reorder_qty}")
    print(f"Supplier:      {item.supplier}")
    return 0


def _save(store, args):
    store.save(args.item, _to_number(args.min), _to_number(args.reorder), args.supplier)
    item = store.read(args.item)
    print(
        f"Saved {item.item_no}: minimum stock {item.min_qty}, "
        f"reorder qty {item.reorder_qty}, supplier {item.supplier}"
    )
    return 0


def _list(store, args):
    items = store.list_all()
    if not items:
        print("No items.")
        return 0
    rows = [("Item", "Minimum stock", "Reorder qty", "Supplier")]
    rows += [(i.item_no, str(i.min_qty), str(i.reorder_qty), i.supplier) for i in items]
    widths = [max(len(row[col]) for row in rows) for col in range(4)]
    for row in rows:
        cells = [row[col].ljust(widths[col]) for col in range(3)]
        print("  ".join(cells + [row[3]]))
    return 0


COMMANDS = {"show": _show, "save": _save, "list": _list}


def main(argv=None, store=None):
    """Run one command and return the exit code (0 = ok, 1 = error)."""
    args = _build_parser().parse_args(argv)
    own_store = store is None
    if own_store:
        store = ReorderStore()
    try:
        return COMMANDS[args.command](store, args)
    except ValidationError as error:
        print(error, file=sys.stderr)
        return 1
    finally:
        if own_store:
            store.close()
