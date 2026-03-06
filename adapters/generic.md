# gh-evolve — Agent Instructions (Generic)

These instructions work with any LLM-based coding agent. Add them to your agent's
system prompt or project instructions file.

---

## Evolution Protocol

You have access to `evolve`, a CLI that manages evolutionary problem-solving over
GitHub PRs. Each problem is tracked as a GitHub issue. Each attempt is a PR.

### Commands

- `evolve status <issue>` — See the problem definition, leaderboard, and suggested strategy
- `evolve start <issue> --strategy <mutate|crossover|explore> --parent <pr>` — Create a branch
- `evolve eval <issue>` — Run the evaluation function defined in the issue
- `evolve submit <issue> --score <n> --strategy <s> --parent <pr> --conclusion "..."` — Open PR, update issue
- `evolve show <pr>` — Read a specific attempt's details and diff
- `evolve prune <issue> --keep-top <n>` — Close low-scoring attempts

### Workflow

1. Run `evolve status <issue>` to understand the problem and what has been tried
2. Study the top attempts with `evolve show <pr>`
3. Pick a strategy based on the trend:
   - Stagnating (no improvement in 3+ attempts) → explore
   - Improving → mutate the best
   - Multiple promising directions → crossover
4. Run `evolve start` to create your branch
5. Make your changes
6. Run `evolve eval <issue>` and note the score
7. Commit and run `evolve submit` with your results
