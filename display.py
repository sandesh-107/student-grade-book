"""Aligned table output (FR3)."""


def print_students(students, show_rank=False):
    if len(students) == 0:
        print("\nNo records to show.")
        return
    rank_head = f"{'Rank':<5}" if show_rank else ""
    print()
    print(f"{rank_head}{'ID':<6}{'Name':<22}{'A1':>7}{'A2':>7}{'A3':>7}{'Final':>8}  Grade")
    print("-" * (len(rank_head) + 64))
    for i, s in enumerate(students, start=1):
        rank = f"{i:<5}" if show_rank else ""
        print(f"{rank}{s.student_id:<6}{s.name[:21]:<22}"
              f"{s.marks[0]:>7.1f}{s.marks[1]:>7.1f}{s.marks[2]:>7.1f}"
              f"{s.final_mark:>8.2f}  {s.grade}")
