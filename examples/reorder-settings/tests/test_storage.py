import sqlite3
import unittest

from reorder.storage import ReorderStore, ValidationError

MIN_MESSAGE = "Minimum stock must be a whole number 0 or more"
REORDER_MESSAGE = "Reorder quantity must be a whole number 1 or more"


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.store = ReorderStore(":memory:")
        self.addCleanup(self.store.close)

    def count_rows(self):
        return self.store.connection.execute(
            "SELECT COUNT(*) FROM reorder"
        ).fetchone()[0]

    def test_r002_save_then_read_returns_new_values(self):
        self.store.save("A-100", 5, 20, "Acme")
        self.assertEqual(tuple(self.store.read("A-100")), ("A-100", 5, 20, "Acme"))

    def test_r002_saving_again_replaces_values_with_one_row(self):
        self.store.save("A-100", 5, 20, "Acme")
        self.store.save("A-100", 7, 30, "Bolt Co")
        self.assertEqual(tuple(self.store.read("A-100")), ("A-100", 7, 30, "Bolt Co"))
        self.assertEqual(self.count_rows(), 1)

    def test_r002_read_unknown_item_returns_none(self):
        self.assertIsNone(self.store.read("nope"))

    def test_r002_list_is_sorted_ignoring_case(self):
        self.store.save("b-2", 1, 1, "X")
        self.store.save("A-1", 1, 1, "X")
        self.store.save("C-3", 1, 1, "X")
        self.assertEqual([i.item_no for i in self.store.list_all()],
                         ["A-1", "b-2", "C-3"])

    def test_r003_failed_save_keeps_old_values(self):
        self.store.save("A-100", 5, 20, "Acme")
        # A trigger that fails after the update has been made.
        self.store.connection.execute(
            "CREATE TRIGGER boom AFTER UPDATE ON reorder "
            "BEGIN SELECT RAISE(ABORT, 'simulated failure'); END"
        )
        with self.assertRaises(sqlite3.Error):
            self.store.save("A-100", 99, 99, "Other")
        self.assertEqual(tuple(self.store.read("A-100")), ("A-100", 5, 20, "Acme"))
        self.assertEqual(self.count_rows(), 1)

    def test_r004_bad_input_is_refused_and_data_unchanged(self):
        self.store.save("A-100", 5, 20, "Acme")
        bad_inputs = [
            (("", 5, 20, "Acme"), "Item number must not be empty"),
            (("   ", 5, 20, "Acme"), "Item number must not be empty"),
            (("A-100", 5, 20, ""), "Supplier must not be empty"),
            (("A-100", 5, 20, "  "), "Supplier must not be empty"),
            (("A-100", -1, 20, "Acme"), MIN_MESSAGE),
            (("A-100", 1.5, 20, "Acme"), MIN_MESSAGE),
            (("A-100", True, 20, "Acme"), MIN_MESSAGE),
            (("A-100", "5", 20, "Acme"), MIN_MESSAGE),
            (("A-100", 5, 0, "Acme"), REORDER_MESSAGE),
            (("A-100", 5, 2.0, "Acme"), REORDER_MESSAGE),
        ]
        for args, message in bad_inputs:
            with self.subTest(args=args):
                with self.assertRaises(ValidationError) as caught:
                    self.store.save(*args)
                self.assertEqual(str(caught.exception), message)
        self.assertEqual(tuple(self.store.read("A-100")), ("A-100", 5, 20, "Acme"))
        self.assertEqual(self.count_rows(), 1)

    def test_r004_zero_min_is_allowed(self):
        self.store.save("A-100", 0, 1, "Acme")
        self.assertEqual(self.store.read("A-100").min_qty, 0)

    def test_r004_spaces_at_the_ends_are_removed(self):
        self.store.save("  A-100 ", 5, 20, " Acme  ")
        self.assertEqual(tuple(self.store.read("A-100")), ("A-100", 5, 20, "Acme"))

    def test_r004_database_checks_refuse_bad_rows_too(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.connection.execute(
                "INSERT INTO reorder VALUES ('X', -1, 1, 'S')")
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.connection.execute(
                "INSERT INTO reorder VALUES ('X', 0, 0, 'S')")

    def test_r005_special_characters_come_back_exactly(self):
        texts = ["O'Brien", 'say "hi"', "a;b", "x--y", "Müller",
                 "'; DROP TABLE reorder; --"]
        for number, text in enumerate(texts):
            with self.subTest(text=text):
                item_no = f"I{number}-{text}"
                self.store.save(item_no, 1, 1, text)
                found = self.store.read(item_no)
                self.assertEqual(found.item_no, item_no)
                self.assertEqual(found.supplier, text)

    def test_r005_apostrophe_supplier(self):
        self.store.save("A-100", 1, 1, "O'Brien")
        self.assertEqual(self.store.read("A-100").supplier, "O'Brien")

    def test_r007_read_ignores_case(self):
        self.store.save("A-100", 5, 20, "Acme")
        self.assertEqual(tuple(self.store.read("a-100")), ("A-100", 5, 20, "Acme"))

    def test_r007_save_with_other_case_updates_and_keeps_spelling(self):
        self.store.save("A-100", 5, 20, "Acme")
        self.store.save("a-100", 8, 40, "Bolt Co")
        self.assertEqual(self.count_rows(), 1)
        self.assertEqual(tuple(self.store.read("A-100")), ("A-100", 8, 40, "Bolt Co"))


if __name__ == "__main__":
    unittest.main()
