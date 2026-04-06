#!/usr/bin/env python3
"""HENRY AI Risk Matrix Calculator.

Scores risks by probability (1-5) x impact (1-5).
Returns sorted risk matrix with severity ratings.

Usage:
  python risk_matrix.py '[{"name":"Client concentration","probability":4,"impact":5},{"name":"Key person risk","probability":3,"impact":4}]'
  python risk_matrix.py --test
"""
import json
import sys


def assess(risks: list) -> dict:
    if not isinstance(risks, list) or len(risks) == 0:
        return {"error": "Input must be a non-empty JSON array of risk objects"}

    scored = []
    for i, risk in enumerate(risks):
        name = risk.get("name", f"Risk {i+1}")
        prob = risk.get("probability")
        impact = risk.get("impact")
        if not (prob and 1 <= prob <= 5 and impact and 1 <= impact <= 5):
            return {"error": f"Risk '{name}': probability and impact must be 1-5"}

        severity = prob * impact
        if severity >= 20:
            rating = "CRITICAL"
        elif severity >= 12:
            rating = "HIGH"
        elif severity >= 6:
            rating = "MEDIUM"
        else:
            rating = "LOW"

        scored.append({
            "name": name,
            "probability": prob,
            "impact": impact,
            "severity": severity,
            "rating": rating,
            "mitigation": risk.get("mitigation", "NOT DEFINED — requires mitigation plan"),
        })

    scored.sort(key=lambda x: x["severity"], reverse=True)

    critical = sum(1 for r in scored if r["rating"] == "CRITICAL")
    high = sum(1 for r in scored if r["rating"] == "HIGH")

    if critical > 0:
        overall = "UNACCEPTABLE — critical risks must be mitigated before proceeding"
    elif high >= 3:
        overall = "HIGH — multiple high risks require comprehensive mitigation"
    elif high >= 1:
        overall = "MODERATE — proceed with active risk monitoring"
    else:
        overall = "LOW — standard monitoring sufficient"

    return {
        "risks": scored,
        "summary": {
            "total_risks": len(scored),
            "critical": critical,
            "high": high,
            "medium": sum(1 for r in scored if r["rating"] == "MEDIUM"),
            "low": sum(1 for r in scored if r["rating"] == "LOW"),
        },
        "overall_assessment": overall,
    }


def run_tests():
    # Critical risk
    r = assess([{"name": "test", "probability": 5, "impact": 5}])
    assert r["risks"][0]["rating"] == "CRITICAL"
    assert r["risks"][0]["severity"] == 25

    # Sorted by severity
    r = assess([
        {"name": "low", "probability": 1, "impact": 1},
        {"name": "high", "probability": 4, "impact": 4},
        {"name": "med", "probability": 2, "impact": 3},
    ])
    assert r["risks"][0]["name"] == "high"
    assert r["risks"][-1]["name"] == "low"

    # Low risk overall
    r = assess([{"name": "minor", "probability": 1, "impact": 2}])
    assert "LOW" in r["overall_assessment"]

    # Invalid
    r = assess([])
    assert "error" in r

    r = assess([{"name": "bad", "probability": 6, "impact": 1}])
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
        print(json.dumps(assess(data), indent=2))
    else:
        print(__doc__)
