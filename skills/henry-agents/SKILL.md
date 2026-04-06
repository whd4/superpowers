---
name: henry-agents
description: Use when routing tasks to HENRY AI agents by callsign — maps /nexus, /atlas, /ledger, /forge, /shield, /oracle, /pulse, /closer, /engine to their domain-specific agent files with routing rules and handoff protocol
---

# HENRY Agent Routing Index

## Agent Directory

| Callsign | Domain | Agent File | Use When |
|----------|--------|------------|----------|
| `/nexus` | Orchestrator | `agents/henry-nexus.md` | Task spans 3+ domains, needs sequencing or parallel dispatch |
| `/atlas` | Strategy | `agents/henry-atlas.md` | Acquisitions, partnerships, market entry, competitive positioning |
| `/ledger` | Finance | `agents/henry-ledger.md` | Valuations, SBA loans, unit economics, cash flow, financial models |
| `/forge` | Engineering | `agents/henry-forge.md` | Code, MCP servers, architecture, deployments, debugging |
| `/shield` | Legal | `agents/henry-shield.md` | LOIs, NDAs, contracts, compliance, risk assessment |
| `/oracle` | Research | `agents/henry-oracle.md` | Due diligence, market intel, competitive analysis, sourcing |
| `/pulse` | Marketing | `agents/henry-pulse.md` | GTM, content, SEO, brand, campaigns, lead gen |
| `/closer` | Sales | `agents/henry-closer.md` | Proposals, pitches, outreach sequences, pipeline, closing |
| `/engine` | Operations | `agents/henry-engine.md` | Sprint planning, execution tracking, workflows, capacity |

## Routing Rules

1. **Single domain** → Route directly to matching agent
2. **Two domains** → Lead agent owns delivery, consults second agent
3. **Three+ domains** → Route through `/nexus` for orchestration
4. **Unclear domain** → Default to `/nexus` for triage
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

- **Nexus loads descriptions only** for routing — never loads all 9 full agent files
- Each agent file is self-contained with decision frameworks, output templates, and verification
- Agent files are under 500 lines each for context discipline
