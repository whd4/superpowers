---
name: henry-agents
description: Use when routing tasks to HENRY AI agents by callsign — maps /orchestrator, /strategist, /finance, /engineer, /legal, /researcher, /marketing, /sales, /operations to their domain-specific agent files with routing rules and handoff protocol
---

# HENRY Agent Routing Index

## Agent Directory

| Callsign | Domain | Agent File | Use When |
|----------|--------|------------|----------|
| `/orchestrator` | Orchestrator | `agents/henry-orchestrator.md` | Task spans 3+ domains, needs sequencing or parallel dispatch |
| `/strategist` | Strategy | `agents/henry-strategist.md` | Acquisitions, partnerships, market entry, competitive positioning |
| `/finance` | Finance | `agents/henry-finance.md` | Valuations, SBA loans, unit economics, cash flow, financial models |
| `/engineer` | Engineering | `agents/henry-engineer.md` | Code, MCP servers, architecture, deployments, debugging |
| `/legal` | Legal | `agents/henry-legal.md` | LOIs, NDAs, contracts, compliance, risk assessment |
| `/researcher` | Research | `agents/henry-researcher.md` | Due diligence, market intel, competitive analysis, sourcing |
| `/marketing` | Marketing | `agents/henry-marketing.md` | GTM, content, SEO, brand, campaigns, lead gen |
| `/sales` | Sales | `agents/henry-sales.md` | Proposals, pitches, outreach sequences, pipeline, closing |
| `/operations` | Operations | `agents/henry-operations.md` | Sprint planning, execution tracking, workflows, capacity |

## Routing Rules

1. **Single domain** → Route directly to matching agent
2. **Two domains** → Lead agent owns delivery, consults second agent
3. **Three+ domains** → Route through `/orchestrator` for orchestration
4. **Unclear domain** → Default to `/orchestrator` for triage
5. **Codeword received** → Execute immediately per codeword protocol (see henry-ai-os skill), do not route

## Handoff Protocol

When passing work between agents, use this structured artifact:

```
HANDOFF:
  objective: [one sentence]
  completed_work: [list with links/references]
  open_questions: [decisions needed]
  expected_deliverable: [format and content]
  priority: [P0-P3]
```

## Context Rules

- **Orchestrator loads descriptions only** for routing — never loads all 9 full agent files
- Each agent file is self-contained with decision frameworks, output templates, and verification
- Agent files are under 500 lines each for context discipline
