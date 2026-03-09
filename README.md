# gh-evolve

An AI agent skill for evolutionary problem-solving over GitHub PRs. Works with Claude Code and Gemini CLI.

`gh-evolve` transforms a standard GitHub Issue into an autonomous optimization environment. Instead of relying on brute force or a single long-context prompt to solve hard problems, this skill creates a shared protocol where one or more AI agents iteratively explore, mutate, and combine solutions as an evolutionary search tree. 

All state lives entirely in GitHub — no external databases, CLI binaries, or web servers required.

```
GitHub Issue (root node)            <- problem definition + leaderboard
├── PR: attempt-1-baseline          <- score: 0.52
├── PR: attempt-2-mutate-of-1       <- score: 0.58
├── PR: attempt-3-mutate-of-2       <- score: 0.61  (best)
└── PR: attempt-4-crossover-2-3     <- score: 0.55  (pruned)
```

## Features
- **Stateless & Concurrent:** Because the Issue body *is* the database, multiple CLI agents running on different machines can simultaneously read the Trait Matrix, invent new evolutionary operators, and submit PRs to the same issue without race conditions.
- **Scientific Methodology:** Every PR is an attempt containing a clear hypothesis, execution method, resulting metrics, and a conclusion. This builds an explicit Trait Matrix preventing agents from repeating failed experiments.
- **Pareto Pruning:** Tracks multi-dimensional metrics (e.g., P&L, Speed, Token Usage) rather than reducing everything to a single score. Autonomously prunes strictly inferior branches.

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

1. **Issue** = problem definition (objective, eval command, constraints) + leaderboard. The agent generates a Mermaid.js lineage graph and Markdown table on the issue.
2. **PR** = one attempt (hypothesis, method, metrics, conclusion) with a hidden JSON `EVOLVE_STATE` block.
3. **Strategy** = agents invent operators like `mutate` the best, `crossover` two approaches structurally, or `explore` something completely new to escape local maximums.
4. **Prune** = close Pareto-inferior PRs when the tree grows, injecting a `pruned` state so agents don't forget the failure.

Each conclusion feeds into the next round. The eval command can output multiple metrics (e.g., P&L, Sharpe ratio, maximum drawdown) — the agent tracks them in a Trait Matrix and uses Pareto dominance to decide what to keep.

After each round, the issue is updated with the search graph and Trait Matrix, giving future rounds full context on what has been tried and what worked — preventing duplicate experiments and guiding strategy.

Inspired by Google's [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/).

## License

MIT