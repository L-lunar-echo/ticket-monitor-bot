import json, threading, time, random
from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)
events_data = {"status": "監控啟動中...", "last_check": "尚未開始"}
lock = threading.Lock()

def monitor_loop():
    while True:
        try:
            with sync_playwright() as p:
                # 加入這三個參數，大幅降低記憶體消耗
                browser = p.chromium.launch(
                    headless=True,
                    args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]
                )
                context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
                page = context.new_page()
                
                with open('events.json', 'r', encoding='utf-8') as f:
                    events = json.load(f)
                
                for ev in events:
                    page.goto(ev['url'], wait_until="domcontentloaded", timeout=60000)
                    time.sleep(random.uniform(2, 5))
                    with lock:
                        events_data[ev['id']] = {"name": ev['name'], "status": "已檢查", "time": time.ctime()}
                
                browser.close()
                events_data["last_check"] = time.ctime()
        except Exception as e:
            print(f"錯誤: {e}")
        time.sleep(300)

threading.Thread(target=monitor_loop, daemon=True).start()

@app.route("/api/status")
def api_status():
    with lock: return jsonify(events_data)

if __name__ == "__main__":
    app.run(port=5001)

