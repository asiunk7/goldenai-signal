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

        # Validasi
        required_keys = ["symbol", "tf", "candle1", "candle2", "atr", "rsi"]
        for key in required_keys:
            if key not in market_data:
                return jsonify({"error": f"Missing field: {key}"}), 400

        # Struktur candle
        c1 = market_data["candle1"]
        c2 = market_data["candle2"]
        rsi = market_data["rsi"]
        atr = market_data["atr"]
        symbol = market_data["symbol"]

        # Logika sinyal instant
        if c1["close"] > c1["open"] and c1["close"] > c2["close"] and rsi < 70:
            instant = {
                "direction": "BUY",
                "entry": round(c1["close"], 3),
                "sl": round(c1["low"] - atr, 3),
                "tp": round(c1["close"] + atr * 2, 3),
                "winrate": 80.0
            }
        elif c1["close"] < c1["open"] and c1["close"] < c2["close"] and rsi > 30:
            instant = {
                "direction": "SELL",
                "entry": round(c1["close"], 3),
                "sl": round(c1["high"] + atr, 3),
                "tp": round(c1["close"] - atr * 2, 3),
                "winrate": 80.0
            }
        else:
            instant = None

        # Logika sinyal limit
        limit = {
            "direction": "SELL",
            "entry": round(c1["high"] + atr * 0.5, 3),
            "sl": round(c1["high"] + atr * 1.5, 3),
            "tp": round(c1["low"], 3),
            "winrate": 70.0
        }

        return jsonify({
            "instant": instant,
            "limit": limit
        })

    except Exception as e:
        print("❌ Error parsing signal JSON:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Golden AI Signal Server is running ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
