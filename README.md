# gh-evolve

A Claude Code skill for evolutionary problem-solving over GitHub PRs.

Iteratively optimize code: each attempt is a PR with a score, the best survive, and conclusions teach the next round what to try. State lives entirely in GitHub issues and PRs.

```
GitHub Issue (root node)            <- problem definition + leaderboard
├── PR: attempt-1-baseline          <- score: 0.52
├── PR: attempt-2-mutate-of-1       <- score: 0.58
├── PR: attempt-3-mutate-of-2       <- score: 0.61  (best)
└── PR: attempt-4-crossover-2-3     <- score: 0.55  (pruned)
```

## Install

Paste into Claude Code:

```
Install the evolve skill from github.com/kaiwong-sapiens/gh-evolve
```

Requires: `gh` CLI authenticated with your GitHub account.

## Usage

Just tell Claude what you want:

```
evolve issue 1 for 3 rounds
```

```
improve the score on issue 5
```

```
set up a new evolution problem for optimizing my sort function
```

The skill handles everything: reading the issue, studying prior attempts, picking a strategy, implementing changes, evaluating, and submitting PRs.

## How it works

1. **Issue** = problem definition (objective, eval command, constraints) + leaderboard
2. **PR** = one attempt (hypothesis, method, score, conclusion)
3. **Strategy** = mutate the best, crossover two approaches, or explore something new
4. **Prune** = close low-scoring PRs when the tree grows

Each attempt's conclusion feeds into the next round's strategy. Scores provide objective signal. The leaderboard prevents going in circles.

## Setting up a problem

You need:
- A function or system to optimize
- An evaluation script that prints `SCORE: <number>`
- Constraints (what can and can't be changed)

Tell Claude to set up the problem and it creates the GitHub issue with the right structure.

## Try it

**Step 1.** Set up the problem:

```
Set up an evolve issue to maximize accuracy of estimate_pi() in solution.py.
Eval: python evaluate.py. Constraint: only modify solution.py.
```

**Step 2.** Let it rip:

```
Evolve issue 1 for 5 rounds
```

## More examples

See [kaiwong-sapiens/cache-eviction](https://github.com/kaiwong-sapiens/cache-eviction) for a larger example: evolve a cache eviction policy across diverse workloads.

## Design principles

- **No CLI, no server, no database** — just a skill and GitHub
- **Convention over code** — structured issue/PR bodies are the protocol
- **One scalar score** — the evaluation function returns a single number
- **Conclusions are memory** — each attempt teaches the next what to try

## License

MIT
