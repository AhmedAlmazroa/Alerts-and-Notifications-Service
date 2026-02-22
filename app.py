# app.py
# Alerts & Notifications Microservice (REST API + JSON)
#
# Endpoints:
#   POST /alerts        - Send an alert (deadline, system condition, reminder)
#   GET  /health        - Health check
#
# Response format:
#   Success: { "status": "sent", "alert": { ... } }
#   Error:   { "status": "error", "message": "..." }

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory alert storage (simple for assignment requirements)
alerts_db = []

# Static API key for authentication
VALID_API_KEY = "TEST_API_KEY"


# -------------------------
# Helper functions
# -------------------------

def json_success(data, http_status=200):
    """Return a standardized success response."""
    return jsonify({"status": "sent", **data}), http_status


def json_error(message, http_status):
    """Return a standardized error response."""
    return jsonify({"status": "error", "message": message}), http_status


def validate_api_key():
    """Check Authorization header for a valid API key."""
    auth = request.headers.get("Authorization", "")
    return auth == f"Bearer {VALID_API_KEY}"


# -------------------------
# Routes
# -------------------------

@app.get("/health")
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "ok", "message": "Alerts service running"}), 200


@app.post("/alerts")
def send_alert():
    """Send an alert notification."""
    # 1. Validate API key
    if not validate_api_key():
        return json_error("Unauthorized", 401)

    # 2. Parse JSON body
    data = request.get_json(silent=True) or {}

    required_fields = ["userId", "alertType", "message", "priority", "eventId"]

    # 3. Validate required fields
    if not all(field in data for field in required_fields):
        return json_error("Missing required alert information.", 400)

    # 4. Prevent duplicate alerts for the same eventId
    for alert in alerts_db:
        if alert["eventId"] == data["eventId"]:
            return jsonify({"status": "sent", "message": "Duplicate ignored"}), 200

    # 5. Store alert
    alerts_db.append(data)

    # 6. Return success response
    return json_success({"alert": data}, 200)


# -------------------------
# Start server
# -------------------------
if __name__ == "__main__":
    app.run(port=5001, debug=True)
