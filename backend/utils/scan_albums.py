# ✅ Start of scan_albums.py
import os
import json
from typing import Dict, Any
from config import RECORDINGS_DIR
from urllib.parse import quote

def clean_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    return {k: ("" if v in [None, "NaN", "nan"] else v) for k, v in metadata.items()}

def list_albums():
    albums = []
    for folder in os.listdir(RECORDINGS_DIR):
        album_path = os.path.join(RECORDINGS_DIR, folder)
        metadata_path = os.path.join(album_path, "metadata.json")

        if os.path.isdir(album_path) and os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = clean_metadata(json.load(f))
            except Exception as e:
                print(f"Skipping {folder}: {e}")
                continue

            front_cover = None
            front_dir = os.path.join(album_path, "Front Cover")
            if os.path.exists(front_dir):
                encoded_folder = quote(folder)

                preferred = next(
                    (f for f in os.listdir(front_dir)
                     if f.lower().startswith("cover.") and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))),
                    None
                )

                if preferred:
                    front_cover = f"/cover/{encoded_folder}/Front%20Cover/{quote(preferred)}"
                else:
                    for f in os.listdir(front_dir):
                        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                            front_cover = f"/cover/{encoded_folder}/Front%20Cover/{quote(f)}"
                            break

            albums.append({
                "folder": folder,
                "title": metadata.get("Title", folder),
                "artist": metadata.get("Artist", ""),
                "cover": front_cover
            })

    return albums

def get_album_detail(folder: str) -> Dict[str, Any]:
    album_path = os.path.join(RECORDINGS_DIR, folder)
    metadata_path = os.path.join(album_path, "metadata.json")

    if not os.path.exists(metadata_path):
        return {"error": "Album not found"}

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = clean_metadata(json.load(f))

    def find_image(subdir: str):
        dir_path = os.path.join(album_path, subdir)
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    return f"/cover/{quote(folder)}/{quote(subdir)}/{quote(file)}"
        return None

    front = find_image("Front Cover")
    back = find_image("Back Cover")

    audio_root = os.path.join(album_path, "Audio")
    audio_mp3 = []
    downloads = []

    if os.path.exists(audio_root):
        for fmt in os.listdir(audio_root):
            fmt_path = os.path.join(audio_root, fmt)
            if os.path.isdir(fmt_path):
                for file in sorted(os.listdir(fmt_path)):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in [".mp3", ".wav", ".flac", ".aac"]:
                        file_entry = {
                            "title": os.path.splitext(file)[0],
                            "file": f"/audio/{folder}/{fmt}/{file}"
                        }
                        if ext == ".mp3":
                            audio_mp3.append(file_entry)
                        downloads.append({**file_entry, "format": fmt})

    return {
        "folder": folder,
        "metadata": metadata,
        "frontCover": front,
        "backCover": back,
        "audio": {"mp3": audio_mp3},
        "downloads": downloads
    }
