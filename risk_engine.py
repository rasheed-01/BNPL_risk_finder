from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_risk_score(purchase_amount, past_fraud_reports, social_score):
    score = 0
    explanation_parts = []

    if purchase_amount > 1000:
        score += 40
        explanation_parts.append("High purchase amount increased the risk significantly.")
    elif purchase_amount > 500:
        score += 25
        explanation_parts.append("Moderately high purchase amount increased the risk.")
    else:
        score += 10
        explanation_parts.append("Low purchase amount had minimal impact on risk.")

    if past_fraud_reports > 0:
        fraud_score = past_fraud_reports * 20
        score += fraud_score
        explanation_parts.append(f"{past_fraud_reports} past fraud report(s) added significant risk.")

    if social_score > 80:
        score -= 20
        explanation_parts.append("High social trust score reduced the risk.")
    elif social_score < 40:
        score += 20
        explanation_parts.append("Low social trust score increased the risk.")
    else:
        explanation_parts.append("Average social trust score had neutral impact.")

    score = max(0, min(100, score))

    if score < 30:
        grade = "Low"
        decision = "Approved"
    elif score < 70:
        grade = "Medium"
        decision = "Approved with caution"
    else:
        grade = "High"
        decision = "Rejected"

    return {
        "score": score,
        "grade": grade,
        "decision": decision,
        "explanation": " ".join(explanation_parts)
    }

@app.route("/risk", methods=["POST"])
def risk():
    data = request.json
    result = calculate_risk_score(
        data.get("purchase_amount", 0),
        data.get("past_fraud_reports", 0),
        data.get("social_score", 50)
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5001)
