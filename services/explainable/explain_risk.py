def generate_risk_explanation(risk_score, esg_score, alt_data_score=None, climate_score=None):
    """
    Explains WHY a decision was made.
    Add-on layer only — does not change current system.
    """

    explanation = []

    # risk interpretation
    if risk_score < 40:
        explanation.append("Applicant has low financial risk.")
    elif 40 <= risk_score < 70:
        explanation.append("Applicant has moderate financial risk.")
    else:
        explanation.append("Applicant has high financial risk.")

    # ESG reasoning
    if esg_score > 70:
        explanation.append("Strong ESG impact improves approval chances.")
    elif esg_score < 40:
        explanation.append("Low ESG contribution increases risk.")

    # alternative data insight
    if alt_data_score:
        if alt_data_score > 70:
            explanation.append("Positive behavioral and crop data improves reliability.")
        else:
            explanation.append("Limited alternative data confidence.")

    # climate insight
    if climate_score:
        if climate_score < 40:
            explanation.append("Adverse climate conditions increase risk.")
        else:
            explanation.append("Stable climate supports repayment capacity.")

    return {
        "risk_explanation": explanation
    }