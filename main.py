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

        # Cek jika data wajib tersedia
        required_keys = ["symbol", "tf", "candle1", "candle2", "atr", "rsi"]
        for key in required_keys:
            if key not in market_data:
                return jsonify({"error": f"Missing field: {key}"}), 400

        # (Sementara ini dummy logic untuk testing, nanti bisa diganti ke real signal AI)
        return jsonify({
            "direction": "BUY",
            "entry": 3225.123,
            "sl": 3215.456,
            "tp": 3240.789,
            "winrate": 78.9
        }), 200

    except Exception as e:
        print("❌ Error parsing signal JSON:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Golden AI Signal Server is running ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
