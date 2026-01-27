from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 認証情報の設定
LINE_CHANNEL_ACCESS_TOKEN = '' 
LINE_CHANNEL_SECRET = '' 
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 最新データを保持する変数
latest_data = {"ブルーベリー＆クリームチーズベーグル":{"timestamp": None, "value": None}}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == "「ブルーベリー＆クリームチーズベーグル」の在庫":
        reply = f"現在の「ブルーベリー＆クリームチーズベーグル」は、{latest_data['value']}個です。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))