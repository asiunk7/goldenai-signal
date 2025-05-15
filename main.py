from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from openai import OpenAI
import os

app = Flask(__name__)
latest_data = {}

# Inisialisasi client OpenAI versi >= 1.0.0
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/price', methods=['POST'])
def price():
    global latest_data
    latest_data = request.get_json(force=True)
    print("🔥 Received candle data:", latest_data)
    return jsonify({"status": "received"})

@app.route('/signal', methods=['GET'])
def signal():
    if not latest_data:
        return jsonify({"status": "error", "message": "no price data"})

    # Buat prompt yang akan dikirim ke GPT
    prompt = (
        "Kamu adalah AI expert trading. Berdasarkan data berikut, buat sinyal terbaik "
        "(BUY/SELL LIMIT/INSTANT), entry, SL, TP, dan winrate secara masuk akal.\n\n"
        f"Candle1: {latest_data.get('candle1')}\n"
        f"Candle2: {latest_data.get('candle2')}\n"
        f"Candle3: {latest_data.get('candle3')}\n"
        f"ATR: {latest_data.get('atr')}\n"
        f"RSI: {latest_data.get('rsi')}\n\n"
        "Jawaban format JSON:\n"
        "{\n"
        "  \"instant\": {\n"
        "    \"direction\": \"...\",\n"
        "    \"entry\": ...,\n"
        "    \"sl\": ...,\n"
        "    \"tp\": ...,\n"
        "    \"winrate\": ...\n"
        "  },\n"
        "  \"limit\": {\n"
        "    \"direction\": \"...\",\n"
        "    \"entry\": ...,\n"
        "    \"sl\": ...,\n"
        "    \"tp\": ...,\n"
        "    \"winrate\": ...\n"
        "  }\n"
        "}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah AI asisten trading"},
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = response.choices[0].message.content
        return jsonify({"status": "success", "raw": ai_reply})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
