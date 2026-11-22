# Student Gradebook (ICT102 Assessment 3, Topic B)
Student: Sandesh Bishwokarma (SM20252697)

A menu-driven Python console app for recording student marks, working out final marks and grades, and reporting on the class.

## Run it
Needs Python 3.8 or newer. No extra packages.

    python main.py          (or python3 main.py)

Records load from `data/students.csv` at start-up and are saved when you choose Exit (option 9). If the file is missing it gets created.

## Run the tests

    python -m unittest discover -s tests -v

## Files
- `main.py`        menu loop and user-facing actions
- `gradebook.py`   Gradebook class: add, search, update, delete, rank
- `student.py`     Student class, final mark calculation, grade bands
- `reports.py`     summary report (loops for highest/lowest/counts)
- `recursion.py`   recursive_sum (class average) and merge_sort (ranking)
- `storage.py`     CSV load/save
- `validation.py`  input helpers that re-prompt until valid
- `display.py`     aligned table output
- `tests/`         unit tests, `TEST_RESULTS.txt` has the last run

## Marking scheme used
Three assessments, each out of 100. Final mark = 30% A1 + 30% A2 + 40% A3.
HD 85-100, DN 75-84, CR 65-74, PS 50-64, FL 0-49.

## Tool acknowledgement
The claude is used for code suggestion , Syntax suggestions, and debugging
guidance.

