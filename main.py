from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/signal', methods=['GET'])
def signal():
    return jsonify({
        "symbol": "XAUUSD",
        "entry": 3225.834,
        "sl": 3234.248,
        "tp": 3198.621,
        "direction": "SELL",
        "winrate": 81.2
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
