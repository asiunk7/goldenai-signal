from flask import Flask, jsonify
import random

app = Flask(__name__)

def generate_signal(direction=None):
    if not direction:
        direction = random.choice(["BUY", "SELL"])
        
    base_price = round(random.uniform(3200, 3300), 3)

    if direction == "BUY":
        entry = base_price
        sl = round(entry - random.uniform(5, 10), 3)
        tp = round(entry + random.uniform(20, 40), 3)
    else:
        entry = base_price
        sl = round(entry + random.uniform(5, 10), 3)
        tp = round(entry - random.uniform(20, 40), 3)

    winrate = round(random.uniform(70, 95), 1)

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
    # Buat sinyal utama (limit)
    limit_signal = generate_signal()

    # Instant = versi modifikasi dari sinyal yang sama, entry-nya sedikit lebih dekat ke harga real
    instant_signal = generate_signal(direction=limit_signal["direction"])
    instant_signal["entry"] = round(limit_signal["entry"] + random.uniform(-0.5, 0.5), 3)
    instant_signal["winrate"] = round(limit_signal["winrate"] - random.uniform(0.5, 2.0), 1)

    return jsonify({
        "limit": limit_signal,
        "instant": instant_signal
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
