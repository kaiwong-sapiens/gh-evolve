# gh-evolve

Evolutionary problem-solving over GitHub PRs.

Use any LLM agent (or a human) to iteratively solve optimization problems.
Each attempt is a PR. The best survive, the rest get pruned.
State lives entirely in GitHub issues and PRs — no database, no server.

## How it works

```
GitHub Issue (root node)            ← problem definition + leaderboard
├── PR: attempt-1-baseline          ← score: 0.52
├── PR: attempt-2-mutate-of-1       ← score: 0.58
├── PR: attempt-3-mutate-of-2       ← score: 0.61  (best)
└── PR: attempt-4-crossover-2-3     ← score: 0.55  (pruned)
```

1. **Issue** = problem definition, evaluation command, constraints, leaderboard
2. **PR** = one attempt with hypothesis, method, score, and conclusion
3. **Agent** = reads the leaderboard, picks a strategy (mutate/crossover/explore), submits a new PR
4. **Prune** = close low-scoring PRs, keep the tree manageable

## Install

```bash
# Clone and add to PATH
git clone https://github.com/<you>/gh-evolve.git
export PATH="$PATH:$(pwd)/gh-evolve"

# Requires: gh CLI (https://cli.github.com), Python 3.7+, git
```

## Quick start

```bash
# 1. Create a problem
evolve init \
  --title "Optimize sort function" \
  --objective "Minimize comparisons for lists under 100 elements" \
  --eval "python evaluate.py" \
  --constraint "Pure Python, no external libs"

# 2. See what's been tried
evolve status 1

# 3. Start a new attempt
evolve start 1 --strategy explore

# 4. Make your changes, then evaluate
evolve eval 1

# 5. Submit results
evolve submit 1 --score 0.73 --strategy explore --conclusion "Baseline using insertion sort"

# 6. Prune when the tree grows
evolve prune 1 --keep-top 5
```

## Commands

| Command | Description |
|---------|-------------|
| `evolve init` | Create a new evolution problem (GitHub issue) |
| `evolve status <issue>` | Show problem, leaderboard, and suggested next strategy |
| `evolve start <issue>` | Create a branch for a new attempt |
| `evolve eval <issue>` | Run the evaluation command from the issue |
| `evolve submit <issue>` | Open a PR with results, update issue leaderboard |
| `evolve show <pr>` | View a specific attempt's details and diff |
| `evolve prune <issue>` | Close low-scoring PRs and clean up |

## Using with an LLM agent

gh-evolve is agent-agnostic. Drop the right instructions file into your project:

| Agent | File |
|-------|------|
| Claude Code | Copy from `adapters/claude-code.md` into your `CLAUDE.md` |
| Cursor | Copy from `adapters/generic.md` into `.cursorrules` |
| Aider | Copy from `adapters/generic.md` into your aider config |
| Any other | Copy from `adapters/generic.md` into your agent's instructions |

Then tell your agent: *"Work on evolve issue #42"*

The agent reads the leaderboard, studies past attempts, picks a strategy, and submits a new PR — all through the CLI.

## Example

See [`examples/string-distance/`](examples/string-distance/) for a working example:
evolve a string similarity function to maximize correlation with human judgments.

```bash
cd examples/string-distance
python3 generate_benchmark.py   # create the test data
python3 evaluate.py             # baseline score: ~0.66
```

## Design principles

- **Convention over code** — works even without the CLI, it's just a naming pattern
- **No server, no database** — state lives in GitHub
- **Agent-agnostic** — any LLM or human can participate
- **One scalar score** — the evaluation function returns a single number for ranking
- **Deterministic evaluation** — same code, same score, always

## License

MIT
