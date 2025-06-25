from flask import Flask, request, jsonify
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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
