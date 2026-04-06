#!/usr/bin/env python3
"""HENRY AI SBA Loan Calculator.

Calculates monthly payment, total interest, and amortization summary
for SBA 7(a) loan structures.

Usage:
  python sba_calculator.py '{"purchase_price":500000,"down_payment_pct":10,"annual_rate":6.5,"term_years":10}'
  python sba_calculator.py --test
"""
import json
import sys
import math


def calculate(data: dict) -> dict:
    price = data.get("purchase_price", 0)
    down_pct = data.get("down_payment_pct", 10)
    rate = data.get("annual_rate", 0)
    years = data.get("term_years", 10)

    if price <= 0 or rate <= 0 or years <= 0:
        return {"error": "purchase_price, annual_rate, and term_years must be positive"}

    down_payment = price * (down_pct / 100)
    loan_amount = price - down_payment
    monthly_rate = rate / 100 / 12
    num_payments = years * 12

    # Standard amortization formula
    if monthly_rate == 0:
        monthly_payment = loan_amount / num_payments
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

    total_paid = monthly_payment * num_payments
    total_interest = total_paid - loan_amount
    annual_debt_service = monthly_payment * 12

    # SBA guarantee fee estimate (approximate)
    if loan_amount <= 150000:
        guarantee_fee_pct = 2.0
    elif loan_amount <= 700000:
        guarantee_fee_pct = 3.0
    else:
        guarantee_fee_pct = 3.5
    guarantee_fee = loan_amount * 0.75 * (guarantee_fee_pct / 100)  # 75% guaranteed portion

    closing_costs_est = loan_amount * 0.04  # ~4% estimate

    return {
        "purchase_price": price,
        "down_payment": round(down_payment, 2),
        "loan_amount": round(loan_amount, 2),
        "annual_rate_pct": rate,
        "term_years": years,
        "monthly_payment": round(monthly_payment, 2),
        "annual_debt_service": round(annual_debt_service, 2),
        "total_interest": round(total_interest, 2),
        "total_cost": round(total_paid + down_payment, 2),
        "sba_guarantee_fee_est": round(guarantee_fee, 2),
        "closing_costs_est": round(closing_costs_est, 2),
        "total_cash_needed_at_close": round(down_payment + guarantee_fee + closing_costs_est, 2),
    }


def run_tests():
    r = calculate({"purchase_price": 500000, "down_payment_pct": 10, "annual_rate": 6.5, "term_years": 10})
    assert r["loan_amount"] == 450000.0
    assert r["down_payment"] == 50000.0
    assert 5000 < r["monthly_payment"] < 6000, f"Monthly payment {r['monthly_payment']} out of expected range"
    assert r["total_interest"] > 0
    assert abs(r["annual_debt_service"] - r["monthly_payment"] * 12) < 0.02

    # Edge: invalid input
    r = calculate({"purchase_price": 0, "annual_rate": 5, "term_years": 10})
    assert "error" in r

    # Small loan
    r = calculate({"purchase_price": 100000, "down_payment_pct": 10, "annual_rate": 7.0, "term_years": 10})
    assert r["loan_amount"] == 90000.0
    assert r["sba_guarantee_fee_est"] > 0

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
