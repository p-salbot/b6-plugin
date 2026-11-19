"""Operations on the task list: add, list and mark done."""


def add_task(tasks, title):
    """Add a new open task and return it; raise ValueError if the title is empty."""
    if not title.strip():
        raise ValueError("Title must not be empty")
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    return task


def list_tasks(tasks, include_done=True):
    """Return the tasks, optionally only the open ones."""
    return [task for task in tasks if include_done or not task["done"]]


def mark_done(tasks, task_id):
    """Mark the task as done; raise KeyError if there is no such task."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return task
    raise KeyError(task_id)


def format_task(task):
    """Return one line of text for a task."""
    mark = "x" if task["done"] else " "
    return "[{}] {}. {}".format(mark, task["id"], task["title"])
