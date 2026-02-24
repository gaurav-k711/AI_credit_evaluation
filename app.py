# ---------------- IMPORTS ----------------
from flask import Flask, request, jsonify, render_template, session, redirect
from database.db import get_db_connection
from database.models import create_tables, create_user_table
from services.integration_engine import run_smart_assessment

# ---------------- APP INITIALIZATION ----------------
app = Flask(__name__)
app.secret_key = "credit_risk_secret_key"
API_TOKEN = "secure-credit-api-123"

# ---------------- DATABASE INIT ----------------
create_tables()
create_user_table()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "AI Credit Evaluation API is running"

# ---------------- MAIN APP ----------------
@app.route("/app")
def main_app():
    if "username" not in session:
        return redirect("/login")
    return render_template("base.html")

# ---------------- DYNAMIC PAGE LOADER ----------------
@app.route("/page/<name>")
def load_page(name):

    # ---------- FORM PAGE ----------
    if name == "form":
        return render_template("components/form.html")

    # ---------- DASHBOARD ----------
    if name == "dashboard":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loan_applications ORDER BY id DESC")
        applications = cursor.fetchall()
        conn.close()

        smart_preview = session.get("latest_smart_ai", {
            "alt_data_confidence": 0,
            "climate_risk": 0,
            "fraud_flag": "No data",
            "recommended_loan": 0
        })

        explain_data = session.get("explain_ai", {})

        return render_template(
            "components/dashboard.html",
            applications=applications,
            smart_preview=smart_preview,
            explain_data=explain_data
        )

    # ---------- ANALYTICS ----------
    if name == "analytics":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT decision, COUNT(*) as count
            FROM loan_applications
            GROUP BY decision
        """)
        decision_data = cursor.fetchall()
        conn.close()

        return render_template(
            "components/analytics.html",
            decision_data=decision_data
        )

    return "<h3>Page not found</h3>"

# ---------------- AUTH ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        session["username"] = username
        session["role"] = user["role"]
        return redirect("/app")

    return render_template("login.html", error="Invalid credentials")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- MAIN CREDIT ENGINE ----------------
@app.route("/predict", methods=["POST"])
def predict():

    # ---------- API SECURITY ----------
    if request.headers.get("X-API-KEY") != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    # ---------- ESG FLAGS ----------
    women_led = bool(data.get("womenLed", False))
    organic_farm = bool(data.get("organicFarm", False))
    small_farmer = bool(data.get("smallFarmer", False))

    # ---------- FIELD EXTRACTION ----------
    business_type = data.get("business_type", "Unknown")
    credit_score = int(data.get("credit_score", 0))
    dti = float(data.get("debt_to_income_ratio", 1))
    loan_amount = float(data.get("loan_amount_requested", 0))
    annual_revenue = float(data.get("annual_revenue", 0))

    # ---------- CARD BENEFITS ----------
    kisan_card = bool(data.get("kisanCard", False))
    soil_card = bool(data.get("soilCard", False))
    insurance_card = bool(data.get("insuranceCard", False))
    rupay_card = bool(data.get("rupayCard", False))

    # ---------- BASE DECISION ----------
    if credit_score >= 700 and dti < 0.4 and loan_amount < annual_revenue:
        decision = "APPROVE"
        risk_score = 20
        confidence = "High"
    elif credit_score >= 600:
        decision = "REVIEW"
        risk_score = 50
        confidence = "Medium"
    else:
        decision = "REJECT"
        risk_score = 80
        confidence = "Low"

    # ---------- CARD ENGINE ----------
    if kisan_card:
        risk_score -= 10
    if soil_card:
        risk_score -= 5
    if rupay_card:
        risk_score -= 3
    if insurance_card and confidence == "Medium":
        confidence = "High"

    # ---------- ESG ENGINE ----------
    impact_score = 50

    if women_led:
        impact_score += 20
        confidence = "High"

    if organic_farm:
        impact_score += 15
        risk_score -= 5

    if small_farmer:
        impact_score += 15
        if decision == "REVIEW":
            decision = "APPROVE"

    risk_score = max(5, min(risk_score, 95))
    impact_score = max(0, min(impact_score, 100))

    # ---------- CREDIT LIMIT ----------
    recommended_limit = annual_revenue * 0.4

    if confidence == "High":
        recommended_limit *= 1.2
    if risk_score > 60:
        recommended_limit *= 0.7
    if impact_score >= 80:
        recommended_limit *= 1.1

    recommended_limit = round(recommended_limit, 2)

    # ---------- SAVE DATABASE ----------
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO loan_applications
        (business_type, risk_score, decision, confidence)
        VALUES (?, ?, ?, ?)
    """, (
        business_type,
        risk_score,
        decision,
        confidence
    ))
    conn.commit()
    conn.close()

    # ---------- RUN SMART AI ENGINE ----------
    smart_input = {
        "phone": data.get("phone", "NA"),
        "upi_id": data.get("upi_id", "NA"),
        "crop_type": data.get("crop_type", "unknown"),
        "location": data.get("location", "unknown"),
        "annual_income": annual_revenue,
        "loan_amount": loan_amount,
        "previous_applications": 1
    }

    smart_result = run_smart_assessment(smart_input, risk_score, impact_score)

    # ---------- STORE SMART AI ----------
    session["latest_smart_ai"] = {
        "alt_data_confidence": smart_result["alt_data_profile"]["alt_data_confidence"],
        "climate_risk": smart_result["climate_profile"]["overall_climate_risk"],
        "fraud_flag": smart_result["anomaly_result"]["reason"],
        "recommended_loan": smart_result["loan_recommendation"]["recommended_loan_amount"]
    }

    # ---------- APPROVAL REASONING ENGINE ----------
    if decision == "APPROVE":
        final_reason = "Loan approved due to stable income, acceptable risk and strong ESG support."
    elif decision == "REVIEW":
        final_reason = "Application sent for review due to moderate risk or insufficient financial signals."
    else:
        final_reason = "Loan rejected due to high credit risk or weak repayment capacity."

    # ---------- EXPLAINABLE AI ----------
    session["explain_ai"] = {
        "risk_score": risk_score,
        "esg_score": impact_score,
        "income": annual_revenue,
        "loan_requested": loan_amount,
        "decision": decision,
        "confidence": confidence,
        "key_reason": smart_result["anomaly_result"]["reason"],
        "final_reason": final_reason
    }

    # ---------- RESPONSE ----------
    return jsonify({
        "risk_score": risk_score,
        "decision": decision,
        "confidence": confidence,
        "impact_score": impact_score,
        "recommended_limit": recommended_limit
    })

# ---------------- SMART DEMO ROUTE ----------------
@app.route("/smart-assessment", methods=["POST"])
def smart_assessment():
    user_input = request.json
    risk_score = user_input.get("risk_score", 50)
    esg_score = user_input.get("esg_score", 50)

    result = run_smart_assessment(user_input, risk_score, esg_score)
    return jsonify(result)

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)