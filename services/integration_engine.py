from services.alt_data.alt_data_pipeline import build_alt_data_profile
from services.climate.climate_pipeline import build_climate_profile
from services.recommendation.loan_recommender import generate_loan_recommendation
from services.fraud.fraud_rules import basic_fraud_checks
from services.fraud.anomaly_check import anomaly_detection
from services.explainable.explain_risk import generate_risk_explanation


def run_smart_assessment(user_input, risk_score=50, esg_score=50):
    """
    Central intelligence layer.
    Combines all NEW features.
    DOES NOT modify current app logic.
    Works as an add-on module.
    """

    # 1️⃣ alternative data
    alt_profile = build_alt_data_profile(user_input)

    # 2️⃣ climate intelligence
    climate_profile = build_climate_profile(user_input)

    # 3️⃣ fraud detection
    fraud_flags = basic_fraud_checks(user_input)
    anomaly_flag = anomaly_detection(user_input)

    # 4️⃣ smart loan recommendation
    recommendation = generate_loan_recommendation(user_input, risk_score)

    # 5️⃣ explainable insights
    explanation = generate_risk_explanation(
        risk_score=risk_score,
        esg_score=esg_score,
        alt_data_score=alt_profile["alt_data_confidence"],
        climate_score=climate_profile["overall_climate_risk"]
    )

    return {
        "alt_data_profile": alt_profile,
        "climate_profile": climate_profile,
        "fraud_alerts": fraud_flags,
        "anomaly_result": anomaly_flag,
        "loan_recommendation": recommendation,
        "explainable_output": explanation
    }