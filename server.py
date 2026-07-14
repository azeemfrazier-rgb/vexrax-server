from flask import Flask, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

KEYS_FILE = "keys.json"

# Load keys
def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    with open(KEYS_FILE, "r") as f:
        return json.load(f)

# Save keys
def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=4)

# Route: check key
@app.route("/check_key", methods=["POST"])
def check_key():
    data = request.json
    key = data.get("key")

    keys = load_keys()

    if key in keys:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})

# Route: generate key
@app.route("/generate_key", methods=["GET"])
def generate_key():
    keys = load_keys()

    new_key = str(uuid.uuid4())
    keys[new_key] = {"active": True}

    save_keys(keys)

    return jsonify({"key": new_key})

# ✅ IMPORTANT FIX HERE
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)