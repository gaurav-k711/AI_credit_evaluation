import pandas as pd
from src.shap_explainer import explain_prediction

# Example applicant (same format as model input)
test_applicant = pd.DataFrame([{
    "business_type": 0,
    "years_in_operation": 4,
    "annual_revenue": 800000,
    "monthly_cashflow": 60000,
    "loan_amount_requested": 250000,
    "credit_score": 700,
    "existing_loans": 1,
    "debt_to_income_ratio": 0.35,
    "collateral_value": 350000,
    "repayment_history": 1
}])

explain_prediction(test_applicant)