import json, threading, time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 全域變數儲存狀態
events_data = {}
lock = threading.Lock()

def load_events_from_json():
    with open('events.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def monitor_loop():
    global events_data
    while True:
        try:
            # 這裡模擬監控邏輯，將結果寫入 events_data
            # 之後你可以將你的爬蟲邏輯寫在這裡
            current_events = load_events_from_json()
            with lock:
                events_data = {ev['id']: ev for ev in current_events}
        except Exception as e:
            print(f"監控錯誤: {e}")
        time.sleep(60)

threading.Thread(target=monitor_loop, daemon=True).start()

@app.route("/")
def index():
    with lock:
        # 將資料傳給 index.html 渲染
        return render_template("index.html", events=events_data)

@app.route("/api/status")
def api_status():
    with lock:
        return jsonify(events_data)

if __name__ == "__main__":
    app.run(port=5001)
