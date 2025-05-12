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

    if not last_limit or now - last_time > 1800:
        # Limit signal
        last_limit = generate_signal()
        
        # Instant signal: entry = simulated real price
        current_price = round(random.uniform(3190, 3310), 3)
        dir_factor = 1 if last_limit["direction"] == "BUY" else -1

        entry = current_price
        tp = round(entry + dir_factor * random.uniform(20, 35), 3)
        sl = round(entry - dir_factor * random.uniform(8, 12), 3)
        winrate = round(last_limit["winrate"] - random.uniform(1.0, 3.0), 1)

        last_instant = {
            "direction": last_limit["direction"],
            "entry": float(f"{entry:.3f}"),
            "sl": float(f"{sl:.3f}"),
            "tp": float(f"{tp:.3f}"),
            "winrate": winrate,
            "symbol": "XAUUSD"
        }

        last_time = now

    return jsonify({
        "limit": last_limit,
        "instant": last_instant
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

