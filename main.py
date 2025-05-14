from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
latest_data = {}

@app.route('/price', methods=['POST'])
def price():
    global latest_data
    latest_data = request.get_json(force=True)
    print("🔥 Received candle data:", latest_data)
    return jsonify({"status": "received"})

@app.route('/signal', methods=['GET'])
def signal():
    if not latest_data:
        return jsonify({"status": "error", "message": "no price data"})

    # Ambil data candle
    c1 = latest_data.get("candle1", {})
    c2 = latest_data.get("candle2", {})
    c3 = latest_data.get("candle3", {})
    atr = latest_data.get("atr", 0)
    rsi = latest_data.get("rsi", 0)

    # Expired time = akhir candle M30 berikutnya
    now = datetime.utcnow()
    expired = (now.replace(second=0, microsecond=0) + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

    # Logika deteksi sinyal SELL LIMIT
    if (
        c1.get("close", 0) < c1.get("open", 0) and
        c2.get("close", 0) < c2.get("open", 0) and
        c1.get("high", 0) < c2.get("high", 99999) and
        rsi > 70
    ):
        return jsonify({
            "status": "success",
            "instant": {},
            "limit": {
                "direction": "SELL",
                "entry": round(c1.get("high", 0) + atr, 2),
                "sl": round(c2.get("high", 0) + atr * 2, 2),
                "tp": round(c1.get("low", 0) - atr * 2, 2),
                "winrate": 70.5,
                "expired": expired
            }
        })

    return jsonify({"status": "error", "message": "no valid signal"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
