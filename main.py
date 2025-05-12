from flask import Flask, jsonify
import random, time

app = Flask(__name__)

last_limit = None
last_instant = None
last_time = 0

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
    global last_limit, last_instant, last_time
    now = time.time()

    # Refresh sinyal setiap 30 menit
    if not last_limit or now - last_time > 1800:
        last_limit = generate_signal()
        last_instant = generate_signal(direction=last_limit["direction"])
        last_instant["entry"] = round(last_limit["entry"] + random.uniform(-0.5, 0.5), 3)
        last_instant["winrate"] = round(last_limit["winrate"] - random.uniform(0.5, 2.0), 1)
        last_time = now

    return jsonify({
        "limit": last_limit,
        "instant": last_instant
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
