"""
Evaluate the solution against the benchmark.

Prints a single score: Spearman rank correlation between the solution's
similarity scores and the human-judged ground truth.
"""

import json
import sys
import time


def spearman_correlation(x, y):
    """Compute Spearman rank correlation without scipy."""
    n = len(x)
    if n < 2:
        return 0.0

    def rankdata(vals):
        indexed = sorted(enumerate(vals), key=lambda t: t[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and indexed[j + 1][1] == indexed[j][1]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = avg_rank
            i = j + 1
        return ranks

    rx = rankdata(x)
    ry = rankdata(y)

    d_sq = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - (6 * d_sq) / (n * (n ** 2 - 1))


def main():
    # Import the solution
    sys.path.insert(0, ".")
    from solution import similarity

    # Load benchmark
    with open("benchmark.json") as f:
        benchmark = json.load(f)

    # Run evaluation
    predicted = []
    actual = []
    total_time = 0

    for pair in benchmark:
        start = time.perf_counter()
        score = similarity(pair["a"], pair["b"])
        elapsed = time.perf_counter() - start
        total_time += elapsed

        predicted.append(score)
        actual.append(pair["score"])

        if elapsed > 0.001:
            print(f"WARNING: similarity({pair['a']!r}, {pair['b']!r}) took {elapsed*1000:.1f}ms (>1ms limit)")

    avg_time = total_time / len(benchmark) * 1000
    correlation = spearman_correlation(predicted, actual)

    print(f"Pairs evaluated: {len(benchmark)}")
    print(f"Avg time per pair: {avg_time:.3f}ms")
    print(f"Spearman correlation: {correlation:.4f}")
    print(f"SCORE: {correlation:.4f}")


if __name__ == "__main__":
    main()
