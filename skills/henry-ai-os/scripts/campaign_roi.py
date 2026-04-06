#!/usr/bin/env python3
"""HENRY AI Campaign ROI Calculator.

Calculates expected leads, customers, revenue, CAC, and ROAS
from campaign parameters.

Usage:
  python campaign_roi.py '{"budget":5000,"impressions":50000,"ctr_pct":2.5,"conversion_pct":5,"close_rate_pct":20,"avg_deal_value":15000}'
  python campaign_roi.py --test
"""
import json
import sys


def calculate(data: dict) -> dict:
    budget = data.get("budget", 0)
    impressions = data.get("impressions", 0)
    ctr = data.get("ctr_pct", 0) / 100
    conv = data.get("conversion_pct", 0) / 100
    close = data.get("close_rate_pct", 0) / 100
    deal_value = data.get("avg_deal_value", 0)

    if budget <= 0 or impressions <= 0 or deal_value <= 0:
        return {"error": "budget, impressions, and avg_deal_value must be positive"}

    clicks = int(impressions * ctr)
    leads = int(clicks * conv)
    customers = max(1, int(leads * close)) if leads > 0 else 0
    revenue = customers * deal_value
    cac = round(budget / customers, 2) if customers > 0 else None
    roas = round(revenue / budget, 2) if budget > 0 else 0
    cpl = round(budget / leads, 2) if leads > 0 else None
    breakeven_customers = max(1, int(budget / deal_value) + 1) if deal_value > 0 else None

    if roas >= 5:
        verdict = "EXCELLENT — strong ROI, consider scaling budget"
    elif roas >= 2:
        verdict = "GOOD — profitable, monitor and optimize"
    elif roas >= 1:
        verdict = "MARGINAL — barely breaking even, needs optimization"
    else:
        verdict = "NEGATIVE — losing money, pause and redesign"

    return {
        "inputs": {
            "budget": budget,
            "impressions": impressions,
            "ctr_pct": data.get("ctr_pct"),
            "conversion_pct": data.get("conversion_pct"),
            "close_rate_pct": data.get("close_rate_pct"),
            "avg_deal_value": deal_value,
        },
        "funnel": {
            "impressions": impressions,
            "clicks": clicks,
            "leads": leads,
            "customers": customers,
        },
        "economics": {
            "revenue": revenue,
            "cost_per_lead": cpl,
            "cost_per_customer": cac,
            "roas": roas,
            "breakeven_customers": breakeven_customers,
        },
        "verdict": verdict,
    }


def run_tests():
    r = calculate({
        "budget": 5000,
        "impressions": 50000,
        "ctr_pct": 2.5,
        "conversion_pct": 5,
        "close_rate_pct": 20,
        "avg_deal_value": 15000,
    })
    assert r["funnel"]["clicks"] == 1250
    assert r["funnel"]["leads"] == 62
    assert r["funnel"]["customers"] >= 1
    assert r["economics"]["roas"] > 0
    assert r["economics"]["revenue"] > 0

    # Zero budget
    r = calculate({"budget": 0, "impressions": 100, "avg_deal_value": 100})
    assert "error" in r

    # High ROAS
    r = calculate({
        "budget": 1000,
        "impressions": 100000,
        "ctr_pct": 5,
        "conversion_pct": 10,
        "close_rate_pct": 50,
        "avg_deal_value": 10000,
    })
    assert "EXCELLENT" in r["verdict"]

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
        print(json.dumps(calculate(data), indent=2))
    else:
        print(__doc__)
