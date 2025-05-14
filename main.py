import os
import openai
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
                {"role": "system", "content": "You are a professional forex analyst. Given candle data, suggest best trade (BUY/SELL), entry, SL, TP, and winrate. Respond in JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return jsonify(eval(answer))  # ⚠️ bisa diganti json.loads(answer)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def build_prompt(data):
    prompt = f"""
Candle data (M30):

Candle 1 (latest pullback):
Open: {data['candle1']['open']}, High: {data['candle1']['high']}, Low: {data['candle1']['low']}, Close: {data['candle1']['close']}

Candle 2 (impulse):
Open: {data['candle2']['open']}, High: {data['candle2']['high']}, Low: {data['candle2']['low']}, Close: {data['candle2']['close']}

Candle 3 (structure/swing):
Open: {data['candle3']['open']}, High: {data['candle3']['high']}, Low: {data['candle3']['low']}, Close: {data['candle3']['close']}

ATR: {data.get('atr', 'N/A')}
RSI: {data.get('rsi', 'N/A')}

Now suggest:
- direction (BUY or SELL)
- entry price
- stop loss (SL)
- take profit (TP)
- winrate estimation (in percent)
- expired (set to end of current M30 candle in UTC)

Respond ONLY in JSON format, like this:
{{
  "status": "success",
  "instant": {{
    "direction": "...",
    "entry": ...,
    "sl": ...,
    "tp": ...,
    "winrate": ...,
    "expired": "YYYY-MM-DD HH:MM:SS"
  }},
  "limit": {{
    "direction": "...",
    "entry": ...,
    "sl": ...,
    "tp": ...,
    "winrate": ...,
    "expired": "YYYY-MM-DD HH:MM:SS"
  }}
}}
"""
    return prompt

if __name__ == '__main__':
    app.run(debug=True, port=10000)
