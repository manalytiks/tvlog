from flask import Flask, request, jsonify, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "alerts_live_log.csv"

@app.route("/tvwebhook", methods=["POST"])
def tv_webhook():
    data = request.json
    now = datetime.utcnow().isoformat()
    row = {
        "Time": now,
        "Ticker": data.get("ticker", "UNKNOWN"),
        "Interval": data.get("interval", ""),
        "Description": data.get("alert_message", "")
    }

    try:
        df = pd.read_csv(LOG_FILE)
    except:
        df = pd.DataFrame(columns=row.keys())

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

    return jsonify({"status": "ok", "received": row})

@app.route("/")
def healthcheck():
    return "✅ TradingView Webhook Server Active"

@app.route("/alerts", methods=["GET"])
def download_csv():
    if os.path.exists(LOG_FILE):
        return send_file(LOG_FILE, as_attachment=True)
    else:
        return "No alert log found.", 404

@app.route("/alerts/json", methods=["GET"])
def return_json():
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        return jsonify(df.to_dict(orient="records"))
    else:
        return jsonify([])

@app.route("/enrich", methods=["POST"])
def enrich_alerts():
    return jsonify({"status": "placeholder", "message": "Enrichment logic will go here."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000, but Render sets PORT
    app.run(host="0.0.0.0", port=port)
