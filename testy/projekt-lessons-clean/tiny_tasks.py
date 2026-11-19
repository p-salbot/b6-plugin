"""Command line entry point: python3 tiny_tasks.py add|list|done."""
import argparse

from storage import load_tasks, save_tasks
from tasks import add_task, format_task, list_tasks, mark_done


def build_parser():
    parser = argparse.ArgumentParser(description="Tiny Tasks")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="add a task")
    add.add_argument("title")
    listing = commands.add_parser("list", help="show tasks")
    listing.add_argument("--open", action="store_true", help="only open tasks")
    done = commands.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    tasks = load_tasks()
    if args.command == "add":
        try:
            print(format_task(add_task(tasks, args.title)))
        except ValueError as problem:
            print(problem)
            return 1
    elif args.command == "list":
        for task in list_tasks(tasks, include_done=not args.open):
            print(format_task(task))
    else:
        try:
            print(format_task(mark_done(tasks, args.id)))
        except KeyError:
            print("No task with id {}".format(args.id))
            return 1
    save_tasks(tasks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
