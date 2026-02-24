import pandas as pd
import numpy as np

# Always gives same data when re-run (important for consistency)
np.random.seed(42)

ROWS = 2500

business_types = ["Manufacturing", "Retail", "Services", "Trading"]
repayment_histories = ["Good", "Average", "Poor"]

data = {
    "business_type": np.random.choice(business_types, ROWS),
    "years_in_operation": np.random.randint(1, 25, ROWS),
    "annual_revenue": np.random.randint(300000, 8000000, ROWS),
    "monthly_cashflow": np.random.randint(20000, 500000, ROWS),
    "loan_amount_requested": np.random.randint(50000, 3000000, ROWS),
    "credit_score": np.random.randint(300, 850, ROWS),
    "existing_loans": np.random.randint(0, 5, ROWS),
    "debt_to_income_ratio": np.round(np.random.uniform(0.1, 0.9, ROWS), 2),
    "collateral_value": np.random.randint(0, 5000000, ROWS),
    "repayment_history": np.random.choice(repayment_histories, ROWS)
}

df = pd.DataFrame(data)

# -------- DEFAULT LOGIC (VERY IMPORTANT) --------
def calculate_default(row):
    risk = 0

    if row["credit_score"] < 600:
        risk += 1
    if row["debt_to_income_ratio"] > 0.6:
        risk += 1
    if row["loan_amount_requested"] > row["annual_revenue"]:
        risk += 1
    if row["repayment_history"] == "Poor":
        risk += 1

    return 1 if risk >= 2 else 0

df["default_flag"] = df.apply(calculate_default, axis=1)

# Save dataset inside data folder
df.to_csv("data/business_credit_data.csv", index=False)

print("✅ Synthetic dataset generated successfully")
print("Total records:", len(df))