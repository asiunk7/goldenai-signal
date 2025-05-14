from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/price', methods=['POST'])
def receive_price():
    data = request.get_json(force=True)
    print("Received price data:", data)
    return jsonify({"status": "received"})

@app.route('/signal', methods=['GET'])
def send_signal():
    now = datetime.utcnow()
    # Atur expired ke akhir candle M30 saat ini
    minute = now.minute
    next_half_hour = 30 if minute < 30 else 60
    expired_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=next_half_hour)

    # Contoh sinyal realistis (SELL)
    signal = {
        "status": "success",
        "instant": {
            "direction": "SELL",
            "entry": 3195.170,
            "sl": 3204.900,
            "tp": 3181.370,
            "winrate": 78.3,
            "expired": expired_time.strftime('%Y-%m-%d %H:%M:%S')
        },
        "limit": {
            "direction": "SELL",
            "entry": 3195.170,
            "sl": 3204.900,
            "tp": 3181.370,
            "winrate": 78.3,
            "expired": expired_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    return jsonify(signal)

if __name__ == '__main__':
    app.run(debug=True, port=10000)
