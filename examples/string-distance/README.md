# Example: Evolve a String Similarity Function

A simple problem to demonstrate gh-evolve. The goal is to write a function
that scores how similar two strings are, optimized against a benchmark of
human-judged similarity pairs.

## Setup

```bash
cd examples/string-distance
pip install -r requirements.txt  # no dependencies beyond stdlib

# Initialize the evolution problem
evolve init \
  --title "String similarity function" \
  --objective "Write a string similarity function that maximizes correlation with human judgments" \
  --eval "python evaluate.py" \
  --constraint "Function must run in under 1ms per pair. Pure Python only (no C extensions)."
```

## How it works

- `solution.py` contains the function to evolve: `similarity(a: str, b: str) -> float`
- `benchmark.json` contains 50 string pairs with human-judged similarity scores (0-1)
- `evaluate.py` runs the solution against the benchmark and prints a Spearman correlation score

## Try it

1. Start with the baseline in `solution.py` (simple length-ratio)
2. Run `python evaluate.py` to see the baseline score
3. Use `evolve start`, modify `solution.py`, run `evolve submit`
4. Repeat — each attempt tries to beat the previous best
