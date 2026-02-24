import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("model/credit_risk_model.pkl")

# Sample background data (VERY IMPORTANT)
# Use small synthetic examples for SHAP baseline
background_data = pd.DataFrame([
    [0, 5, 500000, 40000, 200000, 650, 1, 0.4, 300000, 1],
    [1, 3, 300000, 25000, 150000, 600, 2, 0.5, 200000, 0],
    [2, 8, 800000, 70000, 300000, 720, 0, 0.3, 600000, 2]
], columns=[
    "business_type",
    "years_in_operation",
    "annual_revenue",
    "monthly_cashflow",
    "loan_amount_requested",
    "credit_score",
    "existing_loans",
    "debt_to_income_ratio",
    "collateral_value",
    "repayment_history"
])

# Create SHAP explainer
explainer = shap.Explainer(model, background_data)

def explain_prediction(input_df):
    """
    Takes one applicant row and explains model decision
    """
    shap_values = explainer(input_df)

    # Summary plot
    shap.plots.waterfall(shap_values[0])

    plt.show()