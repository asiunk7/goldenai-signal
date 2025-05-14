from flask import Flask, request, jsonify
from datetime import datetime, timedelta

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

    return jsonify({
        "status": "success",
        "instant": {
            "direction": latest_data.get("instant_direction", "BUY"),
            "entry": latest_data.get("instant_entry", 0),
            "sl": latest_data.get("instant_sl", 0),
            "tp": latest_data.get("instant_tp", 0),
            "winrate": latest_data.get("instant_winrate", 0),
            "expired": expired
        },
        "limit": {
            "direction": latest_data.get("limit_direction", "BUY"),
            "entry": latest_data.get("limit_entry", 0),
            "sl": latest_data.get("limit_sl", 0),
            "tp": latest_data.get("limit_tp", 0),
            "winrate": latest_data.get("limit_winrate", 0),
            "expired": expired
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
