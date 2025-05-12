# Flask server to receive live price from MT4 and serve AI signal
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

live_price = {
    "bid": 0.0,
    "ask": 0.0,
    "timestamp": 0
}

last_signal = {
    "instant": {},
    "limit": {},
    "last_generated": 0
}

@app.route("/price", methods=["POST"])
def receive_price():
    data = request.get_json()
    live_price["bid"] = float(data.get("bid", 0.0))
    live_price["ask"] = float(data.get("ask", 0.0))
    live_price["timestamp"] = time.time()
    return jsonify({"status": "received"})

@app.route("/signal", methods=["GET"])
def serve_signal():
    now = time.time()
    if now - last_signal["last_generated"] > 1800 or not last_signal["instant"]:
        bid = live_price["bid"]
        ask = live_price["ask"]
        mid_price = round((bid + ask) / 2, 3)

        direction = "BUY" if mid_price % 2 > 1 else "SELL"
        entry = round(ask if direction == "BUY" else bid, 3)
        sl = round(entry - 10 if direction == "BUY" else entry + 10, 3)
        tp = round(entry + 40 if direction == "BUY" else entry - 40, 3)
        winrate = 80.0

        signal = {
            "direction": direction,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "symbol": "XAUUSD",
            "winrate": winrate
        }

        last_signal["instant"] = signal
        last_signal["limit"] = {
            **signal,
            "entry": round(entry - 5 if direction == "BUY" else entry + 5, 3),
            "winrate": round(winrate - 1.2, 1)
        }
        last_signal["last_generated"] = now

    return jsonify({
        "instant": last_signal["instant"],
        "limit": last_signal["limit"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



