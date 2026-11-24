from collections import deque
import os
import threading
from flask import Flask, jsonify, request

queue = deque()
lock = threading.Lock()
app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"status": "ok", "queued": len(queue)})


@app.route("/push", methods=["POST"])
def push():
    data = request.get_json(silent=True) or {}
    with lock:
        queue.append(data)
    return jsonify({"ok": True, "queued": len(queue)})


@app.route("/poll", methods=["GET"])
def poll():
    with lock:
        cmd = queue.popleft() if queue else None
    return jsonify({"command": cmd})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)