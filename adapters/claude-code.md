# gh-evolve — Agent Instructions (Claude Code)

Add this to your project's CLAUDE.md to enable evolution-driven problem solving.

---

## Evolution Protocol

When asked to work on an evolution issue (e.g. "work on evolve issue #42"):

1. Run `evolve status <issue>` to see the problem, constraints, and all prior attempts
2. Read the top 3 attempts' PRs to understand what worked (`evolve show <pr>`)
3. Decide on a strategy:
   - If the best score hasn't improved in 3+ attempts: **explore** (try something novel)
   - If a recent attempt showed improvement: **mutate** (refine it)
   - If two different approaches each help: **crossover** (combine them)
4. Run `evolve start <issue> --strategy <strategy> --parent <pr>` to create your branch
5. Implement your idea — keep changes focused and minimal
6. Run `evolve eval <issue>` to evaluate
7. Commit your changes
8. Run `evolve submit <issue> --score <score> --strategy <strategy> --parent <pr> --conclusion "what you learned"`
9. If your score is the new best, explain why in the conclusion
