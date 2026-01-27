from flask import Flask

# 最新データを保持する変数
latest_data = {"ブルーベリー＆クリームチーズベーグル":{"timestamp": None, "value": None}}

@app.route("/status")

# HTMLで記述
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