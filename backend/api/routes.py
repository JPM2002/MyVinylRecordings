import os
import zipfile
import io
from urllib.parse import unquote
from flask import Blueprint, jsonify, send_file, abort  # ✅ send_file instead of send_from_directory
from utils.scan_albums import list_albums, get_album_detail
from config import RECORDINGS_DIR

api = Blueprint("api", __name__)

# 📦 List all albums (basic info: title, artist, cover)
@api.route("/albums")
def get_albums():
    return jsonify(list_albums())

# 📖 Get full metadata + covers + audio info for one album folder
@api.route("/albums/<path:folder>")
def get_album_detail_route(folder):
    folder = unquote(folder)
    album = get_album_detail(folder)
    if "error" in album:
        return abort(404)
    return jsonify(album)

# 🖼️ Serve front/back cover images
@api.route("/cover/<path:folder>/<subfolder>/<filename>")
def get_cover(folder, subfolder, filename):
    folder = unquote(folder)
    subfolder = unquote(subfolder)
    filename = unquote(filename)
    cover_path = os.path.join(RECORDINGS_DIR, folder, subfolder)
    file_path = os.path.join(cover_path, filename)
    if not os.path.exists(file_path):
        return abort(404)
    return send_file(file_path)

# 📦 Create and serve a ZIP of the requested audio format
@api.route("/download/<path:folder>/<format>")
def download_format(folder, format):
    folder = unquote(folder)
    format = unquote(format).lower()
    audio_path = os.path.join(RECORDINGS_DIR, folder, "Audio", format)

    if not os.path.exists(audio_path) or not os.path.isdir(audio_path):
        return abort(404)

    files = [
        f for f in os.listdir(audio_path)
        if f.lower().endswith((".mp3", ".flac", ".wav", ".aac"))
    ]

    if not files:
        return abort(404)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in files:
            file_path = os.path.join(audio_path, f)
            zipf.write(file_path, arcname=f)
    zip_buffer.seek(0)

    filename = f"{folder}-{format}.zip".replace(" ", "_")
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=filename
    )
