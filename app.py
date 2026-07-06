import requests # 確保這有被 import

def monitor_loop():
    while True:
        try:
            with open('events.json', 'r', encoding='utf-8') as f:
                events = json.load(f)
            
            for ev in events:
                # 改用 requests 直接獲取網頁，不需要開啟瀏覽器
                response = requests.get(ev['url'], timeout=10)
                status_text = "連線成功" if response.status_code == 200 else f"錯誤: {response.status_code}"
                
                with lock:
                    events_data[ev['id']] = {"name": ev['name'], "status": status_text, "time": time.ctime()}
            
            events_data["last_check"] = time.ctime()
            print(f"檢查完成: {time.ctime()}") # 現在這行會出現在 Logs 裡了
        except Exception as e:
            print(f"監控錯誤: {e}")
        
        time.sleep(300) # 等待 5 分鐘
