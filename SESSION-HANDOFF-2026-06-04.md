# SESSION HANDOFF — 2026-06-04 (≈18:00 CT)

> **For:** the next local session (the orchestrator booting from `C:\Users\whitt\CLAUDE.md`)
> **From:** the superpowers-repo orchestrator session (Claude Desktop, branch `claude/setup-henry-ai-os-f6svQ`)
> **Read this first, then run the anti-drift check, then orient Whitt.**

---

## ⚡ ONE-LINE STATE
Day-long infrastructure cleanup is **done and green**. The open problem is **too many AI agents running at once** on one machine. Next job: collapse to **one driver**, then finally start **Dwyer Interiors case study #0**.

---

## 🟢 LIVE SYSTEMS (verify before trusting — use `wsl.exe bash -c "..."`, NOT Git Bash)
| System | Last known | Check |
|--------|-----------|-------|
| Hermes gateway | **PID 190025** (was 297; restarted by v0.15.1 upgrade), port 8643 | `wsl.exe bash -c "pgrep -f 'gateway run'"` |
| Trading bot | **PID 197**, dashboard :8888 | `wsl.exe bash -c "pgrep -f run_with_dashboard"` |
| mission-control | bun, :4250 (operator cockpit) | browser / `pgrep -f` |
| HENRY Sweeper | parent+worker `pythonw` pair (detached) | **NEVER kill by name — exact PID only** |
| Kuzu graph | held by **Claude Desktop, PID 55200** (single-writer lock) | see Graph Decision below |

Memory pipeline is WORKING — CAPTURE PULSE dashboard showed: Sweeper events 42, Notepad rescues 89, Graph entities 390, ~704 notes.

---

