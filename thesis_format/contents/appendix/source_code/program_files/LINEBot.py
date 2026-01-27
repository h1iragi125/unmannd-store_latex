from flask import Flask, request, jsonify, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime

app = Flask(__name__)

# チャネルアクセストークンおよびチャネルシークレットは伏せている
LINE_CHANNEL_ACCESS_TOKEN = '' 
LINE_CHANNEL_SECRET = '' 
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 最新データを保持する変数
latest_data = {"ブルーベリー＆クリームチーズベーグル":{"timestamp": None, "value": None}}

# Webhook受信
@app.route("/callback", methods=['POST'])
def callback():
    # LINEからの改ざん防止用署名を取得
    signature = request.headers['X-Line-Signature']

    # イベント情報（JSON形式）を取得
    body = request.get_data(as_text=True)
    print("Received body:", body)

    # 処理の受け渡し
    try:
        handler.handle(body, signature)

    # エラー発生時の処理
    except Exception as e:
        print("[ERROR] LINE handler:", e)
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == "「ブルーベリー＆クリームチーズベーグル」の在庫":
        reply = f"現在の「ブルーベリー＆クリームチーズベーグル」は、{latest_data['value']}個です。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    else:
        return

# Raspberry pi3からデータ受信
@app.route("/upload", methods=['POST'])
def upload():

    # JSON形式でデータ受信
    try:
        data = request.get_json()

	# データの妥当性確認
        if not data or "value" not in data:
            return jsonify({"error": "Invalid JSON"}), 400

	# データ取得
        value = data["value"]

	# 最新データに更新
        latest_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest_data["value"] = value

        print(f"[UPLOAD] Received new data from device: {value}")

        return jsonify({"status": "success", "received_value": value}), 200
    except Exception as e:
        print("[ERROR] Upload failed:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/status")
def status():
    html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>最新データ</title>
        <style>
            body {{
                font-family: "Segoe UI", sans-serif;
                background-color: #ffffff;
                color: #000000;
                padding: 50px;
            }}
            h1 {{
                font-size: 28px;
                font-weight: 700; /* 太め */
                margin-bottom: 20px;
            }}
            ul {{
                list-style-type: none;
                padding-left: 10px;
                font-size: 18px;
                font-weight: 400; /* 通常の太さ */
                line-height: 1.8;
            }}
        </style>
    </head>
    <body>
        <h1>最新データ</h1>
        <ul>
            <li>商品名：ブルーベリー＆クリームチーズベーグル</li>
            <li>時間：{latest_data['timestamp']}</li>
            <li>数量：{latest_data['value']}</li>
        </ul>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("[SYSTEM] Flask server is running on port 5000...")
    app.run(host="0.0.0.0", port=5000)