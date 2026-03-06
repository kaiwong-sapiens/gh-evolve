"""
String similarity function to evolve.

Modify this function to maximize correlation with human similarity judgments.
The function should return a float between 0.0 (completely different) and
1.0 (identical).
"""


def similarity(a: str, b: str) -> float:
    """Baseline: simple length ratio."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return min(len(a), len(b)) / max(len(a), len(b))
