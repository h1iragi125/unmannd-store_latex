import requests
import json
import time

# サーバのURL指定（IPアドレスは伏せている）
FLASK_SERVER_URL = "http:// {サーバを立てたPCのIPアドレス（IPv4）}:5000/upload"

# データ送信準備
def send_data_to_server(value):
    data = {"value": value}
    try:
        res = requests.post(FLASK_SERVER_URL, json=data)
        print(f"[SEND] Sent{value}, Status: {res.status_code}")

    # エラー処理
    except Exception as e:
        print(f"[ERROR] {e}")

# データ定期送信
if __name__ == "__main__":
    while True:

        # センサ値のダミーデータ（実用化の際は検出したセンサデータに切り替える）
        fake_value = 5
        send_data_to_server(fake_value)
        time.sleep(10)