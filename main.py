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
        market = request.get_json(force=True)
        print("📥 Received market data:", market)

        # Ambil candle dan data indikator
        c1 = market["candle1"]
        c2 = market["candle2"]
        rsi = float(market["rsi"])
        atr = float(market["atr"])
        symbol = market["symbol"]
        tf = market["tf"]

        bid = float(market.get("bid", 0))
        ask = float(market.get("ask", 0))
        spread = abs(ask - bid)

        # ================================
        # LOGIC INSTANT SIGNAL
        # ================================
        instant_direction = None
        if c1["close"] > c1["open"] and rsi < 70:  # Bullish + RSI tidak overbought
            instant_direction = "BUY"
        elif c1["close"] < c1["open"] and rsi > 30:  # Bearish + RSI tidak oversold
            instant_direction = "SELL"

        # Atur RR: TP 2x SL
        sl_buffer = atr * 1.2
        tp_buffer = atr * 2.4

        if instant_direction == "BUY":
            instant_entry = ask
            instant_sl = ask - sl_buffer
            instant_tp = ask + tp_buffer
        elif instant_direction == "SELL":
            instant_entry = bid
            instant_sl = bid + sl_buffer
            instant_tp = bid - tp_buffer
        else:
            instant_entry = instant_sl = instant_tp = 0

        # ================================
        # LOGIC LIMIT SIGNAL
        # ================================
        limit_direction = instant_direction  # ikut arah instant
        if limit_direction == "BUY":
            limit_entry = c1["low"] - spread * 1.5
            limit_sl = limit_entry - sl_buffer
            limit_tp = limit_entry + tp_buffer
        elif limit_direction == "SELL":
            limit_entry = c1["high"] + spread * 1.5
            limit_sl = limit_entry + sl_buffer
            limit_tp = limit_entry - tp_buffer
        else:
            limit_entry = limit_sl = limit_tp = 0

        # ================================
        # Output Response
        # ================================
        response = {
            "instant": {
                "direction": instant_direction,
                "entry": round(instant_entry, 3),
                "sl": round(instant_sl, 3),
                "tp": round(instant_tp, 3),
                "winrate": 78.5
            },
            "limit": {
                "direction": limit_direction,
                "entry": round(limit_entry, 3),
                "sl": round(limit_sl, 3),
                "tp": round(limit_tp, 3),
                "winrate": 82.1
            }
        }
        return jsonify(response), 200

    except Exception as e:
        print("❌ Error in /signal logic:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Golden AI Smart Signal Server ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
