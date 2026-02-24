def generate_loan_recommendation(user_input, risk_score=50):
    """
    Smart recommendation engine.
    This does NOT change your current approval logic.
    It only suggests better loan decisions.
    """

    requested_amount = user_input.get("loan_amount", 100000)
    annual_income = user_input.get("annual_income", 200000)

    # safe loan logic
    safe_limit = annual_income * 0.4

    if risk_score < 40:
        recommended_amount = min(requested_amount, safe_limit)
        emi = recommended_amount / 24
        insurance_needed = False
        subsidy_hint = "Eligible for low‑interest schemes"

    elif 40 <= risk_score < 70:
        recommended_amount = min(requested_amount * 0.8, safe_limit)
        emi = recommended_amount / 18
        insurance_needed = True
        subsidy_hint = "Recommend crop insurance"

    else:
        recommended_amount = requested_amount * 0.5
        emi = recommended_amount / 12
        insurance_needed = True
        subsidy_hint = "High‑risk borrower, limited credit advised"

    return {
        "recommended_loan_amount": round(recommended_amount),
        "estimated_emi": round(emi),
        "insurance_required": insurance_needed,
        "subsidy_suggestion": subsidy_hint
    }