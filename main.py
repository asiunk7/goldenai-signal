from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/price", methods=["POST"])
def receive_price():
    try:
        data = request.get_json(force=True)
        print("✅ Received price:", data)
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("❌ Error parsing price JSON:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/signal", methods=["POST"])
def send_signal():
    try:
        market_data = request.get_json(force=True)
        print("📥 Received signal request:", market_data)

        required_keys = ["symbol", "tf", "candle1", "candle2", "atr", "rsi"]
        for key in required_keys:
            if key not in market_data:
                return jsonify({"error": f"Missing field: {key}"}), 400

        # Contoh logic sinyal realistik
        entry_now = float(market_data["candle1"]["close"])
        atr = float(market_data["atr"])
        direction = "BUY" if float(market_data["rsi"]) < 50 else "SELL"

        sl = entry_now - atr if direction == "BUY" else entry_now + atr
        tp = entry_now + atr * 2 if direction == "BUY" else entry_now - atr * 2

        return jsonify({
            "direction": direction,
            "entry": round(entry_now, 3),
            "sl": round(sl, 3),
            "tp": round(tp, 3),
            "winrate": 78.9
        }), 200

    except Exception as e:
        print("❌ Error parsing signal JSON:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def home():
    return "✅ Golden AI Signal Server aktif", 200

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)
