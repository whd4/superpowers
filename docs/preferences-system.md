# Personal Preferences System

> Two surfaces. Two install steps. One source of truth.

## What this is

A two-part personal-preferences system that gives Whitt a consistent persona, ADHD response discipline, and orchestrated session startup across **both** Claude surfaces:

1. **Desktop app (claude.ai web + native)** — static text pasted into Settings → Profile → "What personal preferences should Claude consider in responses?"
2. **Claude Code (CLI)** — dynamic SessionStart hook that injects the same persona, probes for `HENRY_CONTEXT.md`, and reports Knowledge Base / Graph / Vector-DB readiness.

Both surfaces stay in sync because the desktop preferences file is rendered from the same content as the `personal-preferences` skill.

## Install — Desktop App

1. Open Claude → **Settings → Profile**.
2. In the **"What personal preferences should Claude consider in responses?"** field, paste the contents of [`preferences/whitt-preferences.md`](../preferences/whitt-preferences.md).
3. Save.

**Verify:** start a new chat. Claude should respond bottom-line-first with a `NEXT ACTION →` footer, even before any codeword is used.

## Install — Claude Code

The Superpowers plugin already wires the SessionStart hook through `.claude-plugin/plugin.json` and `hooks/hooks.json`. To activate the enhanced version:

1. Make sure the plugin is loaded — your `.claude/settings.json` (project) or `~/.claude/settings.json` (user) references the `whd4/superpowers` marketplace + plugin.
2. `cd` into a project directory so `$CLAUDE_PROJECT_DIR` resolves correctly.
3. Start a Claude Code session. The hook fires on `startup`, `resume`, `clear`, and `compact` (matchers in `hooks/hooks.json`).

**Verify the hook is firing** — at the top of Claude's first message in the session you should see a banner like:

```
═══ HENRY AI OS — SESSION START ═══
HENRY_CONTEXT: PRESENT at C:\Users\whitt\DevFactory\dark-factory\HENRY_CONTEXT.md
Knowledge Base: found at ~/.henry/kb.db
Graph (Mermaid MCP): not probed (check Mermaid Chart MCP availability in /mcp)
Vector DB: Supabase configured ($SUPABASE_URL set)
Project dir: ...
Plugin root: ...
═══════════════════════════════════
```

If you don't see the banner, the hook didn't fire. Debug by running it manually:

```bash
# From the plugin root
bash hooks/session-start.sh | jq .
```

You should see a JSON object with `hookSpecificOutput.additionalContext` containing the session status, personal-preferences, henry-ai-os, and using-superpowers blocks.

## What the hook does (in order)

1. **Locate roots** — plugin root via `BASH_SOURCE`, project root via `$CLAUDE_PROJECT_DIR` (fallback `$PWD`).
2. **Read skills** in priority order:
   - `skills/personal-preferences/SKILL.md`
   - `skills/henry-ai-os/SKILL.md`
   - `skills/using-superpowers/SKILL.md`
3. **Probe `HENRY_CONTEXT.md`** in project root — if present, excerpt first 2KB.
4. **Probe data stores:**
   - Knowledge Base: `$HOME/.henry/kb.db` or `$PROJECT_DIR/.henry/kb.db`
   - Vector DB: `$PROJECT_DIR/.henry/vector.db` or `$SUPABASE_URL` env var
   - Graph: presence of Mermaid Chart MCP (reported as "not probed" — MCP availability isn't shell-visible)
5. **Emit** a single JSON object with `additionalContext` containing the SESSION STATUS banner + all three skills + the HENRY_CONTEXT excerpt.

## Skill consolidation map

See [`skills/personal-preferences/SKILL.md`](../skills/personal-preferences/SKILL.md) — the body documents the full 23-skill catalog grouped into 9 functional categories with three concrete merge recommendations (net 23 → 19 skills).

**Architectural recommendation:** per-project skill scoping (`.claude/skills/` in each project) over one global pile. Drop only the skills the project actually uses, rather than serving the whole catalog every session.

## Files

| Path | Purpose |
|------|---------|
| `preferences/whitt-preferences.md` | Desktop app paste target |
| `skills/personal-preferences/SKILL.md` | Core volume / entry skill with consolidation map |
| `hooks/session-start.sh` | Bash hook (Linux / macOS / Git-Bash on Windows) |
| `hooks/run-hook.cmd` | Windows polyglot wrapper (existing) |
| `hooks/hooks.json` | Claude Code hook registration (existing) |
| `docs/preferences-system.md` | This file |

## Updating

When Whitt's preferences change, update **both files** in the same commit:

- `preferences/whitt-preferences.md` (desktop paste target)
- `skills/personal-preferences/SKILL.md` (Claude Code skill body)

Then re-paste the updated desktop file into Settings → Profile. The Claude Code surface picks up changes automatically on next session start.
