import os
from urllib.parse import unquote
from flask import Blueprint, jsonify, send_from_directory, abort
from utils.scan_albums import list_albums, get_album_detail
from config import RECORDINGS_DIR

api = Blueprint("api", __name__)

# 📦 List all albums (basic info: title, artist, cover)
@api.route("/albums")
def get_albums():
    return jsonify(list_albums())

# 📖 Get full metadata + covers + audio info for one album folder
@api.route("/album/<path:folder>")
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
    return send_from_directory(cover_path, filename)

# 🔊 Serve audio files by format (e.g., Audio/mp3/track.mp3)
@api.route("/audio/<path:folder>/<format>/<filename>")
def get_audio(folder, format, filename):
    folder = unquote(folder)
    format = unquote(format)
    filename = unquote(filename)
    audio_dir = os.path.join(RECORDINGS_DIR, folder, "Audio", format)
    file_path = os.path.join(audio_dir, filename)
    if not os.path.exists(file_path):
        return abort(404)
    return send_from_directory(audio_dir, filename)
