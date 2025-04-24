import time
from watcher_core import log_event
from decoy_injection import inject_decoy
from sprite_reaction import trigger_sprite_reaction
from telegram_alert import send_telegram_alert

def start_watcher():
    log_event("Starting Watcher Backend...")

    # Simulate backend watching
    while True:
        event = check_for_event()
        if event:
            log_event(f"Event detected: {event}")
            if event == "keylogger_spike":
                inject_decoy()
                trigger_sprite_reaction(event)
                send_telegram_alert("Keylogger spike detected, decoy injected!")
        time.sleep(5)

def check_for_event():
    # Placeholder function to simulate event detection
    # Replace with actual keylogger detection logic
    return "keylogger_spike"  # Simulated event

start_watcher()
