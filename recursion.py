"""FR10: recursive helper used by the summary report."""


def recursive_sum(values):
    """Add up a list of numbers recursively.

    Base case:      an empty list sums to 0.
    Recursive case: first item + the sum of everything after it.
    """
    if len(values) == 0:
        return 0
    return values[0] + recursive_sum(values[1:])


def merge_sort(items, key):
    """Sort a list recursively (merge sort), smallest key first. Returns a new list.

    Base case:      a list of 0 or 1 items is already sorted.
    Recursive case: sort each half, then merge the two sorted halves.
    Recursion depth is only about log2(n), so it is safe for any realistic class size.
    """
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    """Merge two sorted lists into one. Stable: ties keep their original order."""
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if key(right[j]) < key(left[i]):
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged
