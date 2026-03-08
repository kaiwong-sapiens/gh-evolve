# gh-evolve

An AI agent skill for evolutionary problem-solving over GitHub PRs. Works with Claude Code and Gemini CLI.

Each attempt is a PR with metrics and a conclusion. The best survive, the rest are pruned, and each conclusion teaches the next round what to try. All state lives in GitHub issues and PRs — no external tools required.

```
GitHub Issue (root node)            <- problem definition + leaderboard
├── PR: attempt-1-baseline          <- score: 0.52
├── PR: attempt-2-mutate-of-1       <- score: 0.58
├── PR: attempt-3-mutate-of-2       <- score: 0.61  (best)
└── PR: attempt-4-crossover-2-3     <- score: 0.55  (pruned)
```

## Install

Paste into your CLI:

```
Install the evolve skill from github.com/kaiwong-sapiens/gh-evolve
```

Requires: `gh` CLI authenticated with your GitHub account.

## Usage

Create a problem (this sets up a structured GitHub issue):

```
Use evolve skill to create an issue: <what you want to optimize>
```

Evolve it:

```
Evolve issue <number> for 3 rounds
```

When satisfied, finalize to merge the winner and clean up:

```
Finalize evolve issue <number>
```

## Try it

**Step 1.** Pick an example and paste the prompt into your CLI:

Pi approximation (example: [kaiwong-sapiens/approximate-pi#1](https://github.com/kaiwong-sapiens/approximate-pi/issues/1)):
```text
Use evolve skill to create an issue: approximate pi.
No math module, only basic arithmetic.
```

Backtesting speed:
```text
Use evolve skill to create an issue to speed up the backtesting script.
```

Trading strategy:
```text
Use evolve skill to create an issue to improve the performance
of my trading strategy using the backtest script.  Design the metrics.
```

**Step 2.** Review the issue on GitHub, modify as needed. Then paste the prompt into your CLI:
```text
Evolve the issue.
```

## How it works

1. **Issue** = problem definition (objective, eval command, constraints) + leaderboard
2. **PR** = one attempt (hypothesis, method, metrics, conclusion)
3. **Strategy** = mutate the best, crossover two approaches, or explore something new
4. **Prune** = close Pareto-inferior PRs when the tree grows

Each conclusion feeds into the next round. The eval command can output multiple metrics (e.g., P&L, Sharpe ratio, maximum drawdown) — the agent tracks them in a trait matrix and uses Pareto dominance to decide what to keep, so you don't need to reduce everything to a single score.

After each round, the issue is updated with a search graph and trait matrix, giving future rounds full context on what has been tried and what worked — preventing duplicate experiments and guiding strategy.

Inspired by Google's [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/).

## License

MIT
