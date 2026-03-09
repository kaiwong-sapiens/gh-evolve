# gh-evolve

An AI agent skill for evolutionary problem-solving. Works with Claude Code and Gemini CLI.

`gh-evolve` uses GitHub Issues and Pull Requests as an evolutionary search tree. It creates a shared protocol where one or more AI agents iteratively explore, mutate, and combine solutions to solve optimization problems.

All state lives entirely in GitHub — no external databases or tools required.

```text
GitHub Issue (root node)            <- problem definition + leaderboard
├── PR: attempt-1-baseline          <- score: 0.52
├── PR: attempt-2-mutate-of-1       <- score: 0.58
├── PR: attempt-3-mutate-of-2       <- score: 0.61  (best)
└── PR: attempt-4-crossover-2-3     <- score: 0.55  (pruned)
```

## Install

Paste into your CLI:

```text
Install the evolve skill from github.com/kaiwong-sapiens/gh-evolve
```

Requires: `gh` CLI authenticated with your GitHub account.

## Usage

Create a problem (this sets up a structured GitHub issue):

```text
Use evolve skill to create an issue: <what you want to optimize>
```

Evolve it:

```text
Evolve issue <number> for 3 rounds
```

When satisfied, finalize to merge the winner and clean up:

```text
Finalize evolve issue <number>
```

## Try it

**Step 1.** Pick an example and run it in your CLI:

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

**Step 2.** Review the issue on GitHub, modify as needed. Then run:
```text
Evolve the issue.
```

## How it works

1. **Issue** = The problem definition (objective, eval command, constraints) and a leaderboard. The agent generates a visual search graph and a Trait Matrix here.
2. **PR** = One attempt (hypothesis, method, metrics, conclusion) with a hidden JSON `EVOLVE_STATE` block.
3. **Strategy** = Agents invent operators like `mutate` the best, `crossover` two approaches structurally, or `explore` something completely new.
4. **Prune** = Pareto-inferior PRs are autonomously closed when the tree grows, injecting a `pruned` state so agents don't forget the failure.

Each conclusion feeds into the next round. The eval command can output multiple metrics (e.g., P&L, Sharpe ratio, maximum drawdown) — the agent tracks them in the Trait Matrix and uses Pareto dominance to decide what to keep.

Because the Issue body acts as a shared database, multiple CLI agents running on different machines can simultaneously read the Trait Matrix and submit PRs to the same issue without race conditions.

Inspired by Google's [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/).

## License

MIT