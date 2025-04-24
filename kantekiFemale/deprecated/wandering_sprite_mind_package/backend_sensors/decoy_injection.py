
import time
from watcher_core import log_event

def inject_decoy():
    fake_creds = [
        "user: admin | pass: 1234pass!",
        "email: fake@decoy.com | key: FAKE-KEY-9999",
        "login_token=ABC123FAKE999XYZ"
    ]
    for cred in fake_creds:
        log_event(f"[DECOY PAYLOAD INJECTED] {cred}")
        time.sleep(1)
