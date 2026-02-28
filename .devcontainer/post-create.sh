#!/bin/bash
set -e

# Install global CLI tools
npm install -g @anthropic-ai/claude-code @fission-ai/openspec

# Link claude-toolbox commands and skills
ln -sfn /home/max/Desktop/coding-projects/claude-toolbox/commands /home/vscode/.claude/commands
ln -sfn /home/max/Desktop/coding-projects/claude-toolbox/skills /home/vscode/.claude/skills

# Install Python dependencies and Playwright
if [ -f pyproject.toml ]; then
    uv sync
    uv run playwright install chromium
fi
