from flask import Flask, request, jsonify
import random, time

app = Flask(__name__)
last_signal = None
last_time = 0

def generate_signal(struct):
    direction = "SELL" if struct["candle1"]["close"] < struct["candle1"]["open"] else "BUY"
    base = struct["candle1"]["close"]

    if direction == "BUY":
        entry = round(base - random.uniform(1.0, 2.5), 3)
        sl = round(entry - random.uniform(2.0, 4.0), 3)
        tp = round(entry + random.uniform(3.5, 6.0), 3)
    else:
        entry = round(base + random.uniform(1.0, 2.5), 3)
        sl = round(entry + random.uniform(2.0, 4.0), 3)
        tp = round(entry - random.uniform(3.5, 6.0), 3)

    winrate = round(random.uniform(78, 92), 1)

    return {
        "direction": direction,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "symbol": "XAUUSD",
        "winrate": winrate
    }

@app.route("/signal", methods=["POST"])
def signal():
    global last_signal, last_time
    struct = request.get_json()
    now = time.time()

    if last_signal is None or now - last_time > 1800:
        limit = generate_signal(struct)
        instant = limit.copy()
        instant["entry"] = round(limit["entry"] + random.uniform(-0.2, 0.2), 3)
        instant["winrate"] = round(limit["winrate"] - random.uniform(0.3, 1.0), 1)

        last_signal = {
            "limit": limit,
            "instant": instant
        }
        last_time = now

    return jsonify(last_signal)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


