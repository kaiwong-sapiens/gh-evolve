---
name: evolve
description: Evolutionary problem-solving over GitHub PRs. Only trigger when the user explicitly mentions "evolve skill", "evolve issue", or "use evolve". Do NOT trigger on general optimization, improvement, or scoring requests.
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

<!-- EVOLVE_STATE: {"score": <float>, "strategy": "<strategy>", "parents": [<pr-number>, ...], "metrics": "<short string of secondary metrics>"} -->
```

### Parsing rules
- **Score & State**: Read the hidden JSON block at the bottom of the PR body `<!-- EVOLVE_STATE: {...} -->` for deterministic parsing. Use this JSON for sorting and logic.
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

For the top 2-3 scoring PRs, read their conclusions to decide your strategy. ONLY pull the `diff` for the specific parent PR(s) you decide to mutate or crossover to avoid context bloat:
```bash
gh pr view <pr-number> --json title,body,state,headRefName
# Only if mutating/crossing over this specific PR:
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

CRITICAL: If your strategy is `mutate` or `crossover`, you MUST start from the parent PR's branch or apply its changes to main.

```bash
# If strategy is 'explore' (starting fresh):
git checkout main && git pull --ff-only
git checkout -b evolve/<issue>/attempt-<N>-<short-description>

# If strategy is 'mutate' (building on a parent PR):
git fetch origin <parent-head-ref>
git checkout -b evolve/<issue>/attempt-<N>-<short-description> FETCH_HEAD
```

### 5. Implement

- Read the code you're modifying first
- One idea per attempt — don't bundle unrelated changes
- Think about why prior approaches scored the way they did
- Keep changes minimal and focused

### 6. Evaluate

Extract the eval command from the issue body and run it. 

**Security Warning:** If this repository involves running untrusted code or dependencies, it is strongly recommended to run the eval command inside an isolated environment (e.g., Docker container) to prevent the evolutionary algorithm from executing destructive code on your host OS.

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

Create the PR with the structured body as a DRAFT to avoid cluttering reviewers and CI/CD pipelines:

```bash
gh pr create \
  --draft \
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

<!-- EVOLVE_STATE: {"score": <score>, "strategy": "<strategy>", "parents": [<parent-pr>], "metrics": "<secondary metrics if any>"} -->
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
| Rank | PR | Score | Metrics | Strategy | Parent(s) | Status | Key Insight |
|------|-----|-------|---------|----------|-----------|--------|-------------|
| 1 | #4 | 0.588 | `time:1.2s` | mutate | #3 | open | Hybrid recency+freq+IRR |
| 2 | #3 | 0.581 | `time:1.5s` | explore | - | open | LRU-LFU combo works |
```

Update the issue body by replacing the content under `## Summary Table` with the new table:

```bash
gh issue edit <issue> --body "<updated body>"
```

### 9. Reflect (multi-round)

Before the next round, review the leaderboard. Did your score improve? Which components are weakest? Are you hitting diminishing returns? Use this to pick the next strategy.

## Creating a New Problem

When the user wants to set up a new evolution problem, keep it fast — the goal is to get the issue on GitHub quickly so the user can see it and start evolving.

1. **Infer what you can from the codebase.** Read the existing code to understand what to optimize, what the eval script does, and what files should be constrained. The user's prompt can be minimal — fill in the gaps yourself.

2. **If an eval script doesn't exist, create one.** It must print `SCORE: <number>`. Keep it simple and correct. Run it once to verify it works and note the baseline score.

3. **Ensure the `evolve` label exists:**
   ```bash
   gh label create evolve --description "Evolution problem" --color 7057ff 2>/dev/null || true
   ```

4. **Commit and push any new files** (eval script, baseline code, etc.) so the repo is up to date before evolution starts.

5. **Create the issue with the structured body:**
   ```bash
   gh issue create \
     --title "[Evolve] <problem title>" \
     --label evolve \
     --body "<issue body following the template above>"
   ```

6. **Print the issue URL** so the user can review it on GitHub before evolving.

Don't overthink the setup. A trivial baseline is fine — the evolution rounds will improve it.

## Pruning

When the leaderboard grows large, close low-scoring PRs to keep things manageable. Close PRs below rank N with a comment explaining why, delete their remote branches, and update the issue leaderboard to show only the kept entries.

Always confirm with the user before pruning.

## Finalizing (Champion Merge)

When the user requests to wrap up or "Finalize" an evolution problem (e.g., `Finalize evolve issue <N>`), your goal is to merge the winning strategy and clean up the environment:

1. **Identify the Winner:** Read the issue leaderboard and identify the `#1` rank PR.
2. **Promote:** Remove the draft status from the winning PR and request a human review (or merge it directly if the user explicitly authorized it).
3. **Clean Up Runners-up:** Close all other open PRs for this issue.
4. **Delete Branches:** Delete the remote branches for the runner-up PRs.
5. **Close Issue:** Close the main GitHub Issue with a summary comment highlighting the final baseline vs. final score and the key insights learned.
