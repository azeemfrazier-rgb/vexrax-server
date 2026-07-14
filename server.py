from flask import Flask, jsonify
import random
import string

app = Flask(__name__)

# store keys (temporary memory)
valid_keys = []

# homepage (so you don't get 404)
@app.route("/")
def home():
    return "Server is running"

# generate a key
@app.route("/generate")
def generate():
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    valid_keys.append(key)
    return jsonify({"key": key})

# verify a key
@app.route("/verify/<key>")
def verify(key):
    if key in valid_keys:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})

# run the server (Render needs this)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
