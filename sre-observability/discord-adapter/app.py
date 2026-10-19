import os

import requests

from flask import Flask, jsonify, request

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()

if not DISCORD_WEBHOOK_URL:
    raise RuntimeError(
        "Required environment variable DISCORD_WEBHOOK_URL is not set"
    )


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/webhook")
def webhook():
    if not DISCORD_WEBHOOK_URL:
        return jsonify({"error": "Discord webhook not configured"}), 500

    payload = request.get_json(silent=True) or {}
    alerts = payload.get("alerts", [])

    if not alerts:
        return jsonify({"status": "No alerts to send"}), 200

    messages = []

    for alert in alerts:
        status = alert.get("status", "unknown").upper()
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        name = labels.get("alertname", "Unnamed alert")
        severity = labels.get("severity", "unspecified")
        summary = annotations.get("summary", "No summary provided")
        description = annotations.get("description")

        message = (
            f"**{status}: {name}**\n"
            f"**Severity:** {severity}\n"
            f"{summary}\n"
            f"{description}"
        )

        messages.append(message)

    for message in messages:
        try:
            response = requests.post(
                DISCORD_WEBHOOK_URL,
                json={"content": message[:2000]},
                timeout=10,
            )
            response.raise_for_status
        except requests.exceptions.Timeout:
            app.logger.error("Timeout while sendind notification to Discord")
            return jsonify({"error": "Discord request timed out"}), 504
        except requests.exceptions.RequestException:
            app.logger.exception("Failed to send notification to Discord")
            return (
                jsonify({"error": "Failed to send notification to Discord"}),
                502,
            )

    return jsonify({"status": "sent", "count": len(messages)}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
