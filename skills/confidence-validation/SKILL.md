---
name: confidence-validation
description: Use when uncertain about refactors, complex changes, or architectural decisions - dispatches recursive validation to catch error islands before low-confidence code ships; implements DeepConf-style multi-agent verification
---

# Confidence Validation

## Overview

Not all code changes carry equal certainty. When confidence is low, validate before executing.

**Core principle:** Uncertainty is signal, not weakness. Act on it.

## The Confidence Gate

```
if model_confidence < threshold:
    recursive_validate(current_snippet)
else:
    execute_code()
```

**Threshold calibration:**
- **< 30%**: STOP. Dispatch validator immediately.
- **30-70%**: Caution zone. Consider validation.
- **> 70%**: Proceed, but document assumptions.

## When to Trigger

**Mandatory validation (confidence < 30%):**
- Refactoring unfamiliar code
- Modifying code without tests
- Changing behavior you don't fully understand
- Working with complex regex, algorithms, or state machines
- Database migrations with data transformation
- Security-sensitive changes

**Recommended validation (30-70%):**
- Large refactors spanning multiple files
- Performance optimizations with trade-offs
- API contract changes
- Concurrency or async modifications

## Error Islands

Error islands are logical gaps that survive surface-level review:

| Type | Description | Example |
|------|-------------|---------|
| **Edge cases** | Unhandled boundary conditions | Empty arrays, null values, overflow |
| **State gaps** | Invalid state transitions possible | User logged out mid-operation |
| **Race conditions** | Timing-dependent failures | Concurrent writes without locks |
| **Type coercion** | Implicit conversions causing bugs | "5" + 5 = "55" in JavaScript |
| **Breaking changes** | Downstream effects not considered | Changed return type, removed field |
| **Assumption drift** | Code assumes context that changed | Hardcoded paths, env variables |

## How to Request Validation

**1. Assess your confidence:**

```
Before implementing, ask:
- How well do I understand this code?
- What could go wrong that I'm not seeing?
- Am I making assumptions about behavior?

Assign percentage: ___%
```

**2. If below threshold, dispatch validator:**

Use Task tool with confidence-validator type, fill template at `confidence-validator.md`

**Placeholders:**
- `{CONFIDENCE_LEVEL}` - Your assessed percentage (e.g., "20%")
- `{CODE_SNIPPET}` - The code being validated
- `{CHANGE_DESCRIPTION}` - What you're trying to accomplish
- `{KNOWN_CONCERNS}` - Issues you're already aware of
- `{CONTEXT}` - Surrounding code, dependencies, constraints

**3. Act on validator response:**

| Response | Action |
|----------|--------|
| CONFIDENCE_HIGH | Proceed with implementation |
| Issues found | Apply corrections, re-validate if needed |
| NEEDS_CONTEXT | Provide additional information, retry |
| RECOMMEND_REWRITE | Consider alternative approach |

## The Validation Loop

```
WHILE confidence < threshold:
    1. DISPATCH validator with current approach
    2. RECEIVE feedback (issues or CONFIDENCE_HIGH)
    3. IF issues found:
        - Apply corrections
        - Re-assess confidence
    4. IF CONFIDENCE_HIGH:
        - EXIT loop, proceed
    5. IF 3+ iterations without resolution:
        - Escalate: request human review
        - Consider: is this the right approach?
```

## Validator Agent Behavior

The confidence-validator agent should:

**DO:**
- Hunt for error islands systematically
- Check edge cases against actual code paths
- Verify assumptions match implementation
- Suggest corrections with reasoning
- Explicitly state CONFIDENCE_HIGH when satisfied

**DON'T:**
- Rubber-stamp without analysis
- Flag style issues as confidence problems
- Require perfection (good enough is enough)
- Cycle indefinitely on minor issues

## Example Flow

```
[Refactoring auth middleware - unfamiliar code]

You: This auth refactor touches session handling I don't fully understand.
     Confidence: 25%

     [Dispatch confidence-validator]
       CONFIDENCE_LEVEL: 25%
       CODE_SNIPPET: [auth middleware changes]
       CHANGE_DESCRIPTION: Consolidate session validation into single middleware
       KNOWN_CONCERNS: Not sure if all routes need session
       CONTEXT: Express.js, sessions stored in Redis

[Validator returns]:
  ERROR_ISLANDS_FOUND:
    1. CRITICAL: /api/webhook routes need auth bypass (currently would reject)
    2. IMPORTANT: Session refresh logic removed, tokens will expire mid-request
    3. EDGE_CASE: Guest checkout flow assumes no session exists

  CORRECTIONS:
    - Add webhook routes to bypass list
    - Restore session refresh call
    - Add session-optional flag for guest routes

  CONFIDENCE: LOW until corrections applied

You: [Apply corrections]
     [Re-dispatch validator with updated code]

[Validator returns]:
  CONFIDENCE_HIGH
  Reasoning: Auth bypass list complete, session refresh preserved,
             guest flow handled with optional flag. No remaining error islands.

You: [Proceed with implementation]
```

## Integration with Other Skills

**With verification-before-completion:**
- Confidence validation happens BEFORE implementation
- Verification happens AFTER implementation
- Both required for high-stakes changes

**With systematic-debugging:**
- Use confidence validation when forming hypotheses
- Low confidence in root cause = validate before fixing

**With code-review:**
- Confidence validation is self-review
- Code review is peer review
- Use both for defense in depth

**With test-driven-development:**
- Low confidence? Write tests first to clarify behavior
- Tests can raise confidence above threshold

## Confidence Signals

**Low confidence indicators:**
- "I think this should work"
- "This might break something"
- "I'm not sure why this exists"
- "Let me just try it"
- Copying code you don't understand

**High confidence indicators:**
- "This follows the established pattern at X"
- "Tests cover this case"
- "I traced the data flow through these functions"
- "The type system guarantees this"

## Red Flags

**Never:**
- Ship code with < 30% confidence unvalidated
- Ignore validator-found error islands
- Assume "it works on my machine" = confidence
- Skip validation because of time pressure
- Override RECOMMEND_REWRITE without justification

**If validator keeps finding issues:**
- Step back: is the approach fundamentally flawed?
- Consider: rewrite with TDD instead of patching
- Ask: does this need architectural review?

## Why This Matters

Low-confidence code that ships becomes:
- Production incidents at 3am
- Security vulnerabilities discovered by attackers
- Tech debt that compounds
- Trust erosion with team and users

Validation takes minutes. Incidents take hours to days.

## The Bottom Line

**Confidence is information. Low confidence = validate first.**

Your uncertainty is telling you something. Listen to it.

See template at: confidence-validation/confidence-validator.md
