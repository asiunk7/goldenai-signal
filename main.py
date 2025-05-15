from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
latest_data = {}

@app.route('/price', methods=['POST'])
def price():
    global latest_data
    try:
        latest_data = request.get_json(force=True)
        print("[RECEIVED] /price @", datetime.utcnow(), "->", latest_data)
        return jsonify({"status": "received", "data": latest_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/signal', methods=['GET'])
def signal():
    if not latest_data or "candle1" not in latest_data:
        return jsonify({"status": "error", "message": "no valid price data"})

    # --- Ambil data struktur candle ---
    symbol = latest_data.get("symbol", "XAUUSD")
    tf = latest_data.get("tf", "M30")
    c1 = latest_data.get("candle1", {})
    c2 = latest_data.get("candle2", {})
    c3 = latest_data.get("candle3", {})
    atr = float(latest_data.get("atr", 100.0))
    rsi = float(latest_data.get("rsi", 50.0))

    # --- Struktur candle analisa sederhana (masih simple bisa diimprove) ---
    is_bearish = c1.get("close", 0) < c1.get("open", 0)
    is_bullish = c1.get("close", 0) > c1.get("open", 0)

    now = datetime.utcnow()
    expired = (now.replace(second=0, microsecond=0) + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

    # --- Logika sinyal simple berbasis arah candle dan RSI ---
    if is_bearish and rsi > 65:
        signal = {
            "status": "success",
            "instant": {
                "direction": "SELL",
                "entry": c1["close"],
                "sl": round(c1["high"] + atr, 2),
                "tp": round(c1["close"] - (2 * atr), 2),
                "winrate": 68.5,
                "expired": expired
            },
            "limit": {
                "direction": "SELL",
                "entry": round(c1["close"] + (0.5 * atr), 2),
                "sl": round(c1["high"] + atr, 2),
                "tp": round(c1["close"] - (2 * atr), 2),
                "winrate": 71.0,
                "expired": expired
            }
        }
    elif is_bullish and rsi < 35:
        signal = {
            "status": "success",
            "instant": {
                "direction": "BUY",
                "entry": c1["close"],
                "sl": round(c1["low"] - atr, 2),
                "tp": round(c1["close"] + (2 * atr), 2),
                "winrate": 67.0,
                "expired": expired
            },
            "limit": {
                "direction": "BUY",
                "entry": round(c1["close"] - (0.5 * atr), 2),
                "sl": round(c1["low"] - atr, 2),
                "tp": round(c1["close"] + (2 * atr), 2),
                "winrate": 70.5,
                "expired": expired
            }
        }
    else:
        signal = {
            "status": "error",
            "message": "struktur tidak valid (no signal)"
        }

    print("[RESPONSE] /signal ->", signal)
    return jsonify(signal)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
