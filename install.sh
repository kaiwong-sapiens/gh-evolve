#!/bin/sh
mkdir -p ~/.claude/skills/evolve
curl -sL https://raw.githubusercontent.com/kaiwong-sapiens/gh-evolve/main/skills/evolve/SKILL.md \
  -o ~/.claude/skills/evolve/SKILL.md
echo "Installed. Restart Claude Code to use: evolve issue <number> [rounds]"
