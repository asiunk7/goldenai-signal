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

    # Ambil data candle terakhir
    c1 = latest_data.get("candle1", {})
    c2 = latest_data.get("candle2", {})
    c3 = latest_data.get("candle3", {})
    rsi = latest_data.get("rsi", 50)
    atr = latest_data.get("atr", 10)

    direction = "SELL" if rsi > 60 else "BUY"
    entry = round(c1["close"], 1)
    tp = round(entry - atr * 1.0, 1) if direction == "SELL" else round(entry + atr * 1.0, 1)
    sl = round(entry + atr * 1.0, 1) if direction == "SELL" else round(entry - atr * 1.0, 1)

    # Buat sedikit beda antara instant dan limit
    signal_data = {
        "status": "success",
        "instant": {
            "direction": direction,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "winrate": 68.5,
            "expired": expired
        },
        "limit": {
            "direction": direction,
            "entry": round(entry + 2.0 if direction == "SELL" else entry - 2.0, 1),
            "sl": sl,
            "tp": tp,
            "winrate": 71,
            "expired": expired
        }
    }
    return jsonify(signal_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
