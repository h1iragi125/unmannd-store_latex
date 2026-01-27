from flask import Flask, request, jsonify
from datetime import datetime

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