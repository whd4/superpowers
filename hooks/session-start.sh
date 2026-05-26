#!/usr/bin/env bash
# SessionStart hook for superpowers plugin
#
# What it does:
#   1. Loads three skills in priority order (personal-preferences, henry-ai-os, using-superpowers)
#   2. Probes HENRY_CONTEXT.md in the project root and excerpts the first 2KB
#   3. Probes data store readiness: Knowledge Base, Graph (Mermaid MCP), Vector DB
#   4. Emits all of the above as a single SessionStart additionalContext JSON payload

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-${PWD:-${HOME}}}"

read_skill() {
    local skill_path="${PLUGIN_ROOT}/skills/$1/SKILL.md"
    if [ -f "$skill_path" ]; then
        cat "$skill_path"
    else
        printf '(skill %q not found at %s)' "$1" "$skill_path"
    fi
}

personal_preferences_content=$(read_skill "personal-preferences")
henry_ai_os_content=$(read_skill "henry-ai-os")
using_superpowers_content=$(read_skill "using-superpowers")

warning_message=""
legacy_skills_dir="${HOME}/.config/superpowers/skills"
if [ -d "$legacy_skills_dir" ]; then
    warning_message="\n\n<important-reminder>IN YOUR FIRST REPLY AFTER SEEING THIS MESSAGE YOU MUST TELL THE USER:⚠️ **WARNING:** Superpowers now uses Claude Code's skills system. Custom skills in ~/.config/superpowers/skills will not be read. Move custom skills to ~/.claude/skills instead. To make this message go away, remove ~/.config/superpowers/skills</important-reminder>"
fi

henry_context_status="ABSENT (no HENRY_CONTEXT.md in project root)"
henry_context_excerpt="(none)"
if [ -f "${PROJECT_DIR}/HENRY_CONTEXT.md" ]; then
    henry_context_status="PRESENT at ${PROJECT_DIR}/HENRY_CONTEXT.md"
    henry_context_excerpt=$(head -c 2000 "${PROJECT_DIR}/HENRY_CONTEXT.md" 2>/dev/null || echo "(read error)")
fi

kb_status="not configured"
if [ -f "${HOME}/.henry/kb.db" ]; then
    kb_status="found at ~/.henry/kb.db"
fi
if [ -f "${PROJECT_DIR}/.henry/kb.db" ]; then
    kb_status="found at ${PROJECT_DIR}/.henry/kb.db"
fi

graph_status="not probed (check Mermaid Chart MCP availability in /mcp)"

vector_db_status="not configured"
if [ -f "${PROJECT_DIR}/.henry/vector.db" ]; then
    vector_db_status="local Chroma at ${PROJECT_DIR}/.henry/vector.db"
fi
if [ -n "${SUPABASE_URL:-}" ]; then
    vector_db_status="Supabase configured (\$SUPABASE_URL set)"
fi

escape_for_json() {
    local input="$1"
    local output=""
    local i char
    for (( i=0; i<${#input}; i++ )); do
        char="${input:$i:1}"
        case "$char" in
            $'\\') output+='\\' ;;
            '"') output+='\"' ;;
            $'\n') output+='\n' ;;
            $'\r') output+='\r' ;;
            $'\t') output+='\t' ;;
            *) output+="$char" ;;
        esac
    done
    printf '%s' "$output"
}

session_status=$(cat <<STATUS
═══ HENRY AI OS — SESSION START ═══
HENRY_CONTEXT: ${henry_context_status}
Knowledge Base: ${kb_status}
Graph (Mermaid MCP): ${graph_status}
Vector DB: ${vector_db_status}
Project dir: ${PROJECT_DIR}
Plugin root: ${PLUGIN_ROOT}
═══════════════════════════════════
STATUS
)

personal_preferences_escaped=$(escape_for_json "$personal_preferences_content")
henry_ai_os_escaped=$(escape_for_json "$henry_ai_os_content")
using_superpowers_escaped=$(escape_for_json "$using_superpowers_content")
henry_context_excerpt_escaped=$(escape_for_json "$henry_context_excerpt")
session_status_escaped=$(escape_for_json "$session_status")
warning_escaped=$(escape_for_json "$warning_message")

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have superpowers. This is a HENRY AI Corporation session for Whitt Dwyer.\n\n## 1. SESSION STATUS\n${session_status_escaped}\n\n## 2. PERSONAL PREFERENCES (LOAD FIRST — ADHD rules, codewords, routing)\n${personal_preferences_escaped}\n\n## 3. HENRY AI OS (CEO operating system)\n${henry_ai_os_escaped}\n\n## 4. SUPERPOWERS PROTOCOL (mandatory skills protocol)\n${using_superpowers_escaped}\n\n## 5. LAST WRITTEN CONTEXT (HENRY_CONTEXT.md excerpt, if present — first 2KB)\n${henry_context_excerpt_escaped}\n${warning_escaped}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF

exit 0
