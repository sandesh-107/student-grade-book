"""Unit tests: normal, boundary and error cases. Run: python -m unittest discover -v"""
import os
import sys
import tempfile
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import validation as v
from gradebook import Gradebook
from recursion import merge_sort, recursive_sum
from reports import build_summary
from storage import load_students, save_students
from student import Student, calculate_final, grade_for


class TestGrades(unittest.TestCase):
    def test_boundaries(self):
        cases = {100: "HD", 85: "HD", 84.99: "DN", 75: "DN", 74.99: "CR",
                 65: "CR", 64.99: "PS", 50: "PS", 49.99: "FL", 0: "FL"}
        for mark, grade in cases.items():
            self.assertEqual(grade_for(mark), grade, mark)

    def test_final_mark_weighting(self):
        self.assertEqual(calculate_final([100, 0, 0]), 30.0)
        self.assertEqual(calculate_final([0, 0, 100]), 40.0)
        self.assertEqual(calculate_final([50, 50, 50]), 50.0)


class TestRecursion(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(recursive_sum([]), 0)

    def test_single_and_many(self):
        self.assertEqual(recursive_sum([5]), 5)
        self.assertEqual(recursive_sum([1, 2, 3, 4.5]), 10.5)


class TestMergeSort(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertEqual(merge_sort([], key=lambda x: x), [])
        self.assertEqual(merge_sort([7], key=lambda x: x), [7])

    def test_sorts_and_does_not_change_input(self):
        data = [5, 2, 9, 1, 5, 6, 0]
        self.assertEqual(merge_sort(data, key=lambda x: x), [0, 1, 2, 5, 5, 6, 9])
        self.assertEqual(data, [5, 2, 9, 1, 5, 6, 0])

    def test_already_sorted_and_reversed(self):
        self.assertEqual(merge_sort([1, 2, 3, 4], key=lambda x: x), [1, 2, 3, 4])
        self.assertEqual(merge_sort([4, 3, 2, 1], key=lambda x: x), [1, 2, 3, 4])

    def test_stable_for_equal_keys(self):
        pairs = [("a", 1), ("b", 1), ("c", 0)]
        self.assertEqual(merge_sort(pairs, key=lambda p: p[1]),
                         [("c", 0), ("a", 1), ("b", 1)])

    def test_ranking_ties_sorted_by_name(self):
        book = Gradebook()
        book.add_student("Zed", [70, 70, 70])
        book.add_student("Amy", [70, 70, 70])
        self.assertEqual([s.name for s in book.ranked()], ["Amy", "Zed"])


class TestMenuFlow(unittest.TestCase):
    """Runs main.main() end to end with scripted keyboard input."""

    def run_menu(self, inputs, csv_text=None):
        import main
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "data", "s.csv")
            if csv_text is not None:
                os.makedirs(os.path.dirname(path))
                with open(path, "w") as f:
                    f.write(csv_text)
            out = io.StringIO()
            with patch.object(main, "DATA_FILE", path), \
                 patch("builtins.input", side_effect=inputs), redirect_stdout(out):
                main.main()
            with open(path) as f:
                return out.getvalue(), f.read()

    def test_invalid_choice_then_exit(self):
        out, _ = self.run_menu(["x", "", "42", "9"])
        self.assertEqual(out.count("Invalid choice"), 3)
        self.assertIn("Goodbye", out)

    def test_closed_input_saves_and_exits(self):
        csv_text = "student_id,name,mark1,mark2,mark3,final_mark,grade\nS001,Ann,50,50,50,50,PS\n"
        out, saved = self.run_menu(["2", EOFError()], csv_text)   # input closes after one action
        self.assertIn("Saving before exit", out)
        self.assertIn("Goodbye", out)
        self.assertIn("S001,Ann", saved)
        out, _ = self.run_menu([KeyboardInterrupt()], csv_text)
        self.assertIn("Goodbye", out)

    def test_add_with_bad_input_saves_on_exit(self):
        out, saved = self.run_menu(["1", "", "Ann Lee", "abc", "-1", "101", "80", "90", "100", "9"])
        self.assertIn("Added Ann Lee as S001", out)
        self.assertIn("S001,Ann Lee,80.0,90.0,100.0,91.0,HD", saved)

    def test_view_when_empty(self):
        out, _ = self.run_menu(["2", "7", "8", "9"])
        self.assertIn("No records to show", out)
        self.assertIn("nothing to report", out)

    def test_delete_needs_confirmation(self):
        csv_text = "student_id,name,mark1,mark2,mark3,final_mark,grade\nS001,Ann,50,50,50,50,PS\n"
        _, saved = self.run_menu(["5", "S001", "n", "9"], csv_text)
        self.assertIn("S001", saved)
        _, saved = self.run_menu(["5", "S999", "S001", "y", "9"], csv_text)
        self.assertNotIn("S001", saved)

    def test_update_and_search(self):
        csv_text = "student_id,name,mark1,mark2,mark3,final_mark,grade\nS001,Ann,50,50,50,50,PS\n"
        out, saved = self.run_menu(["4", "s001", "2", "100", "3", "1", "ANN", "3", "3", "cr", "9"], csv_text)
        self.assertIn("Updated", out)
        self.assertIn("S001,Ann,100.0,50.0,50.0,65.0,CR", saved)
        self.assertGreaterEqual(out.count("S001"), 2)


class TestValidation(unittest.TestCase):
    def test_text_reprompts_on_empty(self):
        with patch("builtins.input", side_effect=["", "   ", "Ann"]):
            self.assertEqual(v.read_text("> "), "Ann")

    def test_float_rejects_bad_values(self):
        bad = ["abc", "", "-5", "101", "nan", "inf", "72.5"]
        with patch("builtins.input", side_effect=bad):
            self.assertEqual(v.read_float("> ", 0, 100), 72.5)

    def test_float_accepts_boundaries(self):
        with patch("builtins.input", side_effect=["0"]):
            self.assertEqual(v.read_float("> ", 0, 100), 0.0)
        with patch("builtins.input", side_effect=["100"]):
            self.assertEqual(v.read_float("> ", 0, 100), 100.0)

    def test_yes_no(self):
        with patch("builtins.input", side_effect=["maybe", "Y"]):
            self.assertTrue(v.read_yes_no("> "))
        with patch("builtins.input", side_effect=["n"]):
            self.assertFalse(v.read_yes_no("> "))


class TestGradebook(unittest.TestCase):
    def setUp(self):
        self.book = Gradebook()
        self.book.add_student("Alice Smith", [90, 90, 90])
        self.book.add_student("bob jones", [60, 60, 60])
        self.book.add_student("Alicia Wong", [40, 40, 40])

    def test_unique_ids(self):
        ids = [s.student_id for s in self.book.students]
        self.assertEqual(ids, ["S001", "S002", "S003"])

    def test_id_not_reused_after_delete(self):
        self.book.delete(self.book.find_by_id("S002"))
        self.assertEqual(self.book.add_student("New", [50, 50, 50]).student_id, "S004")

    def test_search_case_insensitive_multiple(self):
        self.assertEqual(len(self.book.search_by_name("ALI")), 2)
        self.assertEqual(len(self.book.search_by_name("BOB")), 1)
        self.assertEqual(self.book.search_by_name("zzz"), [])
        self.assertEqual(self.book.search_by_grade("hd")[0].name, "Alice Smith")

    def test_unknown_id(self):
        self.assertIsNone(self.book.find_by_id("S999"))

    def test_update_mark_recalculates(self):
        s = self.book.find_by_id("s003")
        self.book.update_mark(s, 0, 100)
        self.book.update_mark(s, 1, 100)
        self.book.update_mark(s, 2, 100)
        self.assertEqual((s.final_mark, s.grade), (100.0, "HD"))

    def test_ranking_order(self):
        names = [s.name for s in self.book.ranked()]
        self.assertEqual(names, ["Alice Smith", "bob jones", "Alicia Wong"])


class TestReport(unittest.TestCase):
    def test_empty_returns_none(self):
        self.assertIsNone(build_summary([]))

    def test_values(self):
        students = [Student("S001", "A", [90, 90, 90]),
                    Student("S002", "B", [60, 60, 60]),
                    Student("S003", "C", [30, 30, 30])]
        r = build_summary(students)
        self.assertEqual(r["average"], 60.0)
        self.assertEqual(r["highest"].name, "A")
        self.assertEqual(r["lowest"].name, "C")
        self.assertEqual(r["grade_counts"], {"HD": 1, "DN": 0, "CR": 0, "PS": 1, "FL": 1})


class TestStorage(unittest.TestCase):
    def test_creates_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "newdata", "s.csv")
            students, skipped = load_students(path)
            self.assertEqual((students, skipped), ([], 0))
            self.assertTrue(os.path.exists(path))

    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "s.csv")
            save_students(path, [Student("S001", "Zed, Jr.", [70, 80, 90])])
            students, _ = load_students(path)
            self.assertEqual(students[0].name, "Zed, Jr.")
            self.assertEqual(students[0].final_mark, 81.0)
            self.assertEqual(students[0].marks, [70.0, 80.0, 90.0])

    def test_bad_rows_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "s.csv")
            with open(path, "w") as f:
                f.write("student_id,name,mark1,mark2,mark3,final_mark,grade\n"
                        "S001,Good,50,50,50,50,PS\n"
                        "S002,BadMark,abc,50,50,0,FL\n"
                        "S003,OutOfRange,150,50,50,0,FL\n"
                        "S004,,50,50,50,50,PS\n")
            students, skipped = load_students(path)
            self.assertEqual((len(students), skipped), (1, 3))


if __name__ == "__main__":
    unittest.main()
