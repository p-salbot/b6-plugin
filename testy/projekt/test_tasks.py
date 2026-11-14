import unittest

from tasks import add_task, list_tasks, mark_done


class TaskTests(unittest.TestCase):
    def test_add_gives_next_id(self):
        tasks = [{"id": 4, "title": "a", "done": False}]
        self.assertEqual(add_task(tasks, "b")["id"], 5)

    def test_list_only_open(self):
        tasks = [{"id": 1, "title": "a", "done": True},
                 {"id": 2, "title": "b", "done": False}]
        self.assertEqual([t["id"] for t in list_tasks(tasks, include_done=False)], [2])

    def test_done_unknown_id(self):
        with self.assertRaises(KeyError):
            mark_done([], 1)


if __name__ == "__main__":
    unittest.main()
