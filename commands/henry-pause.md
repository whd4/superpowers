---
description: "HENRY AI OS: Checkpoint all state to files and await instruction"
---

Activate the henry-ai-os skill. The user has issued the PAUSE codeword.

**Codeword protocol — PAUSE:**
1. Generate a comprehensive state checkpoint:
   - All active tasks and their current status
   - All open decisions and pending questions
   - Current project context and where we left off
   - Any in-progress work that needs to be saved
2. Write this checkpoint to `HENRY_CONTEXT.md` in the project root
3. Confirm the checkpoint was saved
4. Await further instruction — do NOT take any proactive actions

The checkpoint file must contain enough context for a fresh session to pick up exactly where this one left off.
