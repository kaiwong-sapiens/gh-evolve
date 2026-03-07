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
<command that prints metrics and/or a primary score>
```

## Constraints
<rules for valid attempts>

## Trait Matrix
<markdown table of attempts and their metric profiles>

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
- **Score & State**: Read the hidden JSON block at the bottom of the PR body `<!-- EVOLVE_STATE: {...} -->` for deterministic parsing. 
- **Eval command**: fenced code block under `## Evaluate` in issue body
- **Key insight**: first line of `### Conclusion` section (truncated to 80 chars for the Trait Matrix)

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
- The current profile of attempts (under `## Trait Matrix`)

### 2. Study prior attempts

List all PRs for this issue:

```bash
gh pr list --label evolve --state all --json number,title,state,headRefName,body --limit 100
```

Filter to PRs whose `headRefName` starts with `evolve/<issue>/`. Parse the score and metrics from each PR body.

Instead of a strict 1-to-N leaderboard, view these attempts as a **Phenotype Matrix**. You are looking for **patterns in the metrics** (e.g., "The Fast/Inaccurate Profile" vs "The Slow/Precise Profile").

Identify the 2-3 most interesting or dominant profiles. Read their conclusions to decide your strategy. ONLY pull the `diff` for the specific parent PR(s) you decide to mutate or crossover to avoid context bloat:
```bash
gh pr view <pr-number> --json title,body,state,headRefName
# Only if mutating/crossing over this specific PR:
gh pr diff <pr-number>
```

The conclusions tell you what directions are promising and which are dead ends. Without studying them, you'll repeat failed experiments.

### 3. Choose a strategy

Do not blindly look for the "highest score". **Analyze the trade-offs across all metrics to understand the whole pattern.** If one PR discovered a novel structural pattern that massively improved memory but slightly hurt accuracy, that is a highly valuable trait profile to build upon.

- **No attempts yet** → `explore`. Start with a solid, well-known approach. Establish a baseline profile.
- **Clear, promising trait profile** → `mutate`. Refine an attempt that has a strong pattern of metrics. Address its specific weaknesses. This can range from targeted parameter tuning to substantial structural refactoring—do whatever is semantically required to break through the current metric bottleneck without destroying its core strengths.
- **Stagnating (3+ attempts, no meaningful changes in metrics)** → `explore`. Try something fundamentally different — a different algorithm, representation, or decomposition to discover a new trait profile.
- **Two complementary trait profiles** → `crossover`. For example, if PR A is structurally fast but sloppy, and PR B is slow but precise, explicitly combine the best ideas from each to try and merge the patterns.

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
- Ensure your changes are coherent and specifically designed to improve the target metrics. Do not arbitrarily limit the scale of your changes if a major refactor is required.

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

### 8. Update the issue Trait Matrix

After creating the PR, rebuild the matrix from all PRs and update the issue's Trait Matrix section. Fetch all evolve-labeled PRs, parse their metrics, and format as a markdown table. Order them logically (e.g., grouping similar trait profiles together, or roughly by overall utility).

```
| PR | Score | Metrics | Strategy | Parent(s) | Status | Key Insight |
|-----|-------|---------|----------|-----------|--------|-------------|
| #4 | 0.588 | `time:1.2s` | mutate | #3 | open | Hybrid recency+freq+IRR |
| #3 | 0.581 | `time:1.5s` | explore | - | open | LRU-LFU combo works |
```

Update the issue body by replacing the content under `## Trait Matrix` with the new table:

```bash
gh issue edit <issue> --body "<updated body>"
```

### 9. Reflect (multi-round)

Before the next round, review the Trait Matrix. Have you discovered a new pattern? Which specific metric is acting as a bottleneck for your current best profile? Are you hitting diminishing returns on a specific trait? Use this to pick the next strategy.

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

When the matrix grows large, close redundant or strictly inferior PRs to keep things manageable. Prune an attempt if another attempt is **strictly better across ALL metrics** (Pareto inferior). Keep attempts that offer a unique, valuable trade-off profile. Close pruned PRs with a comment explaining why, delete their remote branches, and update the issue's Trait Matrix to show only the kept entries.

Always confirm with the user before pruning.
