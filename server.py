from flask import Flask, request, jsonify
import json, os
import random, string
from datetime import datetime, timedelta

app = Flask(__name__)
KEY_FILE = "keys.json"

# ---------------- LOAD/SAVE ----------------
def load_keys():
    if not os.path.exists(KEY_FILE):
        return {}
    with open(KEY_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(KEY_FILE, "w") as f:
        json.dump(keys, f, indent=4)

# ---------------- GENERATE KEY ----------------
def make_key():
    return "VEX-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

@app.route("/generate", methods=["GET"])
def generate():
    keys = load_keys()

    new_key = make_key()

    # ⏳ expires in 1 day (change this)
    expiry_time = datetime.now() + timedelta(days=1)

    keys[new_key] = {
        "used": False,
        "expiry": expiry_time.isoformat()
    }

    save_keys(keys)

    return jsonify({
        "key": new_key,
        "expires": expiry_time.isoformat()
    })

# ---------------- VALIDATE ----------------
@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    user_key = data.get("key")

    keys = load_keys()

    if user_key not in keys:
        return jsonify({"status": "invalid"})

    key_data = keys[user_key]

    # check expiry
    expiry = datetime.fromisoformat(key_data["expiry"])
    if datetime.now() > expiry:
        return jsonify({"status": "expired"})

    if key_data["used"]:
        return jsonify({"status": "used"})

    # mark used
    keys[user_key]["used"] = True
    save_keys(keys)

    return jsonify({"status": "valid"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(port=5000)