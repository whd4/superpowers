# HENRY AI — Operational State

> Last updated: 2026-06-04
> Session: Infrastructure consolidation + security cleanup
> **Latest handoff: `SESSION-HANDOFF-2026-06-04.md` — read it first.**

## Current Focus
Infra cleanup is **done and green**. Open: (1) Whitt revokes 2 GitHub PATs, (2) pick ONE home surface (VS Code vs Claude Desktop) to end the 4-agent collision + resolve the graph owner, (3) start **Dwyer Interiors case study #0**.

## Boot Sequence
1. Read the most-recent `SESSION-HANDOFF-*.md` (currently 2026-06-04).
2. Run anti-drift check; verify live systems via `wsl.exe` (Hermes PID 190025, trading PID 197).
3. Orient Whitt per the handoff's "NEXT SESSION STARTS WITH".

## Active Projects

### Track 1 — Agency (Cash Flow)
- **Status:** Building
- **Pipeline:** Targeting Houston businesses for AI transformation
- **Pricing:** $5K-$25K/project + $500-$2K/month retainers
- **Margin target:** 85%+

### Track 2 — Acquisitions (Wealth)
- **Status:** Active pipeline
- **Model:** Buy distressed CPA firms at 0.4x rev → 90-day AI transform → 60-70% EBITDA → exit 7x
- **Active targets:**
  - TXS5345 (PRIORITY)
  - TXS5450
  - TXS5513
  - TXS5491

### Star Voss Legal Case
- **Status:** Active litigation
- **Units:** F210, F212, F310

### Fiverr AI Services
- **Status:** Active
- **Focus:** AI automation gigs

### OpenClaw + BMAD V6
- **Status:** In development

## Infrastructure State

### MCP Servers (Configured)
- Command Center — Task/project tracking
- BMAD Framework — 5 specialized agents
- GitHub — Full repo management (`whd4` org)
- Filesystem — Local read/write
- Google Calendar — Scheduling
- Gmail — Email management
- Hugging Face — ML models
- Figma — Design-to-code
- Mermaid Chart — Diagrams
- PDF Tools — Document analysis
- Windows-MCP — Desktop automation
- Claude in Chrome — Browser automation
- AEGIS — Memory, research, verification

### Security (AEGIS SHIELD)
- 5-layer security: Deep scanner, honeypot/canary, Docker kill box, MITRE ATT&CK forensics, malware sandbox
- Ralph security loop plugin active

## Open Tasks
- [ ] **Whitt:** revoke 2 GitHub PATs (`ghp_D3VS…`, `ghp_5yAH…`) at github.com/settings/tokens — only externally-exposed creds
- [ ] **Whitt:** pick home surface — VS Code or Claude Desktop (resolves graph owner + 4-agent collision)
- [ ] Collapse to ONE driver (close Codex, retire/demote extra Claudes)
- [ ] Set OneDrive "Always keep on this device" for dev folders + Claude install (stops 253MB hydration downloads)
- [ ] **Start Dwyer Interiors case study #0** (YC Screen → PAI → agents → G-Stack)
- [ ] Private remote backup of scrubbed vault
- [ ] Check GitHub billing (flagged red)

## Decision Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-16 | Set up HENRY OS in superpowers repo | Leverage existing skills framework for agent orchestration |
| 2026-06-04 | Vault history scrubbed of all secrets, quarantined originals offline | Capture pipeline leaked 9 .env dupes into git; .gitignore gap fixed |
| 2026-06-04 | Rotation list = 2 GitHub PATs only (NOT the stale "4 keys") | Anthropic dead (OAuth), FAL live-but-local; only PATs externally exposed |
| 2026-06-04 | One driver owns shared state (vault/handoff/Hermes) | Multiple concurrent agents caused drift, lock fights, duplicate notes |
| 2026-06-04 | Graph lives wherever the orchestrator lives | Kuzu single-writer; resolves once Whitt picks home surface |

## Notes
- Update this file at the end of every session
- This is the single source of truth for operational state
