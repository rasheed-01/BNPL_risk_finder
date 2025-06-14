from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_risk_score(purchase_amount, past_fraud_reports, social_score):
    score = 0

    if purchase_amount > 1000:
        score += 40
    elif purchase_amount > 500:
        score += 25
    else:
        score += 10

    score += past_fraud_reports * 20

    if social_score > 80:
        score -= 20
    elif social_score < 40:
        score += 20

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
        "decision": decision
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
