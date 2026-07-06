from flask import Flask, jsonify
import threading, time

app = Flask(__name__)

# 簡單的狀態變數
data = {"status": "系統運作正常"}

@app.route("/")
def home():
    return "系統運行中！"

@app.route("/api/status")
def api_status():
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5001)
