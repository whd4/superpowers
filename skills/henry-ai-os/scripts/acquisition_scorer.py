#!/usr/bin/env python3
"""HENRY AI Acquisition Scoring Tool.

Scores acquisition targets on 5 weighted dimensions.
Revenue Quality and Margin Potential are weighted 2x.

Usage:
  python acquisition_scorer.py '{"revenue_quality":4,"margin_potential":3,"integration_complexity":4,"time_to_value":5,"strategic_fit":3}'
  python acquisition_scorer.py --test
"""
import json
import sys

DIMENSIONS = {
    "revenue_quality":        {"weight": 2, "label": "Revenue Quality"},
    "margin_potential":       {"weight": 2, "label": "Margin Potential"},
    "integration_complexity": {"weight": 1, "label": "Integration Complexity"},
    "time_to_value":          {"weight": 1, "label": "Time to Value"},
    "strategic_fit":          {"weight": 1, "label": "Strategic Fit"},
}

MAX_WEIGHTED = sum(5 * d["weight"] for d in DIMENSIONS.values())  # 35


def score(data: dict) -> dict:
    weighted_total = 0
    details = []
    for key, meta in DIMENSIONS.items():
        val = data.get(key)
        if val is None or not (1 <= val <= 5):
            return {"error": f"Missing or invalid score for '{key}' (must be 1-5)"}
        contrib = val * meta["weight"]
        weighted_total += contrib
        details.append({"dimension": meta["label"], "score": val, "weight": meta["weight"], "contribution": contrib})

    # Normalize to 25-point scale for readability
    normalized = round(weighted_total / MAX_WEIGHTED * 25, 1)

    if normalized >= 20:
        recommendation = "STRONG GO — pursue aggressively"
    elif normalized >= 15:
        recommendation = "CONDITIONAL GO — proceed with specific mitigations"
    elif normalized >= 10:
        recommendation = "WEAK — park unless strategic override"
    else:
        recommendation = "NO GO — pass"

    return {
        "weighted_total": weighted_total,
        "max_possible": MAX_WEIGHTED,
        "normalized_score": normalized,
        "out_of": 25,
        "recommendation": recommendation,
        "details": details,
    }


def run_tests():
    # Strong go
    r = score({"revenue_quality": 5, "margin_potential": 5, "integration_complexity": 5, "time_to_value": 5, "strategic_fit": 5})
    assert r["normalized_score"] == 25.0, f"Perfect score should be 25, got {r['normalized_score']}"
    assert "STRONG GO" in r["recommendation"]

    # No go
    r = score({"revenue_quality": 1, "margin_potential": 1, "integration_complexity": 1, "time_to_value": 1, "strategic_fit": 1})
    assert r["normalized_score"] <= 10, f"Minimum score should be <=10, got {r['normalized_score']}"

    # Weighted check: revenue_quality matters more
    r1 = score({"revenue_quality": 5, "margin_potential": 3, "integration_complexity": 3, "time_to_value": 3, "strategic_fit": 3})
    r2 = score({"revenue_quality": 3, "margin_potential": 3, "integration_complexity": 5, "time_to_value": 3, "strategic_fit": 3})
    assert r1["weighted_total"] > r2["weighted_total"], "Revenue quality (2x weight) should outweigh integration complexity (1x)"

    # Invalid input
    r = score({"revenue_quality": 6})
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
        print(json.dumps(score(data), indent=2))
    else:
        print(__doc__)
