def anomaly_detection(user_input):
    """
    Detect abnormal patterns.
    Placeholder for ML later.
    """

    applications_count = user_input.get("previous_applications", 0)

    if applications_count > 5:
        return {
            "fraud_risk": True,
            "reason": "Too many repeated loan attempts"
        }

    return {
        "fraud_risk": False,
        "reason": "Normal behaviour"
    }