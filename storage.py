"""FR9: CSV load/save. Creates the file on first run."""
import csv
import os

from student import Student, NUM_ASSESSMENTS

FIELDNAMES = ["student_id", "name", "mark1", "mark2", "mark3", "final_mark", "grade"]


def ensure_file(path):
    """Create the data folder and an empty CSV (header only) if missing."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDNAMES)


def load_students(path):
    """Read students from CSV. Bad rows are skipped, not fatal.

    Final mark and grade are recalculated rather than trusted from the file.
    Returns (students, number_of_skipped_rows).
    """
    ensure_file(path)
    students = []
    skipped = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                marks = [float(row[f"mark{i}"]) for i in range(1, NUM_ASSESSMENTS + 1)]
                if any(m < 0 or m > 100 for m in marks):
                    raise ValueError("mark out of range")
                name = row["name"].strip()
                sid = row["student_id"].strip()
                if not name or not sid:
                    raise ValueError("missing field")
                students.append(Student(sid, name, marks))
            except (KeyError, ValueError, TypeError, AttributeError):
                skipped += 1
    return students, skipped


def save_students(path, students):
    ensure_file(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)
        for s in students:
            writer.writerow(s.to_row())
