from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import os
from push_to_github import push_signal_to_github

app = Flask(__name__)
latest_data = {}

@app.route('/price', methods=['POST'])
def price():
    global latest_data
    latest_data = request.get_json(force=True)
    return jsonify({"status": "received"})

@app.route('/signal', methods=['GET'])
def signal():
    if not latest_data:
        return jsonify({"status": "error", "message": "no price data"})

    now = datetime.utcnow()
    expired = (now.replace(second=0, microsecond=0) + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

    signal_data = {
        "instant": {
            "direction": "SELL",
            "entry": 3210,
            "sl": 3235,
            "tp": 3180,
            "winrate": 60
        },
        "limit": {
            "direction": "BUY",
            "entry": 3190,
            "sl": 3165,
            "tp": 3225,
            "winrate": 70
        },
        "status": "success",
        "expired": expired
    }

    with open("signal.json", "w") as f:
        json.dump(signal_data, f, indent=2)

    push_signal_to_github("signal.json")
    return jsonify(signal_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
