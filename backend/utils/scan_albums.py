import os
import json
from config import RECORDINGS_DIR

def list_albums():
    albums = []
    for folder_name in os.listdir(RECORDINGS_DIR):
        album_path = os.path.join(RECORDINGS_DIR, folder_name)
        metadata_path = os.path.join(album_path, "metadata.json")

        if os.path.isdir(album_path) and os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            # 🔍 Try to find an image in "Front Cover"
            cover_image = None
            cover_folder = os.path.join(album_path, "Front Cover")
            if os.path.exists(cover_folder):
                for file in os.listdir(cover_folder):
                    if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        cover_image = f"/cover/{folder_name}/{file}"
                        break

            albums.append({
                "title": metadata.get("title", folder_name),
                "artist": metadata.get("artist", ""),
                "folder": folder_name,
                "cover": cover_image
            })

    return albums
