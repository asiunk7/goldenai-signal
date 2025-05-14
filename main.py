from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
latest_data = {}

@app.route('/price', methods=['POST'])
def receive_price():
    global latest_data
    data = request.get_json(force=True)
    latest_data = data
    print("✅ Received price data:", data)
    return jsonify({"status": "received"})

@app.route('/signal', methods=['GET'])
def send_signal():
    global latest_data

    # Validasi input
    if not all(k in latest_data for k in ("candle1", "candle2", "candle3")):
        return jsonify({"status": "error", "message": "not enough candle data"}), 400

    def parse(c):
        return {
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"])
        }

    c1 = parse(latest_data["candle1"])  # candle sekarang
    c2 = parse(latest_data["candle2"])  # candle impuls
    c3 = parse(latest_data["candle3"])  # struktur swing

    # Hitung struktur
    body2 = abs(c2["close"] - c2["open"])
    wick2_top = c2["high"] - max(c2["close"], c2["open"])
    wick2_bot = min(c2["close"], c2["open"]) - c2["low"]

    isBullImpulse = (c2["close"] > c2["open"]) and (body2 > wick2_top * 2 and body2 > wick2_bot * 2)
    isBearImpulse = (c2["open"] > c2["close"]) and (body2 > wick2_top * 2 and body2 > wick2_bot * 2)

    # Cek pullback valid (c1 berlawanan arah impuls)
    pullback_buy = isBullImpulse and (c1["close"] < c1["open"])
    pullback_sell = isBearImpulse and (c1["close"] > c1["open"])

    # Buat sinyal jika valid
    if pullback_buy:
        entry = round(c1["high"] + 2, 3)
        sl = round(c2["low"] - 5, 3)
        tp = round(entry + (entry - sl) * 1.5, 3)
        rr = round((tp - entry) / (entry - sl), 2)
        direction = "BUY"
        winrate = 74.6

    elif pullback_sell:
        entry = round(c1["low"] - 2, 3)
        sl = round(c2["high"] + 5, 3)
        tp = round(entry - (sl - entry) * 1.5, 3)
        rr = round((entry - tp) / (sl - entry), 2)
        direction = "SELL"
        winrate = 77.8

    else:
        return jsonify({"status": "error", "message": "no valid setup"}), 200

    # Filter sinyal jika RR kecil
    if rr < 1.2:
        return jsonify({"status": "error", "message": "RR too small"}), 200

    # Hitung expired ke akhir M30
    now = datetime.utcnow()
    next_half = 30 if now.minute < 30 else 60
    expired = now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=next_half)

    signal = {
        "status": "success",
        "instant": {
            "direction": direction,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "winrate": winrate,
            "expired": expired.strftime('%Y-%m-%d %H:%M:%S')
        },
        "limit": {
            "direction": direction,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "winrate": winrate,
            "expired": expired.strftime('%Y-%m-%d %H:%M:%S')
        }
    }

    return jsonify(signal)

if __name__ == '__main__':
    app.run(debug=True, port=10000)