## ✅ DONE & VERIFIED THIS SESSION
- **Vault secret scrub** — `C:\Users\whitt\knowledge` git history scrubbed byte-level. 9 duplicate `.env` files (all identical Hermes env) + 3 secret notes purged from all history. 25 token strings replaced with `***REMOVED***`. Re-verified: **0 of Whitt's secrets remain** (only benign third-party Obsidian plugin keys left). Originals preserved offline at `~/.henry-archive\quarantine\2026-06-04-vault-snapshot\`.
- **Root cause of leak:** old `.gitignore` only matched `wiki/projects/*/.env` but the capture pipeline dropped them under `todos/wiki/projects/*/.env`. **Fixed** with broad patterns (`.env`, `*.env`, `*GOCSPX*`, `*ghp_*`, `*.pem`, `secrets*`).
- **Audit tools** filed to `~/.henry-archive\audit-tools\` (redact-inventory.ps1, secret-scan.py, scrub_residual.py). Secret-map files deleted.
- **Hermes** upgraded to **v0.15.1** (API_SERVER_KEY breaking change handled, 2 outsourc-e plugins installed, Workspace .env wired). swarm1 reset to default. UI confirmed = hermes dashboard on :9128.
- **GitHub CI** — 5 noisy/failing workflows disabled.
- **OpenClaw** removed (458 MB freed), data preserved.
- **Hermes memory file** `reference_hermes_stack.md` written + indexed.
- **VS Code excludes** set (node_modules, OBSIDIAN, .git) — reload VS Code to feel it.
- **InfraNodus + graphrag MCP** registered to user config (but can't connect — see Graph Decision).

---

## 🔴 OPEN ITEMS

### 1. WHITT'S 30-SECOND JOB — revoke 2 GitHub PATs (only thing a human must do)
These were leaked into a web-session transcript by a bad `grep -oE` (my error). They are the **only externally-exposed** credentials; everything else stayed local.
- Go to **github.com/settings/tokens** (account **whd4**)
- Delete the two tokens: prefix **`ghp_D3VS…`** and **`ghp_5yAH…`** (both 40 chars)
- **Rotation reconciled:** Anthropic keys are DEAD (Whitt uses OAuth, deleted them all). FAL key is live-but-local — defer, never exposed. So the real revoke list is **just these 2 PATs**, NOT the stale "4 keys" from the 06-03 note.

### 2. THE GRAPH OWNER DECISION (parked by Whitt — do NOT force)
Kuzu is **single-writer**. Claude Desktop (PID 55200) holds the graph, so VS Code's registered servers can't open it. Three paths:
- **A — keep in Desktop:** remove the 2 registrations from VS Code Claude Code (stops connect-noise). Right if Desktop stays the orchestrator.
- **B — move to VS Code:** close Desktop / kill PIDs 60168+58444; VS Code takes the locks. Right if VS Code becomes the single home.
- **C — share read-only:** code change in store.py/server.py (`read_only=True`). ⚠️ **MUST verify the 4 AM/PM indexer can still get the write lock** or the graph silently goes stale. Not a clean "20-min edit."
- **Rule:** the graph should live wherever the orchestrator lives. **Resolves automatically once Whitt picks his home surface.**

### 3. THE REAL STRUCTURAL PROBLEM — too many agents at once
Screen showed **4 AI agents** running: 2 Claudes + 1 Codex in VS Code + this Desktop orchestrator. This is the collision pattern that caused all session's drift (scattered notes, lock fights, duplicate work).
**Recommendation (Confidence 17/20):** Pick ONE permanent home — **VS Code** (Wispr Flow voice works there, boots orchestrator from `C:\Users\whitt\CLAUDE.md`). Then: close Codex, keep one Claude worker, retire/demote Claude Desktop, and the graph resolves to Option B.
**Whitt's pending answer:** "Is your home VS Code or Claude Desktop?" — that one choice untangles everything.

### 4. OneDrive is hydrating your dev tools (the "why is it downloading?" mystery, solved)
A 253 MB download of `cloudcode_cli.exe` "from OneDrive" appeared. **Your Claude binary + configs + Documents live in OneDrive-synced paths**, so Windows Files-On-Demand keeps yanking them down. Fix: right-click dev folders + Claude install → **"Always keep on this device."**

### 5. Lower priority / queued
- **Dwyer Interiors end-to-end run** = case study #0 (YC Screen → PAI → agents → G-Stack). The strategic thread, repeatedly deferred all session.
- Private remote backup of the vault (now that it's clean) — solves the no-backup single-point-of-failure.
- GitHub billing flagged red — check Settings → Billing.
- VS Code is running **as Administrator** — causes file-permission mismatches; consider relaunching normally.
- TXS deal records (TXS5345 priority + TXS5450/5513/5491) → write to `knowledge\System\`.

---

## 🔒 STANDING SECURITY CONSTRAINTS (do not violate)
- **Quarantine, never delete.** All cleanup moves to labeled quarantine folders.
- **Never touch Star Voss case files or the knowledge vault without explicit per-action OK.** (Decision-record notes are pre-authorized.)
- **Confirm Hermes + trading bot alive after ANY infra change.**
- **Use `wsl.exe` for WSL.** The plain Bash tool is Git Bash on Windows, NOT WSL.
- **Kill processes by exact PID only — never by name** (the Sweeper runs as `pythonw`).
- **Never print raw secrets** (`grep -oE` etc.) — redact in-script (first-4-chars). *This error became a permanent rule this session.*
- **Nothing enters the vault without Whitt's approval. Scrub all secrets first.**
- **Rotate-before-push** stays the rule for the vault.

## 🧭 NEW STANDING RULE (logged this session)
**One driver owns shared state.** Only one Claude/agent touches the vault, the handoff, or Hermes at a time. Spin up a second instance ONLY for genuinely independent work in a different folder.

---

## ▶️ NEXT SESSION STARTS WITH
1. Run anti-drift check (callsigns fire, live systems alive, state matches SYSTEM-MAP).
2. Orient Whitt: "Infra is green. Two things waiting on you: revoke the 2 PATs, and pick your home surface (VS Code or Desktop). Then we start Dwyer Interiors."
3. Get the home-surface answer → resolve graph + collapse the 4-agent collision.
4. **Start Dwyer Interiors case study #0.**
