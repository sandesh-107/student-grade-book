"""FR8: summary report. Highest/lowest/counts use plain loops; the total uses recursion."""
from recursion import recursive_sum

GRADES = ["HD", "DN", "CR", "PS", "FL"]


def build_summary(students):
    """Return a dict of report values, or None if there are no students."""
    if len(students) == 0:
        return None

    highest = students[0]
    lowest = students[0]
    counts = {g: 0 for g in GRADES}
    for s in students:
        if s.final_mark > highest.final_mark:
            highest = s
        if s.final_mark < lowest.final_mark:
            lowest = s
        counts[s.grade] += 1

    finals = [s.final_mark for s in students]
    average = recursive_sum(finals) / len(students)
    return {
        "count": len(students),
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "grade_counts": counts,
    }


def print_summary(students):
    summary = build_summary(students)
    if summary is None:
        print("\nNo students yet, so there's nothing to report.")
        return
    print("\n=== Class Summary ===")
    print(f"Students       : {summary['count']}")
    print(f"Class average  : {summary['average']:.2f}")
    h, l = summary["highest"], summary["lowest"]
    print(f"Highest mark   : {h.final_mark:.2f} ({h.name})")
    print(f"Lowest mark    : {l.final_mark:.2f} ({l.name})")
    print("Count per grade:")
    for g in GRADES:
        print(f"  {g}: {summary['grade_counts'][g]}")
