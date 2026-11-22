"""Input helpers (FR11). Every function loops until it gets a valid value."""
import math


def read_text(prompt):
    """Ask for a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Input can't be empty. Try again.")


def read_float(prompt, low, high):
    """Ask for a number between low and high (inclusive)."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if not math.isfinite(value):
            print("  Please enter a real number.")
            continue
        if value < low or value > high:
            print(f"  Value must be between {low} and {high}.")
            continue
        return value


def read_yes_no(prompt):
    """Return True for Y, False for N."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please type Y or N.")
