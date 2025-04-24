import os

LOG_PATH = "logs/event_log.txt"
if not os.path.exists("logs"):
    os.makedirs("logs")

def log_event(message):
    with open(LOG_PATH, 'a') as f:
        f.write(f"{message}\n")
