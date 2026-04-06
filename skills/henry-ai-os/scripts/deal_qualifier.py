#!/usr/bin/env python3
"""HENRY AI Deal Qualifier (BANT+).

Scores deals on Budget, Authority, Need, Timeline, Fit (0-2 each).
Returns qualification tier and recommended action.

Usage:
  python deal_qualifier.py '{"budget":2,"authority":1,"need":2,"timeline":1,"fit":2}'
  python deal_qualifier.py --test
"""
import json
import sys

CRITERIA = ["budget", "authority", "need", "timeline", "fit"]


def qualify(data: dict) -> dict:
    scores = {}
    total = 0
    for c in CRITERIA:
        val = data.get(c)
        if val is None or not (0 <= val <= 2):
            return {"error": f"Missing or invalid score for '{c}' (must be 0-2)"}
        scores[c] = val
        total += val

    if total >= 8:
        tier = "PURSUE AGGRESSIVELY"
        action = "Fast-track to proposal. Assign /sales agent immediately."
    elif total >= 5:
        tier = "NURTURE"
        action = "Add to nurture sequence. Follow up in 2 weeks. Build relationship."
    else:
        tier = "DISQUALIFY"
        action = "Park this lead. Re-evaluate if circumstances change."

    # Flag critical gaps
    gaps = []
    if scores["budget"] == 0:
        gaps.append("No budget identified — cannot proceed without funding path")
    if scores["authority"] == 0:
        gaps.append("No access to decision-maker — find champion or escalate")
    if scores["need"] == 0:
        gaps.append("No recognized pain — this is a nice-to-have, not a must-have")

    return {
        "scores": scores,
        "total": total,
        "max": 10,
        "tier": tier,
        "action": action,
        "critical_gaps": gaps if gaps else None,
    }


def run_tests():
    # Strong deal
    r = qualify({"budget": 2, "authority": 2, "need": 2, "timeline": 2, "fit": 2})
    assert r["total"] == 10
    assert r["tier"] == "PURSUE AGGRESSIVELY"

    # Nurture
    r = qualify({"budget": 1, "authority": 1, "need": 2, "timeline": 0, "fit": 1})
    assert r["tier"] == "NURTURE"

    # Disqualify
    r = qualify({"budget": 0, "authority": 0, "need": 1, "timeline": 0, "fit": 1})
    assert r["tier"] == "DISQUALIFY"
    assert len(r["critical_gaps"]) >= 2

    # Invalid
    r = qualify({"budget": 3})
    assert "error" in r

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1:
        try:
            data = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON input"}))
            sys.exit(1)
        print(json.dumps(qualify(data), indent=2))
    else:
        print(__doc__)
