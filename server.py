from flask import Flask, request, jsonify
import time
import uuid

app = Flask(__name__)

# store keys in memory (for now)
keys = {}

# ---------------- GENERATE KEY ----------------
@app.route("/generate", methods=["GET"])
def generate():
    key = str(uuid.uuid4())[:8].upper()
    
    keys[key] = {
        "used": False,
        "expires": time.time() + 3600  # 1 hour expiry
    }

    return jsonify({"key": key})

# ---------------- VALIDATE KEY ----------------
@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    key = data.get("key")

    if key not in keys:
        return jsonify({"status": "invalid"})

    info = keys[key]

    if info["expires"] < time.time():
        return jsonify({"status": "expired"})

    if info["used"]:
        return jsonify({"status": "used"})

    info["used"] = True
    return jsonify({"status": "valid"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
