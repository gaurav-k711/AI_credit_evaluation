import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# -------------------------
# 1. Load Dataset
# -------------------------
data = pd.read_csv("data/business_credit_data.csv")

# -------------------------
# 2. Encode Categorical Columns
# -------------------------
business_encoder = LabelEncoder()
repayment_encoder = LabelEncoder()

data["business_type"] = business_encoder.fit_transform(data["business_type"])
data["repayment_history"] = repayment_encoder.fit_transform(data["repayment_history"])

# -------------------------
# 3. Separate Features & Target
# -------------------------
X = data.drop("default_flag", axis=1)
y = data["default_flag"]

# -------------------------
# 4. Train-Test Split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# 5. Train Logistic Regression
# -------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# -------------------------
# 6. Evaluate Model
# -------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("✅ Model trained successfully")
print("📊 Accuracy:", round(accuracy * 100, 2), "%")

# -------------------------
# 7. Save Model & Encoders
# -------------------------
joblib.dump(model, "model/credit_risk_model.pkl")
joblib.dump(business_encoder, "model/business_encoder.pkl")
joblib.dump(repayment_encoder, "model/repayment_encoder.pkl")

print("💾 Model and encoders saved in model/ folder")