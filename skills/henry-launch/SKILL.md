---
name: henry-launch
description: Use when launching a new HENRY AI project — scaffolds complete project structures for agency AI, CPA acquisitions, or MCP servers with Docker deployment, GitHub Actions CI/CD, JWT auth, and health checks in 2 steps
---

# Launch a New Project

## Overview

2-step project launch:
1. Pick a project type
2. Run the scaffolder

## Project Types

| Type | Flag | What You Get |
|------|------|-------------|
| **Agency AI** | `--type agency` | FastAPI + React + JWT auth + Docker + GitHub Actions |
| **CPA Acquisition** | `--type acquisition` | DD templates + financial models + legal docs + 90-day plan |
| **MCP Server** | `--type mcp-server` | Python MCP server + typed tools + Docker + tests |

## Step 1: Scaffold

```bash
python ${CLAUDE_SKILL_DIR}/scaffolder.py --type <type> --name <project-name>
```

This creates the full project directory with all files, configs, and templates.

## Step 2: Deploy (Agency & MCP only)

```bash
python ${CLAUDE_SKILL_DIR}/deployer.py --path <project-dir>
```

This validates, builds Docker, runs health checks, and reports status.

## For Agency Projects — Auth Setup

After scaffolding, generate secrets:
```bash
python ${CLAUDE_SKILL_DIR}/auth_setup.py --path <project-dir>
```

## Verification

After launch, verify:
- [ ] All files created (check scaffolder output)
- [ ] Docker builds clean: `docker build .`
- [ ] Health check responds: `curl localhost:8000/health`
- [ ] No secrets in tracked files: `git diff --cached | grep -i secret`
- [ ] Tests pass: `pytest` or `npm test`
- [ ] CLAUDE.md present with project-specific instructions

## Dry Run

Preview without creating files:
```bash
python ${CLAUDE_SKILL_DIR}/scaffolder.py --type agency --name test --dry-run
```
