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
                browser = p.chromium.launch(headless=True)
                # 匿名模式：不使用 auth.json，只使用偽裝的 User-Agent
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
                )
                page = context.new_page()
                
                with open('events.json', 'r', encoding='utf-8') as f:
                    events = json.load(f)
                
                for ev in events:
                    print(f"正在檢查: {ev['name']}")
                    page.goto(ev['url'], wait_until="domcontentloaded", timeout=60000)
                    time.sleep(random.uniform(2, 5)) # 模擬人類瀏覽的隨機等待時間
                    
                    with lock:
                        events_data[ev['id']] = {"name": ev['name'], "status": "已檢查", "time": time.ctime()}
                
                browser.close()
                events_data["last_check"] = time.ctime()
        except Exception as e:
            print(f"監控錯誤: {e}")
        
        # 隨機等待 3 到 8 分鐘，避免行為規律被偵測
        sleep_time = random.randint(180, 480)
        print(f"下一次檢查將在 {sleep_time} 秒後進行...")
        time.sleep(sleep_time)

# 啟動背景執行緒
threading.Thread(target=monitor_loop, daemon=True).start()

@app.route("/api/status")
def api_status():
    with lock: return jsonify(events_data)

@app.route("/")
def home():
    return "監控系統運行中，請訪問 /api/status 查看狀態。"

if __name__ == "__main__":
    app.run(port=5001)
    
