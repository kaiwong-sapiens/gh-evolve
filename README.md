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

First, set up a problem (creates a structured GitHub issue):

```
Use evolve skill to set up: <what you want to optimize>
```

Then evolve it:

```
Evolve issue <number> for 3 rounds
```

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

**Step 1.** Pick an example and paste into Claude Code:

Pi approximation:
```text
Use evolve skill to set up: approximate pi.
No math module, only basic arithmetic.
```

Trading strategy:
```text
Use evolve skill to set up: optimize a trading
strategy by Sharpe ratio across market scenarios.
```

**Step 2.** Review the issue on GitHub, then paste:

```text
Evolve issue 1 for 3 rounds
```

## License

MIT
