from flask import Flask, request, abort
from linebot import WebhookHandler

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