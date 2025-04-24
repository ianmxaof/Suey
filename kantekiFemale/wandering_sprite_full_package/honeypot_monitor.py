
import os
import time
from watcher_core import log_event

HONEYPOT_DIR = "honeypots"

def monitor_honeypot_access():
    tracked = set()
    while True:
        current = set(os.listdir(HONEYPOT_DIR))
        new_entries = current - tracked
        for item in new_entries:
            log_event(f"HONEYPOT TRIGGERED: {item} was accessed!")
        tracked = current
        time.sleep(5)
