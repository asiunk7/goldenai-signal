from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/signal")
def get_signal():
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

    return jsonify({
        "direction": direction,
        "entry": entry,
        "sl": sl,
        "symbol": "XAUUSD",
        "tp": tp,
        "winrate": winrate
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

