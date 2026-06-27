# Two Claudes — Cloud vs Local (capability map)

> **Read this to know which Claude can do what.** There are two Claude Code surfaces working as one team. They have different reach.

## The two surfaces

| | ☁️ CLOUD Claude (Desktop/web app) | 💻 LOCAL Claude (VS Code) |
|---|---|---|
| **Runs on** | A rented cloud computer (the "cloud environment") | Whitt's actual PC |
| **Can see** | **Only the `superpowers` repo** (sandbox) | **The whole machine** — every file/folder |
| **The machine (C:\Users\whitt)** | ❌ Blind to it | ✅ Full access |
| **WSL / Hermes / trading bot / mission-control** | ❌ Can't reach | ✅ Yes (via `wsl.exe`) |
| **Knowledge vault + Kuzu graph** | ❌ Not visible | ✅ Reads/writes |
| **Voice (Wispr Flow)** | ❌ No | ✅ Works in VS Code |
| **Run real commands on the box** | ❌ No | ✅ Yes |

## ☁️ CLOUD Claude — strengths (cloud connectors available through it)
Blind to the machine, but wired into cloud tools:
- **Web** — search + fetch any site (research, due diligence)
- **Google** — Gmail, Calendar, Drive
- **Work apps** — Notion, Supabase, Cloudflare, Figma, Canva, Miro
- **Knowledge** — Hugging Face, Context7 (live code docs), Microsoft Learn, Mermaid
- **Whitt's** — GitHub (superpowers repo), Trellis (legal data), Command Center
- **The superpowers repo** — writes/commits/pushes files here

## 💻 LOCAL Claude — strengths
- Anything touching business systems — Hermes, trading bot, the vault, the graph
- Real work on the machine — fix files, run scripts, install things
- Voice (Whitt talks, it works)
- The HENRY agent roster, G-Stack, PAI (all on disk)

## 🎯 The rule
```
Brain / research / cloud apps / strategy    →  ☁️ CLOUD Claude
Hands on the machine / live systems / voice →  💻 LOCAL Claude
```

**Why relaying happens:** Cloud Claude is the researcher + coordinator + cloud-tools brain, but cannot physically reach the machine. Local Claude is the hands. To act on the machine, Cloud Claude writes instruction blocks that Whitt (or a local session) executes. Together they are one team.

> Standing rule: **one driver owns shared state** (vault, handoff, Hermes) at a time — never two Claudes editing the same thing concurrently.
