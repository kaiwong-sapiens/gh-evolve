"""
Generate a benchmark dataset of string pairs with similarity scores.

Scores are based on normalized Levenshtein distance (the "ground truth"
that participants try to approximate without using Levenshtein directly).
"""

import json
import random

PAIRS = [
    # Identical
    ("hello", "hello", 1.0),
    ("world", "world", 1.0),
    # Typos / near-matches
    ("kitten", "sitting", 0.57),
    ("saturday", "sunday", 0.50),
    ("apple", "aple", 0.80),
    ("banana", "bananna", 0.86),
    ("algorithm", "altruistic", 0.30),
    ("python", "pyhton", 0.67),
    ("github", "githu", 0.83),
    ("evolution", "revolution", 0.90),
    # Substring / overlap
    ("test", "testing", 0.57),
    ("evolve", "evolving", 0.63),
    ("data", "database", 0.50),
    ("sun", "sunshine", 0.38),
    ("book", "bookshelf", 0.44),
    # Anagrams
    ("listen", "silent", 0.33),
    ("earth", "heart", 0.40),
    ("race", "care", 0.25),
    ("state", "taste", 0.40),
    ("angel", "angle", 0.60),
    # Completely different
    ("cat", "helicopter", 0.00),
    ("xyz", "abcdef", 0.00),
    ("moon", "spoon", 0.60),
    ("light", "night", 0.80),
    ("train", "brain", 0.60),
    # Different lengths
    ("a", "abcdefghij", 0.10),
    ("ab", "abcdefghij", 0.20),
    ("abc", "abcdefghij", 0.30),
    ("abcd", "abcdefghij", 0.40),
    ("abcde", "abcdefghij", 0.50),
    # Prefix matches
    ("micro", "microscope", 0.50),
    ("auto", "automobile", 0.40),
    ("tele", "telephone", 0.44),
    ("pre", "prediction", 0.30),
    ("un", "understand", 0.20),
    # Suffix matches
    ("tion", "nation", 0.67),
    ("ness", "happiness", 0.44),
    ("ing", "running", 0.43),
    ("able", "comfortable", 0.36),
    ("ment", "government", 0.40),
    # Character swaps
    ("abcdef", "abcdfe", 0.67),
    ("string", "strign", 0.67),
    ("search", "saerch", 0.67),
    ("friend", "freind", 0.67),
    ("receive", "recieve", 0.86),
    # Empty / edge cases
    ("", "", 1.0),
    ("a", "", 0.0),
    ("", "b", 0.0),
    ("x", "x", 1.0),
    ("ab", "ba", 0.50),
    ("abc", "cba", 0.33),
]


def main():
    benchmark = [{"a": a, "b": b, "score": s} for a, b, s in PAIRS]
    random.seed(42)
    random.shuffle(benchmark)

    with open("benchmark.json", "w") as f:
        json.dump(benchmark, f, indent=2)

    print(f"Generated {len(benchmark)} pairs in benchmark.json")


if __name__ == "__main__":
    main()
