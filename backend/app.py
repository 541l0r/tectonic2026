"""Small mock API; replace the response engine after the challenge is known."""

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/api/health")
def health():
    return jsonify(status="ok", source="mock")


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Expected a JSON object"), 400

    message = payload.get("message")
    if not isinstance(message, str) or not message.strip() or len(message) > 2000:
        return jsonify(error="message must be 1–2000 characters"), 400

    if payload.get("user_id", "demo") != "demo":
        return jsonify(error="Only the demo user is available"), 400

    return jsonify(
        answer="Your spending is up in groceries this month.",
        blocks=[
            {"type": "metric", "label": "Groceries", "value": "€420", "detail": "+€60 vs previous month"},
            {"type": "list", "title": "Possible next steps", "items": ["Review recent grocery purchases", "Set a monthly alert"]},
        ],
        source="mock",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
