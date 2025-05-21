from flask import Flask, send_file, abort
import os
from utils import get_file_record

app = Flask(__name__)

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

@app.route('/<hash_id>')
def serve_file(hash_id):
    record = get_file_record(hash_id)
    if not record:
        return abort(404)

    file_path = os.path.join(DOWNLOAD_DIR, record['file_name'])
    if not os.path.exists(file_path):
        return abort(404)
    return send_file(file_path, as_attachment=True)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
