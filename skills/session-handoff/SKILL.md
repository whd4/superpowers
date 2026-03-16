---
name: session-handoff
when_to_use: |
  Use when approaching context limits or ending a session.
  Triggers: context window filling up, user says "pause" or "stop", end of work block.
---

# Session Handoff

Ensure no context is lost between sessions. This is a standing order.

## When to Trigger
- Context window approaching limits
- User issues PAUSE codeword
- Natural end of a work session
- Before any destructive operation on context

## Handoff Protocol

### Step 1: State Capture
- [ ] Update HENRY_CONTEXT.md with:
  - Current focus and what was accomplished
  - All open tasks with status
  - Any decisions made (add to Decision Log)
  - Blockers or items awaiting input

### Step 2: Task Inventory
- [ ] List all in-progress tasks
- [ ] List all tasks that were discussed but not started
- [ ] List any promises made to Whitt
- [ ] Identify next 3 priority actions

### Step 3: File Updates
- [ ] Save any work-in-progress to appropriate files
- [ ] Commit all changes to git
- [ ] Push to remote branch

### Step 4: Handoff Summary
Generate a summary block:

```
## SESSION HANDOFF — [date]
COMPLETED: [what got done]
IN PROGRESS: [what's partially done]
BLOCKED: [what needs input]
NEXT SESSION STARTS WITH: [exact first action]
FILES CHANGED: [list]
```

## Critical Rule
Never let a session end without updating HENRY_CONTEXT.md.
The next session's AI must be able to pick up exactly where this one left off.
