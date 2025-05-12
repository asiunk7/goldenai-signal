from flask import Flask, request, jsonify

@app.route("/signal", methods=["POST"])
def signal():
    global last_limit, last_instant, last_time
    now = time.time()

    # Ambil harga dari JSON body EA
    data = request.get_json()
    if not data or "price" not in data:
        return jsonify({"error": "Missing price"}), 400

    current_price = float(data["price"])

    if not last_limit or now - last_time > 1800:
        last_limit = generate_signal(current_price=current_price)
        last_instant = generate_signal(direction=last_limit["direction"], current_price=current_price)
        last_instant["entry"] = round(last_limit["entry"] + random.uniform(-0.5, 0.5), 3)
        last_instant["winrate"] = round(last_limit["winrate"] - random.uniform(0.5, 2.0), 1)
        last_time = now

    return jsonify({
        "limit": last_limit,
        "instant": last_instant
    })

