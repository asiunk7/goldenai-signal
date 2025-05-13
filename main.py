from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/price", methods=["POST"])
def receive_price():
    data = request.get_json()
    print("Received price:", data)
    return jsonify({"status": "received"}), 200
    except Exception as e:
        print("❌ Error parsing JSON:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/signal", methods=["POST"])
def send_signal():
    data = request.get_json()
    if not data:
        return jsonify({}), 400

    # Ambil data candle
    candle1 = data.get("candle1", {})
    candle2 = data.get("candle2", {})
    atr = float(data.get("atr", 0))
    rsi = float(data.get("rsi", 50))

    open1 = candle1.get("open", 0)
    close1 = candle1.get("close", 0)
    high1 = candle1.get("high", 0)
    low1 = candle1.get("low", 0)

    # Validasi candle impuls dan kondisi RSI
    min_range = 2.0  # candle min 2 point
    body = abs(close1 - open1)
    direction = None

    if body >= min_range:
        if close1 > open1 and rsi < 70:
            direction = "BUY"
        elif close1 < open1 and rsi > 30:
            direction = "SELL"

    if not direction:
        return jsonify({})  # no signal

    buffer = atr * 0.5
    entry = high1 + buffer if direction == "BUY" else low1 - buffer
    sl = low1 - atr if direction == "BUY" else high1 + atr
    tp = entry + (entry - sl) * 1.5 if direction == "BUY" else entry - (sl - entry) * 1.5

    # Estimasi winrate dummy (optional)
    rr = abs(tp - entry) / abs(entry - sl)
    winrate = min(95, max(60, 60 + (rr - 1.0) * 10))

    return jsonify({
        "direction": direction,
        "entry": round(entry, 3),
        "sl": round(sl, 3),
        "tp": round(tp, 3),
        "winrate": round(winrate, 1)
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
