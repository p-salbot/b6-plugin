"""Read and write the task list stored in a JSON file."""
import json
from pathlib import Path

DEFAULT_FILE = Path(__file__).with_name("tasks.json")


def load_tasks(path=DEFAULT_FILE):
    """Return the list of tasks; an empty list if the file does not exist."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_tasks(tasks, path=DEFAULT_FILE):
    """Write the list of tasks to the file."""
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(tasks, handle, indent=2)
        handle.write("\n")
