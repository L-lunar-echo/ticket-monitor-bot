import json, threading, time, logging
from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)
events_data = {"status": "監控啟動中..."}
lock = threading.Lock()

def monitor_loop():
    while True:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                # 使用 auth.json 進行登入狀態模擬
                context = browser.new_context(storage_state="auth.json")
                page = context.new_page()
                with open('events.json', 'r', encoding='utf-8') as f:
                    events = json.load(f)
                for ev in events:
                    page.goto(ev['url'], wait_until="domcontentloaded", timeout=60000)
                    time.sleep(2)
                    with lock:
                        events_data[ev['id']] = {"name": ev['name'], "status": "已檢查"}
                browser.close()
        except Exception as e:
            print(f"錯誤: {e}")
        time.sleep(60)

threading.Thread(target=monitor_loop, daemon=True).start()

@app.route("/api/status")
def api_status():
    with lock: return jsonify(events_data)

if __name__ == "__main__":
    app.run(port=5001)
