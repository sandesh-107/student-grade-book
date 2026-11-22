"""Gradebook: holds the student list and does add/search/update/delete/rank."""
from recursion import merge_sort
from student import Student


class Gradebook:
    def __init__(self, students=None):
        self.students = students if students is not None else []

    def next_id(self):
        """Next free ID in the form S001, S002, ... (never reuses a number)."""
        highest = 0
        for s in self.students:
            digits = s.student_id[1:]
            if digits.isdigit() and int(digits) > highest:
                highest = int(digits)
        return f"S{highest + 1:03d}"

    def add_student(self, name, marks):
        student = Student(self.next_id(), name, marks)
        self.students.append(student)
        return student

    def find_by_id(self, student_id):
        for s in self.students:
            if s.student_id.lower() == student_id.strip().lower():
                return s
        return None

    def search_by_name(self, text):
        text = text.strip().lower()
        return [s for s in self.students if text in s.name.lower()]

    def search_by_grade(self, grade):
        grade = grade.strip().upper()
        return [s for s in self.students if s.grade == grade]

    def update_name(self, student, new_name):
        student.name = new_name

    def update_mark(self, student, index, new_mark):
        student.marks[index] = new_mark
        student.recalculate()

    def delete(self, student):
        self.students.remove(student)

    def ranked(self):
        """Students ordered by final mark, highest first (ties by name).

        Uses the recursive merge_sort from recursion.py.
        """
        return merge_sort(self.students, lambda s: (-s.final_mark, s.name.lower()))
