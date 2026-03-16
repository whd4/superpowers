---
name: acquisition-pipeline
when_to_use: |
  Use when evaluating, pursuing, or managing CPA firm acquisitions.
  Triggers: new target identified, LOI needed, due diligence required, transformation planning.
---

# Acquisition Pipeline

Structured workflow for HENRY AI's CPA firm acquisition process.

## Pipeline Stages

### Stage 1: Target Identification
- [ ] Source target from broker listing or direct outreach
- [ ] Verify: CPA firm, distressed or owner-retiring
- [ ] Confirm asking price ≤ 0.4x annual revenue
- [ ] Log target ID (format: TXS####) in HENRY_CONTEXT.md

### Stage 2: Initial Evaluation (Agent: Atlas)
- [ ] Pull financials: revenue, expenses, EBITDA, client count
- [ ] Assess client concentration (no single client > 20% revenue)
- [ ] Evaluate staff: who stays, who goes, automation potential
- [ ] Score opportunity (0-20 confidence)
- [ ] Decision: pursue / modify terms / pass

### Stage 3: Financial Modeling (Agent: Ledger)
- [ ] Model purchase at target multiple
- [ ] Structure SBA 7(a) financing (10% down, 10yr term)
- [ ] Project 90-day AI transformation costs
- [ ] Model post-transformation EBITDA (target: 60-70%)
- [ ] Calculate exit valuation at 7x EBITDA
- [ ] Compute IRR and cash-on-cash return

### Stage 4: LOI & Legal (Agent: Shield)
- [ ] Draft Letter of Intent with standard HENRY terms
- [ ] Include: price, terms, contingencies, timeline
- [ ] NDA if not already signed
- [ ] Flag items for attorney review

### Stage 5: Due Diligence (Agent: Oracle)
- [ ] Deep financial audit
- [ ] Client interviews / satisfaction assessment
- [ ] Technology stack audit
- [ ] Regulatory compliance check
- [ ] Staff interviews and retention planning

### Stage 6: Close & Transform (Agents: Forge + Engine)
- [ ] Execute purchase agreement
- [ ] Day 1 integration checklist
- [ ] Deploy AI automation stack (30/60/90 day plan)
- [ ] Staff training on new systems
- [ ] Client communication plan
- [ ] Track EBITDA improvement weekly

## Decision Gates
Each stage requires explicit GO/NO-GO before proceeding.
Log all decisions in HENRY_CONTEXT.md Decision Log.
