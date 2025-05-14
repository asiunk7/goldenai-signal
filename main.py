import os
import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv
import openai

# Load API key dari .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

app = Flask(__name__)
latest_data = {}

@app.route('/price', methods=['POST'])
def receive_price():
    global latest_data
    latest_data = request.get_json(force=True)
    print("✅ Price data received:", latest_data)
    return jsonify({"status": "received"})

@app.route('/signal', methods=['GET'])
def send_signal():
    global latest_data

    if not latest_data:
        return jsonify({"status": "error", "message": "no price data"}), 400

    prompt = build_prompt(latest_data)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional forex analyst. Given candle data, suggest best trade (BUY/SELL), entry, SL, TP, and winrate. Respond in JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return jsonify(json.loads(answer))  # ✅ safer than eval
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def build_prompt(data):
    # Hitung expired otomatis ke akhir candle M30
    now = datetime.utcnow()
    next_half = 30 if now.minute < 30 else 60
    expired = now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=next_half)
    expired_str = expired.strftime('%Y-%m-%d %H:%M:%S')

    prompt = f"""
Candle data (Timeframe M30):

Candle 1 (latest pullback):
Open: {data['candle1']['open']}, High: {data['candle1']['high']}, Low: {data['candle1']['low']}, Close: {data['candle1']['close']}

Candle 2 (impulse candle):
Open: {data['candle2']['open']}, High: {data['candle2']['high']}, Low: {data['candle2']['low']}, Close: {data['candle2']['close']}

Candle 3 (structure/swing):
Open: {data['candle3']['open']}, High: {data['candle3']['high']}, Low: {data['candle3']['low']}, Close: {data['candle3']['close']}

ATR: {data.get('atr', 'N/A')}
RSI: {data.get('rsi', 'N/A')}

Please analyze the market structure above and suggest only 1 optimal trade.

Respond ONLY in JSON format like below:
{{
  "status": "success",
  "instant": {{
    "direction": "BUY or SELL",
    "entry": price (float),
    "sl": stop_loss (float),
    "tp": take_profit (float),
    "winrate": confidence_percent (float),
    "expired": "{expired_str}"
  }},
  "limit": {{
    "direction": same_as_above,
    "entry": same_entry_price,
    "sl": same_sl,
    "tp": same_tp,
    "winrate": same_winrate,
    "expired": "{expired_str}"
  }}
}}
"""
    return prompt

if __name__ == '__main__':
    app.run(debug=True, port=10000)
