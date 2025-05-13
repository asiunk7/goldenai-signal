from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/price", methods=["POST"])
def receive_price():
    data = request.get_json()
    print("Received price:", data)
    return jsonify({"status": "received"}), 200

@app.route("/signal", methods=["POST"])
def send_signal():
    market_data = request.get_json()
    print("Received signal request:", market_data)

    return jsonify({
        "direction": "BUY",
        "entry": 3225.123,
        "sl": 3215.456,
        "tp": 3240.789,
        "winrate": 78.9
    }), 200
