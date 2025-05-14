from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Simpan data terakhir dari EA
latest_data = {}

@app.route('/price', methods=['POST'])
def receive_price():
    global latest_data
    data = request.get_json(force=True)
    latest_data = data  # Simpan data terakhir yang dikirim EA
    print("📥 Received price data:", data)
    return jsonify({"status": "received"})

@app.route('/signal', methods=['GET'])
def send_signal():
    global latest_data

    if not latest_data:
        return jsonify({"status": "error", "message": "no data received yet"}), 400

    # Ambil harga terakhir dan hitung entry/SL/TP berdasarkan struktur pasar
    try:
        close_price = float(latest_data["candle1"]["close"])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    # Logic sederhana contoh SELL signal (struktur bisa diimprove)
    entry = round(close_price + 10, 3)
    sl = round(entry + 10, 3)
    tp = round(close_price - 15, 3)
    winrate = 78.3

    # Expired = akhir candle M30
    now = datetime.utcnow()
    next_half = 30 if now.minute < 30 else 60
    expired_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=next_half)

    response = {
        "status": "success",
        "instant": {
            "direction": "SELL",
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "winrate": winrate,
            "expired": expired_time.strftime('%Y-%m-%d %H:%M:%S')
        },
        "limit": {
            "direction": "SELL",
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "winrate": winrate,
            "expired": expired_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=10000)
