def basic_fraud_checks(user_input):
    """
    Rule-based fraud checks.
    Runs separately — does NOT affect current system yet.
    """

    income = user_input.get("annual_income", 0)
    loan_amount = user_input.get("loan_amount", 0)

    issues = []

    if income > 2000000:
        issues.append("Unusually high income declared")

    if loan_amount > income * 2:
        issues.append("Loan amount too high compared to income")

    return issues