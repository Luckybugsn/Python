from flask import Flask, request, send_file, jsonify
import os
import tempfile
import subprocess
import shlex
import uuid

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json() or {}
    url = data.get("url")
    if not url:
        return jsonify({"error":"Missing 'url' in request body"}), 400

    tmpdir = tempfile.mkdtemp(prefix="dl_")
    out_template = os.path.join(tmpdir, "%(title)s-%(id)s.%(ext)s")
    cmd = f"yt-dlp --no-playlist -o {shlex.quote(out_template)} {shlex.quote(url)}"
    try:
        subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, timeout=300)
    except subprocess.CalledProcessError as e:
        return jsonify({"error":"download failed", "detail": e.output.decode(errors="ignore")}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"error":"download timed out"}), 504

    files = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir)]
    if not files:
        return jsonify({"error":"no file downloaded"}), 500
    filepath = files[0]
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
