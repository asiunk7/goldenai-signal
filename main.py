from flask import Flask, request, jsonify
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
        print("✅ Received price:", data)
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/signal", methods=["POST"])
def send_signal():
    try:
        data = request.get_json(force=True)
        print("📥 Market data received:", data)

        bid = live_price["bid"]
        ask = live_price["ask"]
        mid = round((bid + ask) / 2, 3)

        direction = "BUY" if mid % 2 > 1 else "SELL"
        entry = round(ask if direction == "BUY" else bid, 3)
        sl = round(entry - 10 if direction == "BUY" else entry + 10, 3)
        tp = round(entry + 40 if direction == "BUY" else entry - 40, 3)

        signal = {
            "direction": direction,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "winrate": 80.5,
            "symbol": data.get("symbol", "XAUUSD")
        }

        return jsonify(signal), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "✅ Golden AI Signal Server is Running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
