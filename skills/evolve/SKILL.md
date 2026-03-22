---
name: evolve
description: Evolutionary problem-solving over GitHub PRs. A shared protocol that allows one or multiple agents to iteratively solve hard optimization problems. Only trigger when the user explicitly mentions "evolve skill", "evolve issue", or "use evolve". Do NOT trigger on general optimization, improvement, or scoring requests.
source: https://github.com/kaiwong-sapiens/gh-evolve
---

# Evolutionary Problem-Solving over GitHub PRs

This skill uses GitHub issues and PRs as an evolutionary search graph. An issue defines a problem (objective, eval command, constraints) and tracks a leaderboard. Each PR is one attempt with metrics and a conclusion. You iterate: study what worked, try something better, submit, repeat.

This works because each attempt's conclusion teaches the next one what to try. Metrics provide objective signal. The leaderboard prevents going in circles. Inspired by concepts from AlphaEvolve, this protocol frames software development as a genetic search: iteratively mutating, evaluating, and recombining code across the graph to discover optimal solutions. The search graph thrives on shared context; therefore, every trial—whether successful or a failed experiment—is documented as a PR to grow the collective intelligence.

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
`## Objective`, `## Evaluate`, `## Constraints`, `## Findings`, `## Search Graph` (Mermaid), `## Trait Matrix` (Markdown table), and `## Evolution Log`.

### PR body structure
The PR MUST contain these sections:
`## Parent(s)`, `## Strategy`, `### Hypothesis`, `### Method`, `### Results`, `### Conclusion`.
And end with the hidden state block:
`<!-- EVOLVE_STATE: {"strategy": "<strategy>", "parents": [<pr-number>, ...], "metrics": <metrics>, "commit_sha": "<sha>"} -->`

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
- **`co-evolve`**: Mutate the evaluation criteria to raise environment difficulty (combating Goodhart's Law).
- **`revolution`**: Discard the current paradigm and rewrite from scratch to escape a local maximum.

### 4. Branch, PR & Implement
Branch off the appropriate parent commit using the naming convention. Create the DRAFT PR immediately with your hypothesis and add yourself to the issue's Trait Matrix with status `in progress`. This signals to other agents and humans what is being worked on. Implement your changes, then update the PR with results when done.

### 5. Evaluate (Isolated & Fast-Fail)
Extract the eval command and run it.
- **Isolation:** Ensure your evaluation does not leave lingering state (modified DBs, config files) that could poison subsequent generations. Clean up after yourself.
- **Self-Correction:** If cheap heuristic tests fail, do not run full evaluations. Read the error, fix the code, re-run. If stuck, submit the PR with `failed` metrics and record the error in the conclusion.

### 6. Complete PR
Update the PR with results, conclusion, and `EVOLVE_STATE` block. Ensure every completed trial is submitted, as failed local experiments provide valuable data to steer future agents away from dead ends. The conclusion is the most critical part: write what you learned and what the next attempt should focus on.

### 7. Update the Issue (Graph and Matrix)
Rebuild the state from all PRs and immediately update the main Issue body. To avoid overwriting concurrent updates from other agents: re-read the issue body right before writing, and after writing, re-read to verify your changes are present. If another agent overwrote your update, re-read the current body, merge your changes into it, and write again.
- **Graph Pruning:** If the Mermaid graph gets too large to render cleanly, only render the "Active Frontier" (champions, active nodes, and immediate parents). Visually distinguish champion and pruned nodes.
- Update the Trait Matrix table.
- **Update Findings:** Synthesize what has been learned so far — what works, what doesn't, and why. This is the executive summary a human reads to understand the current state without reviewing individual PRs.
- **Refine the Problem:** The issue is a living document. If a metric is bad, drop it. If a constraint is too tight, relax it. Log problem definition changes in the `## Evolution Log`.

## Creating a New Problem
Infer the problem and discover the evaluation mechanism from the codebase. If a new custom evaluation script is required, **do not commit it to the main branch**. Instead, create a `baseline` branch (e.g. `evolve/<issue-number>/attempt-0-baseline`), commit the evaluation script there, and open an initial baseline PR. This keeps the main branch clean and allows the evaluation mechanism to co-evolve alongside the solution within the branch graph.

Ensure the `evolve` label exists on the repository, run the baseline once to verify the evaluation works, and then create the main issue and baseline PR with the structured body.

## Pruning
Autonomously close and prune redundant or strictly Pareto-inferior PRs to keep the search space manageable. Mark pruned PRs in their `EVOLVE_STATE` and clean up their branches.

## Finalizing
When requested to "Finalize" an issue: identify the winning PR (or the specific PR requested by the user). Remove its draft status to mark it ready for review (or merge if authorized). Close all other open PRs for this issue, delete their branches, and close the main issue with a summary comment.