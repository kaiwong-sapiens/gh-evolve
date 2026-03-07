---
name: evolve
description: Iteratively optimize code using evolutionary problem-solving over GitHub PRs. Use this skill whenever the user wants to run evolution rounds on an issue, improve a score through multiple attempts, set up a new optimization problem, or check evolution status. Trigger on phrases like "evolve issue", "do N rounds", "improve the score", "optimize over iterations", "try multiple approaches and keep the best", "run evolution on", or any request to iteratively improve code with scoring and a leaderboard.
---

# Evolutionary Problem-Solving over GitHub PRs

This skill uses GitHub issues and PRs as an evolutionary search tree. An issue defines a problem (objective, eval command, constraints) and tracks a leaderboard. Each PR is one attempt with a score and conclusion. You iterate: study what worked, try something better, submit, repeat.

This works because each attempt's conclusion teaches the next one what to try. Scores provide objective signal. The leaderboard prevents going in circles.

No CLI tool is needed — everything is done with `gh` and `git` directly.

## Arguments

The user provides: `<issue-number> [rounds]`
- Issue number: the GitHub issue tracking the evolution problem (required)
- Rounds: how many attempts to make (default: 1)

If the user asks to set up a new problem, see "Creating a New Problem" at the bottom.

## Conventions

These conventions make everything work together. Follow them exactly.

### Labels and branches
- Label: `evolve` (on both issues and PRs)
- Branch naming: `evolve/<issue-number>/attempt-<N>-<short-description>`
- Issue title prefix: `[Evolve]`
- PR title prefix: `[Evolve]`

### Issue body structure
```
## Objective
<what to optimize>

## Evaluate
```bash
<command that prints SCORE: <number>>
```

## Constraints
<rules for valid attempts>

## Summary Table
<leaderboard — markdown table or "No attempts yet.">

## Evolution Log
- Initialized.
```

### PR body structure
```
## Parent(s): #<pr-number> (or "-" if none)
## Strategy: explore | mutate | crossover

### Hypothesis
<what you expected>

### Method
<what you changed>

### Results
<raw output or per-component scores>

## Score: <float>

### Conclusion
<what you learned — this is the most important field>
```

### Parsing rules
- **Score**: `## Score: <float>` line in PR body
- **Strategy**: `## Strategy: <text>` line in PR body
- **Parents**: `## Parent(s): #N, #M` line in PR body
- **Eval command**: fenced code block under `## Evaluate` in issue body
- **Key insight**: first line of `### Conclusion` section (truncated to 80 chars for leaderboard)

## Protocol

For each round:

### 1. Assess

Read the issue to understand the problem:

```bash
gh issue view <issue> --json title,body,state
```

From the body, extract:
- The objective (under `## Objective`)
- The eval command (code block under `## Evaluate`)
- The constraints (under `## Constraints`)
- The current leaderboard (under `## Summary Table`)

### 2. Study prior attempts

List all PRs for this issue:

```bash
gh pr list --label evolve --state all --json number,title,state,headRefName,body --limit 100
```

Filter to PRs whose `headRefName` starts with `evolve/<issue>/`. Parse the score from each PR body. Sort by score descending — that's the leaderboard.

For the top 2-3 scoring PRs, read their conclusions and diffs:
```bash
gh pr view <pr-number> --json title,body,state,headRefName
gh pr diff <pr-number>
```

The conclusions tell you what directions are promising and which are dead ends. Without studying them, you'll repeat failed experiments.

### 3. Choose a strategy

- **No attempts yet** → `explore`. Start with a solid, well-known approach. Don't overthink; establish a baseline.
- **Score improving** → `mutate`. Refine the best attempt. Small, targeted changes addressing known weaknesses.
- **Stagnating (3+ attempts, no improvement)** → `explore`. Try something fundamentally different — a different algorithm, representation, or decomposition.
- **Two good approaches with complementary strengths** → `crossover`. Combine the best ideas from each.

### 4. Create a branch

Determine the next attempt number by finding the highest existing attempt number and adding 1.

```bash
git checkout main && git pull --ff-only
git checkout -b evolve/<issue>/attempt-<N>-<short-description>
```

### 5. Implement

- Read the code you're modifying first
- One idea per attempt — don't bundle unrelated changes
- Think about why prior approaches scored the way they did
- Keep changes minimal and focused

### 6. Evaluate

Extract the eval command from the issue body and run it:

```bash
<eval-command>
```

Note the `SCORE:` line in the output. If there are per-component scores, note those too.

### 7. Commit and submit

```bash
git add <changed-files>
git commit -m "<descriptive message>"
git push -u origin <branch-name>
```

Create the PR with the structured body:

```bash
gh pr create \
  --title "[Evolve] <short title>" \
  --label evolve \
  --body "$(cat <<'EOF'
## Parent(s): #<parent-pr> (or -)
## Strategy: <explore|mutate|crossover>

### Hypothesis
<what you expected>

### Method
<what you changed>

### Results
<per-component scores if available>

## Score: <score>

### Conclusion
<what you learned, what to try next>
EOF
)"
```

Write a good conclusion. It should include:
- What you tried and why
- What improved and what regressed vs the parent
- Per-component scores if available
- What the next attempt should focus on

### 8. Update the issue leaderboard

After creating the PR, rebuild the leaderboard from all PRs and update the issue's Summary Table section. Fetch all evolve-labeled PRs, parse their scores, sort descending, and format as a markdown table:

```
| Rank | PR | Score | Strategy | Parent(s) | Status | Key Insight |
|------|-----|-------|----------|-----------|--------|-------------|
| 1 | #4 | 0.588 | mutate | #3 | open | Hybrid recency+freq+IRR |
| 2 | #3 | 0.581 | explore | - | open | LRU-LFU combo works |
```

Update the issue body by replacing the content under `## Summary Table` with the new table:

```bash
gh issue edit <issue> --body "<updated body>"
```

### 9. Reflect (multi-round)

Before the next round, review the leaderboard. Did your score improve? Which components are weakest? Are you hitting diminishing returns? Use this to pick the next strategy.

## Creating a New Problem

When the user wants to set up a new evolution problem:

1. Ensure the `evolve` label exists:
   ```bash
   gh label create evolve --description "Evolution problem" --color 7057ff
   ```

2. Create the issue with the structured body:
   ```bash
   gh issue create \
     --title "[Evolve] <problem title>" \
     --label evolve \
     --body "<issue body following the template above>"
   ```

The user needs to provide: a title, an objective, an evaluation command that prints `SCORE: <number>`, and any constraints.

## Pruning

When the leaderboard grows large, close low-scoring PRs to keep things manageable. Close PRs below rank N with a comment explaining why, delete their remote branches, and update the issue leaderboard to show only the kept entries.

Always confirm with the user before pruning.
