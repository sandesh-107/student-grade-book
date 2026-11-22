"""Student record, final mark calculation and grade assignment."""

NUM_ASSESSMENTS = 3
WEIGHTS = (0.30, 0.30, 0.40)  # must add up to 1.0


def grade_for(mark):
    """Map a final mark to HD/DN/CR/PS/FL using the unit's grade bands."""
    if mark >= 85:
        return "HD"
    if mark >= 75:
        return "DN"
    if mark >= 65:
        return "CR"
    if mark >= 50:
        return "PS"
    return "FL"


def calculate_final(marks):
    """Weighted final mark, rounded to 2 decimals."""
    total = 0.0
    for i in range(NUM_ASSESSMENTS):
        total += marks[i] * WEIGHTS[i]
    return round(total, 2)


class Student:
    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = list(marks)
        self.final_mark = 0.0
        self.grade = "FL"
        self.recalculate()

    def recalculate(self):
        """Refresh final mark and grade after any mark changes."""
        self.final_mark = calculate_final(self.marks)
        self.grade = grade_for(self.final_mark)

    def to_row(self):
        return [self.student_id, self.name, *self.marks, self.final_mark, self.grade]
