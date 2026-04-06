import requests
import time
import json
import os

PLAYER_NAME = "alt8888"
THRESHOLD_MINUTES = 20
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

STATE_FILE = "state.json"

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {"status": "unknown"}

url = f"https://api.idleclans.com/player?name={PLAYER_NAME}"
data = requests.get(url).json()

last_activity = data["lastActivity"]
current_time = int(time.time())

idle_minutes = (current_time - last_activity) / 60

is_idle = idle_minutes > THRESHOLD_MINUTES

if is_idle and state["status"] != "idle":
    requests.post(WEBHOOK_URL, json={"content": f"⚠️ {PLAYER_NAME} is idle"})
    state["status"] = "idle"

elif not is_idle and state["status"] != "active":
    requests.post(WEBHOOK_URL, json={"content": f"✅ {PLAYER_NAME} is back"})
    state["status"] = "active"

with open(STATE_FILE, "w") as f:
    json.dump(state, f)
