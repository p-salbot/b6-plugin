import contextlib
import io
import unittest

from reorder.cli import configure_output, main
from reorder.storage import ReorderStore

MIN_MESSAGE = "Minimum stock must be a whole number 0 or more"
REORDER_MESSAGE = "Reorder quantity must be a whole number 1 or more"


class CliTests(unittest.TestCase):
    def setUp(self):
        self.store = ReorderStore(":memory:")
        self.addCleanup(self.store.close)

    def run_cli(self, *argv):
        """Run a command; return (exit code, standard output, standard error)."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(argv), store=self.store)
        return code, out.getvalue(), err.getvalue()

    def save(self, item="A-100", minimum="5", reorder="20", supplier="Acme"):
        return self.run_cli("save", item, "--min", minimum,
                            "--reorder", reorder, "--supplier", supplier)

    def test_r001_show_known_item_prints_all_fields(self):
        self.save()
        code, out, err = self.run_cli("show", "A-100")
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), [
            "Item:          A-100",
            "Minimum stock: 5",
            "Reorder qty:   20",
            "Supplier:      Acme",
        ])
        self.assertEqual(err, "")

    def test_r001_show_unknown_item_prints_only_not_found(self):
        code, out, err = self.run_cli("show", "X-1")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertEqual(err, "Item 'X-1' not found.\n")

    def test_r002_save_then_show_returns_new_values(self):
        code, out, _ = self.save()
        self.assertEqual(code, 0)
        self.assertEqual(
            out, "Saved A-100: minimum stock 5, reorder qty 20, supplier Acme\n")
        self.assertIn("Minimum stock: 5", self.run_cli("show", "A-100")[1])

    def test_r002_saving_again_replaces_values_with_one_row(self):
        self.save()
        self.save(minimum="7", reorder="30", supplier="Bolt Co")
        out = self.run_cli("show", "A-100")[1]
        self.assertIn("Minimum stock: 7", out)
        self.assertIn("Reorder qty:   30", out)
        self.assertIn("Supplier:      Bolt Co", out)
        listing = self.run_cli("list")[1].splitlines()
        self.assertEqual(len(listing), 2)  # header + one row

    def assert_refused(self, message, **fields):
        self.save()
        before = self.store.list_all()
        code, out, err = self.save(**fields)
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn(message, err)
        self.assertEqual(self.store.list_all(), before)

    def test_r004_empty_supplier_is_refused(self):
        self.assert_refused("Supplier must not be empty", supplier="   ")

    def test_r004_empty_item_is_refused(self):
        self.assert_refused("Item number must not be empty", item=" ")

    def test_r004_negative_min_is_refused(self):
        self.assert_refused(MIN_MESSAGE, minimum="-1")

    def test_r004_text_as_min_is_refused(self):
        self.assert_refused(MIN_MESSAGE, minimum="abc")

    def test_r004_reorder_zero_is_refused(self):
        self.assert_refused(REORDER_MESSAGE, reorder="0")

    def test_r004_text_as_reorder_is_refused(self):
        self.assert_refused(REORDER_MESSAGE, reorder="1.5")

    def test_r004_underscore_in_reorder_is_refused(self):
        self.assert_refused(REORDER_MESSAGE, reorder="1_0")

    def test_r004_full_width_digit_in_min_is_refused(self):
        self.assert_refused(MIN_MESSAGE, minimum="\uff15")

    def test_r004_spaces_around_number_are_allowed(self):
        code, _, _ = self.save(minimum=" 5 ")
        self.assertEqual(code, 0)
        self.assertIn("Minimum stock: 5", self.run_cli("show", "A-100")[1])

    def test_r004_bad_new_item_is_not_stored(self):
        code, _, _ = self.save(item="B-1", minimum="-1")
        self.assertEqual(code, 1)
        self.assertEqual(self.store.list_all(), [])

    def test_r005_apostrophe_in_supplier_is_kept(self):
        self.save(supplier="O'Brien")
        out = self.run_cli("show", "A-100")[1]
        self.assertIn("Supplier:      O'Brien\n", out)

    def test_r006_list_is_sorted_by_item_number(self):
        self.save(item="B-2", supplier="Bolt Co")
        self.save(item="A-1", minimum="10", reorder="100")
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        lines = out.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0].split(), ["Item", "Minimum", "stock",
                                            "Reorder", "qty", "Supplier"])
        self.assertEqual(lines[1].split(), ["A-1", "10", "100", "Acme"])
        self.assertEqual(lines[2].split(), ["B-2", "5", "20", "Bolt", "Co"])
        # Columns are aligned: the supplier starts at the same place.
        self.assertEqual(lines[1].index("Acme"), lines[2].index("Bolt Co"))

    def test_r006_list_without_items_says_no_items(self):
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertEqual(out, "No items.\n")

    def test_r007_show_ignores_upper_and_lower_case(self):
        self.save(item="A-100")
        code, out, _ = self.run_cli("show", "a-100")
        self.assertEqual(code, 0)
        self.assertIn("Item:          A-100", out)

    def test_r007_saving_other_spelling_updates_the_item(self):
        self.save(item="A-100")
        self.save(item="a-100", minimum="9")
        listing = self.run_cli("list")[1].splitlines()
        self.assertEqual(len(listing), 2)  # header + one row
        self.assertIn("Minimum stock: 9", self.run_cli("show", "A-100")[1])

    def test_r005_output_is_utf_8_and_never_fails(self):
        out = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
        err = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
        configure_output(out, err)
        text = "\u0141\u00f3d\u017a M\u00fcller"
        for stream in (out, err):
            stream.write(text)
            stream.flush()
            self.assertEqual(stream.buffer.getvalue(), text.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
