from flask import Flask, jsonify
from forex_python.converter import CurrencyRates
import random
import time

app = Flask(__name__)

last_limit = None
last_instant = None
last_time = 0

# Dummy harga realtime - Ganti ini ke harga real-time broker lo kalau butuh
def get_current_price():
    # Bisa diganti dari API harga asli kalau perlu
    return 3246.500  # harga pasar saat ini (kasar)

def generate_signal(direction=None):
    current = get_current_price()

    if not direction:
        direction = random.choice(["BUY", "SELL"])

    if direction == "BUY":
        entry = round(current - 10 + random.uniform(-2, 2), 3)  # limit buy di bawah harga
        sl = round(entry - random.uniform(8, 12), 3)
        tp = round(entry + random.uniform(20, 35), 3)
    else:
        entry = round(current + 10 + random.uniform(-2, 2), 3)  # limit sell di atas harga
        sl = round(entry + random.uniform(8, 12), 3)
        tp = round(entry - random.uniform(20, 35), 3)

    winrate = round(random.uniform(75, 95), 1)

    return {
        "direction": direction,
        "entry": float(f"{entry:.3f}"),
        "sl": float(f"{sl:.3f}"),
        "tp": float(f"{tp:.3f}"),
        "winrate": winrate,
        "symbol": "XAUUSD"
    }

@app.route("/signal", methods=["GET"])
def signal():
    global last_limit, last_instant, last_time
    now = time.time()

    # Ganti sinyal hanya tiap 30 menit
    if not last_limit or now - last_time > 1800:
        last_limit = generate_signal()
        last_instant = generate_signal(direction=last_limit["direction"])

        # Instant entry hanya jika dekat harga market (±2 USD)
        current = get_current_price()
        if last_limit["direction"] == "BUY":
            last_instant["entry"] = round(current + random.uniform(-1.0, 1.0), 3)
        else:
            last_instant["entry"] = round(current + random.uniform(-1.0, 1.0), 3)

        last_instant["winrate"] = round(last_limit["winrate"] - random.uniform(1, 3), 1)
        last_time = now

    return jsonify({
        "instant": last_instant,
        "limit": last_limit
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


