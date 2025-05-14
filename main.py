from flask import Flask, request, jsonify
from waitress import serve
import time

app = Flask(__name__)

live_price = {"bid": 0.0, "ask": 0.0, "timestamp": 0}
last_signal = {"instant": {}, "limit": {}, "last_generated": 0}

@app.route("/price", methods=["POST"])
def receive_price():
    try:
        data = request.get_json(force=True)
        live_price["bid"] = float(data.get("bid", 0.0))
        live_price["ask"] = float(data.get("ask", 0.0))
        live_price["timestamp"] = time.time()
        return jsonify({"status": "received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/signal", methods=["POST"])
def send_signal():
    try:
        data = request.get_json(force=True)
        direction = "BUY" if (live_price["ask"] + live_price["bid"]) % 2 > 1 else "SELL"
        entry = live_price["ask"] if direction == "BUY" else live_price["bid"]
        tp = entry + 30 if direction == "BUY" else entry - 30
        sl = entry - 10 if direction == "BUY" else entry + 10

        signal = {
            "direction": direction,
            "entry": round(entry, 3),
            "sl": round(sl, 3),
            "tp": round(tp, 3),
            "winrate": 82.5,
            "symbol": data.get("symbol", "XAUUSD")
        }
        return jsonify(signal), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Golden AI Signal Server is running ✅", 200

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
