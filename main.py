{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, request, jsonify\
\
app = Flask(__name__)\
\
@app.route('/')\
def home():\
    return 'Golden AI Signal is active.'\
\
@app.route('/signal', methods=['POST'])\
def get_signal():\
    data = request.get_json()\
    # contoh respon dummy, bisa lo ganti sesuai logic sinyal\
    response = \{\
        "symbol": data.get("symbol", "XAUUSD"),\
        "direction": "SELL",\
        "entry": 2322.386,\
        "sl": 2330.712,\
        "tp": 2299.951,\
        "winrate": 83.7\
    \}\
    return jsonify(response)\
\
if __name__ == '__main__':\
    app.run(host='0.0.0.0', port=10000)\
}