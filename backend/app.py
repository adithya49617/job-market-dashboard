from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from analyze import run_all_analytics
from fetch import fetch_jobs

app = Flask(__name__, static_folder="static")
CORS(app)

# ── Serve React frontend ──────────────────────────────────────────────────────
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

# ── Health check ──────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "api_enabled": bool(os.environ.get("RAPIDAPI_KEY"))
    })

# ── Analytics endpoint ────────────────────────────────────────────────────────
@app.route("/analytics", methods=["GET"])
def analytics():
    query = request.args.get("query", "data scientist")
    location = request.args.get("location", "United States")
    live = request.args.get("live", "false").lower() == "true"

    api_jobs = None
    data_source = "sample"

    if live:
        api_jobs = fetch_jobs(query=query, location=location, num_pages=2)
        if api_jobs:
            data_source = "live"

    result = run_all_analytics(api_jobs)
    result["data_source"] = data_source
    result["query"] = query
    result["location"] = location

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
