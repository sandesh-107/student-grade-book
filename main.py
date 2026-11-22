"""Student Gradebook - menu-driven console app (ICT102 Assessment 3)
Author: Sandesh Bishwokarma, SM20252697
"""
import os

import validation as v
from display import print_students
from gradebook import Gradebook
from reports import print_summary
from storage import load_students, save_students
from student import NUM_ASSESSMENTS, WEIGHTS, grade_for

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "students.csv")

MENU = """
===== Student Gradebook =====
1. Add student
2. View all students
3. Search students
4. Update student
5. Delete student
6. Calculate final mark / assign grade
7. Rank students
8. Summary report
9. Exit
"""


def read_marks():
    marks = []
    for i in range(1, NUM_ASSESSMENTS + 1):
        marks.append(v.read_float(f"  Assessment {i} mark (0-100): ", 0, 100))
    return marks


def pick_student(book):
    """Ask for an ID until it matches a student (or the user types 'q')."""
    while True:
        sid = v.read_text("  Student ID (or q to cancel): ")
        if sid.lower() == "q":
            return None
        student = book.find_by_id(sid)
        if student:
            return student
        print("  No student with that ID.")


def add_student(book):
    name = v.read_text("  Name: ")
    marks = read_marks()
    s = book.add_student(name, marks)
    print(f"  Added {s.name} as {s.student_id}. Final {s.final_mark:.2f} ({s.grade}).")


def search_students(book):
    print("  Search by: 1) name  2) student ID  3) grade")
    choice = v.read_text("  Choice: ")
    if choice == "1":
        results = book.search_by_name(v.read_text("  Name contains: "))
    elif choice == "2":
        found = book.find_by_id(v.read_text("  Student ID: "))
        results = [found] if found else []
    elif choice == "3":
        while True:
            g = v.read_text("  Grade (HD/DN/CR/PS/FL): ").upper()
            if g in ("HD", "DN", "CR", "PS", "FL"):
                break
            print("  Not a valid grade.")
        results = book.search_by_grade(g)
    else:
        print("  Invalid choice.")
        return
    if results:
        print_students(results)
    else:
        print("  No matching students.")


def update_student(book):
    s = pick_student(book)
    if s is None:
        return
    print("  Change: 1) name  2) assessment 1  3) assessment 2  4) assessment 3")
    choice = v.read_text("  Choice: ")
    if choice == "1":
        book.update_name(s, v.read_text("  New name: "))
    elif choice in ("2", "3", "4"):
        idx = int(choice) - 2
        book.update_mark(s, idx, v.read_float(f"  New mark for assessment {idx + 1} (0-100): ", 0, 100))
    else:
        print("  Invalid choice.")
        return
    print(f"  Updated. {s.name}: final {s.final_mark:.2f} ({s.grade}).")


def delete_student(book):
    s = pick_student(book)
    if s is None:
        return
    if v.read_yes_no(f"  Delete {s.name} ({s.student_id})? (Y/N): "):
        book.delete(s)
        print("  Deleted.")
    else:
        print("  Cancelled.")


def calculate_grades(book):
    """Topic operation: show the weighting and how each student's grade came about."""
    if not book.students:
        print("\nNo records to show.")
        return
    w = " + ".join(f"{int(x * 100)}% A{i + 1}" for i, x in enumerate(WEIGHTS))
    print(f"\nFinal mark = {w}")
    for s in book.students:
        s.recalculate()
    print_students(book.students)


def main():
    students, skipped = load_students(DATA_FILE)
    book = Gradebook(students)
    print(f"Loaded {len(students)} student(s) from {DATA_FILE}")
    if skipped:
        print(f"Warning: skipped {skipped} unreadable row(s).")

    actions = {
        "1": add_student,
        "2": lambda b: print_students(b.students),
        "3": search_students,
        "4": update_student,
        "5": delete_student,
        "6": calculate_grades,
        "7": lambda b: print_students(b.ranked(), show_rank=True),
        "8": lambda b: print_summary(b.students),
    }
    try:
        while True:
            print(MENU)
            choice = input("Choose an option (1-9): ").strip()
            if choice == "9":
                break
            action = actions.get(choice)
            if action is None:
                print("Invalid choice. Please enter a number from 1 to 9.")
            else:
                action(book)
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D / Ctrl+C / closed input: still save, then leave cleanly
        print("\nInput closed. Saving before exit.")

    save_students(DATA_FILE, book.students)
    print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()
