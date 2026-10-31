import requests

BOT_TOKEN = '7661561704:AAES8gFbKRLXYzCasFxu-dGZ3l1yQ2i3-Fo'
CHAT_ID = '7547029018'

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram alert failed: {e}")
