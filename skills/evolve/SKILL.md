---
name: evolve
description: Evolutionary problem-solving over GitHub PRs. A shared protocol that allows one or multiple agents to iteratively solve hard optimization problems. Only trigger when the user explicitly mentions "evolve skill", "evolve issue", or "use evolve". Do NOT trigger on general optimization, improvement, or scoring requests.
source: https://github.com/kaiwong-sapiens/gh-evolve
---

# Evolutionary Problem-Solving over GitHub PRs

This skill uses GitHub issues and PRs as an evolutionary search graph. An issue defines a problem (objective, eval command, constraints) and tracks a leaderboard. Each PR is one attempt with metrics and a conclusion. You iterate: study what worked, try something better, submit, repeat.

This works because each attempt's conclusion teaches the next one what to try. Metrics provide objective signal. The leaderboard prevents going in circles.

## Principles

This skill has two layers: **protocol** and **guidance**.

**Protocol**: Labels, branch naming, `EVOLVE_STATE` JSON, and issue/PR structure enable multiple agents to read each other's work. Follow these exactly — they are the shared language.

**Guidance**: The goal is to solve the problem, not to follow a script. Everything below is a starting point — the steps, the strategies, the metrics, the evaluation, even the problem framing. Any of them can evolve.

## Arguments

The user provides: `<issue-number> [rounds]`
- Issue number: the GitHub issue tracking the evolution problem (required)
- Rounds: how many attempts to make (default: 1)

## Conventions (The Protocol)

These conventions enable interoperability between agents and across sessions.

### Labels and branches
- Label: `evolve` (on both issues and PRs)
- Branch naming: `evolve/<issue-number>/attempt-<N>-<short-hash>-<short-description>` (Hash prevents branch collisions between concurrent agents).
- Issue title prefix: `[Evolve]`
- PR title prefix: `[Evolve]`

### Issue body structure
The issue MUST contain these sections:
`## Objective`, `## Evaluate` (with a bash code block), `## Constraints`, `## Search Graph` (Mermaid), `## Trait Matrix` (Markdown table), and `## Evolution Log`.

### PR body structure
The PR MUST contain these sections:
`## Parent(s)`, `## Strategy`, `### Hypothesis`, `### Method`, `### Results`, `## Score: <float>`, `### Conclusion`.
And end with the hidden state block:
`<!-- EVOLVE_STATE: {"score": <float>, "strategy": "<strategy>", "parents": [<pr-number>, ...], "metrics": "<short string>", "commit_sha": "<sha>"} -->`

## Execution Guidance

For each round, execute the following phases. You determine the exact CLI commands.

### 1. Assess
Extract the objective, eval command, constraints, current Trait Matrix, and comments from the issue.

### 2. Study (Context-Aware Fetching)
To protect your context window, do not blindly fetch the full bodies of all prior PRs. 
1. Fetch only PR metadata (number, title, state, and the `EVOLVE_STATE` block) to build the Trait Matrix.
2. Identify the most interesting or dominant profiles. 
3. Deep-fetch the diffs/files *only* for the specific PRs you intend to study or mutate.
Read their conclusions to decide your strategy. Cross-pollination of ideas is critical to escaping local maximums.

### 3. Choose a Strategy
Invent your own evolutionary operators based on the situation:
- **`explore`**: Establish a baseline.
- **`mutate`**: Refine a promising trait profile.
- **`crossover`**: Semantically combine two complementary profiles. (Prefer semantic integration reading both parents over raw textual `git merge` to avoid broken conflict markers).
- **`co-evolve`**: Mutate the eval script to raise environment difficulty (combating Goodhart's Law).
- **`revolution`**: Discard the current paradigm and rewrite from scratch to escape a local maximum.

### 4. Branch & Implement
Branch off the appropriate parent commit using the naming convention. Ensure changes are coherent and specifically designed to improve target metrics.

### 5. Evaluate (Isolated & Fast-Fail)
Extract the eval command and run it.
- **Isolation:** Ensure your evaluation does not leave lingering state (modified DBs, config files) that could poison subsequent generations. Clean up after yourself.
- **Self-Correction:** If cheap heuristic tests fail, do not run full evaluations. Read the error, fix the code, re-run. If stuck, submit the PR with `failed` metrics and record the error in the conclusion.

### 6. Submit PR
Push your branch and create a DRAFT PR with the required body structure and `EVOLVE_STATE` block. The `commit_sha` field ensures strict reproducibility. 
The conclusion is the most critical part: write what you learned and what the next attempt should focus on.

### 7. Update the Issue (Graph and Matrix)
Rebuild the state from all PRs and immediately update the main Issue body. 
- **Graph Pruning:** If the Mermaid graph exceeds ~30 nodes, only render the "Active Frontier" (champions, active nodes, and immediate parents) to prevent rendering failures. 
- Use `:::champion` (green) for the best node, `:::pruned` (grey) for nodes with `"pruned": true` in their state. No special characters in node labels.
- Update the Trait Matrix table. 
- **Refine the Problem:** The issue is a living document. If a metric is bad, drop it. If a constraint is too tight, relax it. Log problem definition changes in the `## Evolution Log`.

## Creating a New Problem
Infer the problem, create an eval script if needed, ensure the `evolve` label exists, and create the issue with the structured body. Run the baseline once to verify the eval script works.

## Pruning
Autonomously close and prune redundant or strictly Pareto-inferior PRs to keep the search space manageable. Inject `"pruned": true` into their `EVOLVE_STATE` before closing, delete the remote branch, and remove them from the active Trait Matrix (but keep pruned nodes in the Matrix with a `pruned` status).

## Finalizing
When requested to "Finalize" an issue: identify the winning PR (or the specific PR requested by the user). Remove its draft status to mark it ready for review (or merge if authorized). Close all other open PRs for this issue, delete their branches, and close the main issue with a summary comment.