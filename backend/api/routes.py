import os
import json
from urllib.parse import unquote
from flask import Blueprint, jsonify, send_from_directory, abort
from utils.scan_albums import list_albums
from config import RECORDINGS_DIR

api = Blueprint("api", __name__)

@api.route("/albums")
def get_albums():
    return jsonify(list_albums())

@api.route("/album/<path:album>")
def get_metadata(album):
    album = unquote(album)
    metadata_path = os.path.join(RECORDINGS_DIR, album, "metadata.json")
    if not os.path.exists(metadata_path):
        return abort(404)
    with open(metadata_path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@api.route("/cover/<path:album>/<filename>")
def get_cover(album, filename):
    album = unquote(album)
    filename = unquote(filename)
    cover_path = os.path.join(RECORDINGS_DIR, album, "Front Cover")
    file_path = os.path.join(cover_path, filename)
    if not os.path.exists(file_path):
        return abort(404)
    return send_from_directory(cover_path, filename)

@api.route("/audio/<path:album>/<folder>/<filename>")
def get_audio(album, folder, filename):
    album = unquote(album)
    folder = unquote(folder)
    filename = unquote(filename)
    audio_dir = os.path.join(RECORDINGS_DIR, album, "Audio", folder)
    file_path = os.path.join(audio_dir, filename)
    if not os.path.exists(file_path):
        return abort(404)
    return send_from_directory(audio_dir, filename)
